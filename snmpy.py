#!/ms/dist/python/PROJ/core/2.7.3-64/bin/python
# -*- coding: utf-8 -*-

from ScvLib import *
from SplunkLib import SplunkFeedObject
from yamlLoader import load_yaml
import writtingLog
import argparse
import sys
import subprocess
import re
import calendar
import time
import csv
import logging


parser = argparse.ArgumentParser()


parser.add_argument("-env", "--env", help="path of repo with environment",
                    type=str, default=None)
parser.add_argument("-f", "--file", help="mib file",
                    type=str, default=None)
parser.add_argument("-oid", "--oid", help="respective oid to make the query",
                    type=str, default=None)
parser.add_argument("-host", "--host", help="ip or hostname are valid "
                                            "arguments",
                    type=str, default=None)
parser.add_argument("-c", "--config", help="path of configuration file (YAML "
                                           "file)",
                    type=str, default=None)
parsed_args = parser.parse_args()

default_env_path = "/ms/dist/nms/PROJ/operations_analytics_scripts/dev"
# default_env_path = "/v/global/user/a/ac/acostosc/repos/"\
#                      "operations_analytics_scripts/"
if parsed_args.env is None:
    parsed_args.env = default_env_path
sys.path.insert(1, "{}/python/lib".format(parsed_args.env))
# from writtingLog import writtingLog


# --------------------------- main definition ----------------------------------
def main(margs=None):
    """
    The following 'if' statement is in charge of defaulting to sys.argv when no
    'margs' is passed.
    """
    if margs is None:
        margs = sys.argv[1:]
    # Argument parsing in main scope (based on global's arguments)

    parsed_margs = argparse.ArgumentParser(
        parents=[parser], add_help=False).parse_args(margs)

    # Validate which method will be use run as program or module
    # this section will run if the cmd get the info through yaml file
    if parsed_margs.host is None and parsed_margs.oid is None:
        # this condition use yaml file to load the parameters
        # argument validation

        conf_file = ("{}".format(parsed_margs.config)
                     if parsed_margs.config is None else parsed_margs.config)

        config_data = load_yaml(conf_file)
        if conf_file is None:
            print("invalid configuration file please validate")
            # return 1
        else:
            # loading data from yaml file
            logsdir = config_data[1].get("logsdir", None)
            nas = config_data[1].get("NAS", None)
            scvNamespace = config_data[1].get("scvNamespace", None)
            scvCommunity = config_data[1].get("scvCommunity", None)
            scvUrl = config_data[1].get("scvUrl", None)
            version = config_data[1].get("version", None)
            splunk = config_data[1].get("splunkUrlPost", None)

        if version == "v3":
            username = config_data[1].get("username", None)
            securityLevel = config_data[1].get("securityLevel", None)
            authProtocol = config_data[1].get("authProtocol", None)
            passPhrase = config_data[1].get("passPhrase", None)
            passPhraseProtocol = config_data[1].get("passPhraseProtocol", None)
            privProtocol = config_data[1].get("privProtocol", None)
            mibPath = config_data[1].get("mibPath", None)
            hosts = config_data[1].get("hosts", None)
            oids = config_data[1].get("oids", None)
            tables = config_data[1].get("tables", None)
            # splunk = config_data[1].get("splunkUrlPost", None)

            if splunk is not None:
                splunk_host = re.search('(?P<prot>^http\:\/\/)\w*?(?P<host>'
                                        '\w+[^:/]+)', 'http://ivapp1132449.'
                                        'devin1.ms.com:9090/en-US/app'
                                        '/launcher/home')
                splunk_host = splunk_host.group(2)
                splunk_val = "ping -c 3 {}".format(splunk_host)
                try:
                    subprocess.check_output(splunk_val, stderr=subprocess.PIPE,
                                            shell=True)
                except subprocess.CalledProcessError as error:
                    print error
                    # return 1

                # --------------------------- snmpwalk version 3 ---------------
                # execute snmpwalk cmd itererating for every host and every
                # oid contained in
                # yaml file
                for host in hosts:
                    for oid in oids:
                        snmpV3cmd = "snmpwalk -{} -Os -u {} -l {} -a {} -A {}"\
                                    " -X {} -x {} -OQ -Oa -M {} -m ALL " \
                                    "{} {}".format(version, username,
                                                   securityLevel,
                                                   authProtocol, passPhrase,
                                                   passPhraseProtocol,
                                                   privProtocol, mibPath, host,
                                                   oid)
                        # those print are for validation pruposes print the cmd
                        # that is running
                        print(snmpV3cmd)
                        print("[getting snmpwalk data from {}]".format(host))
                        # this try validate the output of the cmd
                        try:
                            output = subprocess.check_output(snmpV3cmd,
                                                             stderr=subprocess.PIPE,
                                                             shell=True).strip()
                        except:
                            snmperror = "Timeout occur for {}".format(host)
                            print(snmperror)
                            writtingLog("info", "warning {}".format(snmperror),
                                        nas + logsdir)
                            return 1
                        outputList = output.split("\n")
                        # print(outputList)
                        # this is the regular expression that cut the output string
                        # and pass at their
                        # respective label
                        rex = re.compile("(?P<Description>.*?)\s=\s(?P<Value>'\
                                         '.*?)$")
                        dictList = [rex.search(x).groupdict()
                                    for x in outputList if rex.search(x)]
                        # for statement ingest the labels datatype and principal
                        for out in dictList:
                             out["dataType"] = "snmpWalk"
                             out["principal_oid"] = oid
                             host = host.split(".")
                             host = host[0]
                             out["hostname"] = host
                        """ ingest the data in splunk """
                        # print(dictList)
                        splunk_feeder = SplunkFeedObject(config_data[1], "p")
                        # print(config_data[1])
                        finaldata = splunk_feeder.eventPush(dictList)

                # -------------------------- snmptable version 3 ---------------
                # execute snmpwalk cmd itererating for every host and every oid
                # contained
                # in yaml file
                for host in hosts:
                    for table in tables:
                        snmpV3tab = "snmptable -{} -Os -u {} -l {} -a {} -A {}"\
                                    " -X {} -x {} -OQ -Oa -M {} -m ALL -Ci "\
                                    "-Oq -Cf '|' -L n" \
                                    " -OU {} {}".format(version, username,
                                                        securityLevel,
                                                        authProtocol,
                                                        passPhrase,
                                                        passPhraseProtocol,
                                                        privProtocol, mibPath,
                                                        host, table)
                        # those print are for validation pruposes print the cmd
                        # that is rinning print(snmpV3tab)
                        # print("[getting snmptable data from {}]".format(host))
                        # this try validate the output of the cmd
                        try:
                            output_table = subprocess.check_output(snmpV3tab,
                                                                   stderr=subprocess.PIPE,
                                                                   shell=True).strip()
                        except:
                            snmperror = "Timeout occur for {}".format(host)
                            print(snmperror)
                            writtingLog("info", "warning {}".format(snmperror),
                                        nas + logsdir)
                            return 1
                        # this split the output string by brea line and pipe
                        outputList2 = output_table.split("\n")
                        headerlist = outputList2[2].split("|")
                        output_sample = outputList2[3:]
                        # this section ingest the output to a csv delimited by | and stablish the table headers
                        reader = csv.DictReader(output_sample, delimiter='|',
                                                fieldnames=headerlist)
                        eventlist = [x for x in reader]
                        # for statement ingest the labels datatype and principal
                        for x in eventlist:
                            x["dataType"] = "snmpTable"
                            x["principal_table"] = table
                            x["snmpIndex"] = x.pop("index")
                        splunk_feeder2 = SplunkFeedObject(config_data[1], "p")
                        finaldata = splunk_feeder2.eventPush(eventlist)

        # --------------- snmp version 2 begins ----------------

        elif version == "v2":
            if splunk is not None:
                splunk_host = re.search('(?P<prot>^http\:\/\/)\w*?(?P<host>'
                                        '\w+[^:/]+)', 'http://ivapp1132449.'
                                        'devin1.ms.com:9090/en-US/app/launcher'
                                        '/home')
                splunk_host = splunk_host.group(2)
                splunk_val = "ping -c 3 {}".format(splunk_host)
                try:
                    subprocess.check_output(splunk_val, stderr=subprocess.PIPE,
                                            shell=True)
                    print('ping success')
                except subprocess.CalledProcessError as error:
                    print error
                    # return 1

            mibPath = config_data[1].get("mibPath", None)
            hosts = config_data[1].get("hosts", None)
            oids = config_data[1].get("oids", None)
            tables = config_data[1].get("tables", None)
            splunk = config_data[1].get("splunkUrlPost", None)
            community = config_data[1].get("v2Community", None)

            # ------------------------ snmpwalk version 2 ----------------------
            # execute snmpwalk cmd itererating for every host and every
            # oid contained in
            # yaml file

            for host in hosts:
                snmpV2cmd = "snmpwalk -{}c -c {} {} -M {} -m ALL -Os -OQ {}"\
                            " -Oa".format(version, community,
                                          host, mibPath, oid)
                print(snmpV2cmd)
                print("[getting snmpwalk data from {}]".format(host))
                try:
                    output = subprocess.check_output(snmpV2cmd,
                                                     stderr=subprocess.PIPE,
                                                     shell=True).strip()
                except:
                    snmperror = "Timeout occur for {}".format(host)
                    print(snmperror)
                    writtingLog("info", "warning {}".format(snmperror), nas +
                                logsdir)
                    return 1
                outputList = output.split("\n")
                rex = re.compile("(?P<Description>.*?)\s=\s(?P<Value>'\
                                 '.*?)$")
                dictList = [rex.search(x).groupdict()
                            for x in outputList if rex.search(x)]
                # for statement ingest the labels datatype and principal
                for out in dictList:
                     out["dataType"] = "snmpWalk"
                     out["principal_oid"] = oid
                     host = host.split(".")
                     host = host[0]
                     out["hostname"] = host
                """ ingest the data in splunk """
                # print(dictList)
                splunk_feeder = SplunkFeedObject(config_data[1], "p")
                # print(config_data[1])
                finaldata = splunk_feeder.eventPush(dictList)

            # -------------------------- snmptable version 2 ---------------
            # execute snmpwalk cmd itererating for every host and every oid
            # contained
            # in yaml file

            for host in hosts:
                for table in tables:
                    snmpV2tab = "snmptable -{}c -c {} {} -CI -CB -Ci -OX -Cb"\
                                " -Cc 16 -Cw 64 {}".format(version, community,
                                                           host,
                                                           table)
                    # those print are for validation pruposes print the cmd
                    print(snmpV2tab)
                    print("[getting snmptable data from {}]".format(host))
                    # this try validate the output of the cmd
                    try:
                        output_table = subprocess.check_output(snmpV2tab,
                                                               stderr=subprocess.PIPE,
                                                               shell=True).strip()
                    except:
                        snmperror = "Timeout occur for {}".format(host)
                        print(snmperror)
                        writtingLog("info", "warning {}".format(snmperror),
                                    nas + logsdir)
                        return 1
                    # this split the output string by brea line and pipe
                    outputList2 = output_table.split("\n")
                    headerlist = outputList2[2].split("|")
                    output_sample = outputList2[3:]
                    # this section ingest the output to a csv delimited by
                    # | and stablish the table headers
                    reader = csv.DictReader(output_sample, delimiter='|',
                                            fieldnames=headerlist)
                    eventlist = [x for x in reader]
                    # for statement ingest the labels datatype and principal
                    for x in eventlist:
                        x["dataType"] = "snmpTable"
                        x["principal_table"] = table
                        x["snmpIndex"] = x.pop("index")
                    splunk_feeder2 = SplunkFeedObject(config_data[1], "p")
                    finaldata = splunk_feeder2.eventPush(eventlist)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt as k:
        print("Forced Exit")


# --------------------------- snmpwalk version 2 ------------------------------
    # elif version == "v2":
    #     mibPath = config_data[1].get("mibPath", None)
    #     hosts = config_data[1].get("hosts", None)
    #     for host in hosts:
    #         snmpV2cmd = "snmpwalk -{} -c {} {} -M {} -m ALL".format(version,
    #                                                                 scvCommunity,
    #                                                                 host,
    #                                                                 mibPath)
    #         try:
    #             output = subprocess.check_output(snmpV2cmd,
    #                                              stderr=subprocess.PIPE,
    #                                              shell=True).strip()
    #         except:
    #             snmperror = "Timeout occur for {}".format(host)
    #             print(snmperror)
    #             writtingLog("warning {}".format(snmperror), logsdir)
    #             return 1
    #         outputList = output.split("\n")
# do something
# for closing after error use return 1 instead of sys.exit()
