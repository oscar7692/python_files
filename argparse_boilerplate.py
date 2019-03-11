#!/usr/bin/python

import argparse
import sys


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
    if margs is None: margs = sys.argv[1:]

    # Argument parsing in main scope (based on global's arguments)

    parsed_margs = argparse.ArgumentParser(
        parents=[parser], add_help=False).parse_args(margs)

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt as k:
        print("Forced Exit")
