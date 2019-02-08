#!/ms/dist/python/PROJ/core/2.7.3-64/bin/python or /usr/bin/python

from ScvLib import *
from SplunkLib import *
from yamlLoader import load_yaml
from writtingLog import writtingLog
import argparse
import sys
import subprocess
import re
import calendar
import time
import csv


parser = argparse.ArgumentParser()
""""
Boilerplate for stand-alone script

When usng the script as a program arguments can be used for global-scoped
variables and thus they can be set outside the main function, arg 'env' is the
perfect example.
(i.e. a library path to add to sys.path for importing modules from it)

When using the script as a module and based in our example use case, if the
argument isn't defaulted the imports may fail, but if it's defaulted we
wouldn't be able to override it, in such case we would have to add the desired
path to sys.path and import the modules before actually importing this script.
"""
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

default_env_path = "/ms/dist/nms/PROJ/operations_analytics_scripts/prod"
if parsed_args.env is None:
    parsed_args.env = default_env_path

sys.path.insert(1, "{}/python/lib".format(parsed_args.env))


"""
The main function is defined with a None-defaulted argument 'margs' which is
the conduct through which we will pass our arguments to our local parser (which
will inherit all the arguments from our global one), keeping in mind that
those arguments intened for global use will not change if we try to set them
through margs.

When using the script as a program, the bottom code snippet starting at
'if __name__ == "__main__":' will execute, passing no arguments to main and thus
causing it to take them from sys.argv (which is the same place the global parser
takes them from) so everything passed to the program will be identical on both
the global and main's local parser.
When using the script as a module, the arguments will then be passed to main
through 'margs', the local parser will act upon them and output a namespace
called 'parsed_margs' whereas the global parser will operate as if no arguments
were passed, causing only defaulted args from the global parser to be
initialized."""


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
            return 1
        else:
            # loading data from yaml file
            logsdir = config_data[1].get("logsdir", None)
            nas = config_data[1].get("NAS", None)
            scv_namespace = config_data[1].get("scvNamespace", None)
            scv_community = config_data[1].get("scvCommunity", None)
            scv_url = config_data[1].get("scvUrl", None)
            version = config_data[1].get("version", None)

        if version == "v3":
            username = config_data[1].get("username", None)
            security_level = config_data[1].get("securityLevel", None)
            auth_protocol = config_data[1].get("authProtocol", None)
            pass_phrase = config_data[1].get("passPhrase", None)
            pass_phrase_protocol = config_data[1].get("passPhraseProtocol",
                                                      None)
            priv_protocol = config_data[1].get("privProtocol", None)
            mib_path = config_data[1].get("mibPath", None)
            hosts = config_data[1].get("hosts", None)
            oids = config_data[1].get("oids", None)
            tables = config_data[1].get("tables", None)

# --------------------------- snmpwalk version 3 -------------------------------
            for host in hosts:
                for oid in oids:
                    snmp_v3cmd = "snmpwalk -{} -Os -u {} -l {} -a {} -A {} -X "\
                        "{} -x {} -OQ -Oa -M {} -m ALL " \
                        "{} {}".format(version, username,
                                       security_level,
                                       auth_protocol, pass_phrase,
                                       pass_phrase_protocol,
                                       priv_protocol,
                                       mib_path, host, oid)
                    print(snmp_v3cmd)
                    print("[getting snmpwalk data from {}]".format(host))
                    try:
                        output = subprocess.check_output(snmp_v3cmd,
                                                         stderr=subprocess.PIPE,
                                                         shell=True).strip()
                    except:
                        snmperror = "Timeout occur for {}".format(host)
                        print(snmperror)
                        writtingLog("info", "warning {}".format(snmperror),
                                    nas + logsdir)
                        return 1
                    output_list = output.split("\n")
                    # print(output_list)
                    rex = re.compile("(?P<Description>.*?)\s=\s(?P<Value>.*?)$")
                    dict_list = [rex.search(x).groupdict() for x in
                                 output_list if rex.search(x)]
                    for out in dict_list:
                        out["dataType"] = "snmpWalk"
                        out["principal_oid"] = oid
                    splunk_feeder = SplunkFeedObject(config_data[1], "p")
                    finaldata = splunk_feeder.eventPush(dict_list)

# -------------------------- snmptable version 3 -------------------------------
            for host in hosts:
                for table in tables:
                    snmp_v3tab = "snmptable -{} -Os -u {} -l {} -a {} -A {} " \
                                 "-X {} -x {} -OQ -Oa -M {} -m ALL -Ci -Oq  " \
                                 "-Cf '|'  -L n -OU {} {}".format(version,
                                                                  username,
                                                                  security_level,
                                                                  auth_protocol,
                                                                  pass_phrase,
                                                                  pass_phrase_protocol,
                                                                  priv_protocol,
                                                                  mib_path,
                                                                  host, table)
                    print(snmp_v3tab)
                    print("[getting snmptable data from {}]".format(host))
                    try:
                        output_table = subprocess.check_output(snmp_v3tab,
                                                               stderr=subprocess.PIPE,
                                                               shell=True).strip()
                    except:
                        snmperror = "Timeout occur for {}".format(host)
                        print(snmperror)
                        writtingLog("info", "warning {}".format(snmperror),
                                    nas + logsdir)
                        return 1
                    output_list2 = output_table.split("\n")
                    headerlist = output_list2[2].split("|")
                    # print(headerlist)
                    output_sample = output_list2[3:]
                    reader = csv.DictReader(output_sample, delimiter='|',
                                            fieldnames=headerlist)
                    eventlist = [x for x in reader]
                    for x in eventlist:
                        x["dataType"] = "snmpTable"
                        x["principal_table"] = table
                    # print(headerlist)
                    # print(eventlist)
                    # # for x in d1:
                    # #     desc = x.keys()
                    # #     val = x.values()
                    # #     for y in desc:
                    # #         for valor in val:
                    # #             cadena = y + " = " + valor
                    # #             lista.append(cadena)
                    # # rex = re.compile("(?P<Description>.*?)=(?P<Type>.*?):(?P<Value>.*?)$")
                    # # list2 = [rex.search(x).groupdict()
                    # #             for x in lista if rex.search(x)]
                    splunk_feeder2 = SplunkFeedObject(config_data[1], "p")
                    finaldata = splunk_feeder2.eventPush(eventlist)

# --------------------------- first table attempt ------------------------------
# print(output_list2)
# header = output_list2[2:][0]
# values_list = list()
# cont = 0
# for values in output_list2[3:]:
#     values_list.insert(cont, values)
#     cont = cont + 1
# list2 = [header, values_list]
# print(list2)
# key = header.split("|")
# for value in values_list:
#     values = value.split("|")
#
# print(len(key))
# print(len(values))
# --------------------------- snmpwalk version 2 -------------------------------
#     elif version == "v2":
#         mibPath = config_data[1].get("mibPath", None)
#         hosts = config_data[1].get("hosts", None)
#         for host in hosts:
#             snmpV2cmd = "snmpwalk -{} -c {} {} -M {} -m ALL".format(version,
#                                                                     scvCommunity,
#                                                                     host,
#                                                                     mibPath)
#             try:
#                 output = subprocess.check_output(snmpV2cmd,
#                                                  stderr=subprocess.PIPE,
#                                                  shell=True).strip()
#             except:
#                 snmperror = "Timeout occur for {}".format(host)
#                 print(snmperror)
#                 writtingLog("warning {}".format(snmperror), logsdir)
#                 return 1
#             output_list = output.split("\n")
# do something
# for closing after error use return 1 instead of sys.exit()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt as k:
        print("Forced Exit")
