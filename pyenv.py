#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import time
import traceback


__author__ = "oscar pulido"

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name",
                    help="name of virtual environment",
                    type=str, default="virtual_env")
parser.add_argument("-l", "--list",
                    help="list of packages to install in virtual"
                    " environment separated by , "
                    "for example module1,module2,module3,.......",
                    type=str, default=None)
parser.add_argument("-d", "--directory",
                    help="dir where venv will be created, put the directory "
                    "from your actual path to where venv will be created",
                    type=str, default=None)
parser.add_argument("-r", "--requirements",
                    help="file that contain the modules to install is "
                    "recomenden call it requirements.txt, but feel free to "
                    "call it whatever you want",
                    type=str, default=None)


def main(margs=None):
    if margs is None:
        margs = sys.argv[1:]
    parsed_margs = argparse.ArgumentParser(parents=[parser],
                                           add_help=False).parse_args(margs)
    pymods = parsed_margs.list
    venvname = parsed_margs.name
    venvdir = parsed_margs.directory
    reqfile = parsed_margs.requirements
    spacecmd = "echo -e '\n'"
    if parsed_margs.requirements is None:
        os.chdir(venvdir)
        try:
            modl.switch(py27,py34)
            print("\nmodule ", py27, "to", py34,"\n")
        except Exception as e:
            print(e)
            traceback.print_exc()
        time.sleep(5)
        modl.load("python/msdlenv/qa")
        time.sleep(5)
        msvenv = "msvenv {}\n".format(venvname)
        os.system(msvenv)
        print("venv {} was created\n".format(venvname))
        time.sleep(3)
        if parsed_margs.list is not None:
            module_inst = "{}_modules_installer.sh".format(venvname)
            os.system("touch {}".format(module_inst))
            os.system("echo 'source {}/bin/activate' >>"
                      " {}".format(venvname, module_inst))
            pymods = parsed_margs.list.split(',')
            for pymod in pymods:
                os.system("echo 'msdlpkg install {}' >> "
                          "{}".format(pymod, module_inst))
                os.system("echo {} >> {}".format(spacecmd,module_inst))
            os.system("chmod 764 {}".format(module_inst))
            os.system(module_inst)
        else:
            print("/n no modules provided venv {} successfully "
                  "created".format(venvname))
    else:
        os.chdir(venvdir)
        try:
            modl.switch(py27,py34)
            print("\nmodule ", py27, "to", py34,"\n")
        except Exception as e:
            print(e)
            traceback.print_exc()
        time.sleep(5)
        modl.load("python/msdlenv/qa")
        time.sleep(3)
        module_inst = "{}_modules_installer.sh".format(venvname)
        with open(reqfile, 'r') as modfile:
            newmods = modfile.read()
        newmods = newmods.split()
        for newmod in newmods:
            os.system("echo 'msdlpkg install {}' >> "
                      "{}".format(newmod, module_inst))
            os.system("echo {} >> {}".format(spacecmd,module_inst))
        os.system("*_modules_installer.sh")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt as k:
        print("Forced Exit by user")
