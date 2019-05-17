# -*- coding: utf-8 -*-
"""
Created on Mon May 6 2019

@author: oscar pulido

@title: py-passwd
"""

import argparse
from getpass import getpass, getuser
import json
from os import remove
import pyAesCrypt
import sys


parser = argparse.ArgumentParser()

parser.add_argument("-u", "--user", help="username will be store",
                    type=str, default=None)
parser.add_argument("-p", "--password", help="password will be store",
                    type=str, default=None)
parser.add_argument("-f", "--file", help="filename", type=str, 
                    default=None)
parser.add_argument("-fm", "--filemode", 
                    help="in what mode file will be open r --> read,"\
                        "w --> write", type=str, default=None)
parser.add_argument("-bs", "--bufferSize", help="set a custom value for"\
                    " buffer size or leave in blanc to use default value",
                    type=int, default=65536)

parsed_args = parser.parse_args()


def encryptfile(filename, password, bufferSize):
    filename = filename
    password = password
    bufferSize = bufferSize
    try:
        pyAesCrypt.encryptFile(filename, "{}.aes".format(filename), 
                                password, bufferSize)
        remove(filename)
        print("{} has been encrypted".format(filename))
    except IOError as file_error:
        print("file error please validate \n {}".format(file_error))

def decryptfile(filename, password, bufferSize):
    filename = filename
    password = password
    fileout = filename[:-4]
    bufferSize = bufferSize
    try:
        pyAesCrypt.decryptFile(filename, fileout, password, bufferSize)
        remove(filename)
        print("{} has been decrypted as {}".format(filename, fileout))
    except IOError as file_error:
        print("file error please validate \n {}".format(file_error))

def read_vault(filename, filemode):
    filename = filename
    filemode = filemode
    print("read mode")
    if filemode == "r":
        try:
            with open(filename, filemode) as vault:
                scvault = json.load(vault)
                print(json.dumps(scvault, indent=4, sort_keys=True))
        except IOError as vaulterror:
            print("file error please validate \n {}".format(vaulterror))

def user_val(username):
    username = username
    rb_user = str(getuser())
    if rb_user == username:
        pass
    else:
        sys.exit()

# def vault(filename, filemode):
#     filename = filename
#     filemode = filemode
#     if filemode == 'w':
#         with open(filename, filemode) as secvault:
#             json.load(secvault)
#         print("write mode")
#     else:
#         print("use a valid option as :"\
#             "r for read, w to write")

# --------------------------- main definition ----------------------------------
def main(margs=None):
    if margs is None: margs = sys.argv[1:]
    parsed_margs = argparse.ArgumentParser(parents=[parser],
                                            add_help=False).parse_args(margs)
    username = parsed_margs.user
    password = parsed_margs.password
    filename = parsed_margs.file
    filemode = parsed_margs.filemode
    bufferSize = parsed_margs.bufferSize

    user_val(username)
    try:
        if ".aes" in filename:
            decryptfile(filename,password,bufferSize)
            print("file decrypted")
        else:
            encryptfile(filename,password,bufferSize)
            print("file encrypted")
    except IOError as err:
        print(err)
    if filemode is None:
        sys.exit()
    elif filemode is "r":
        read_vault(filename, filemode)
    elif filemode is "w":
        pass
    else:
        print("use a valid option as :"\
            "r for read, w to write")




if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt as k:
        print("Forced Exit")
