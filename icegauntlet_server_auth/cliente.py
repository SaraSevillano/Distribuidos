#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

'''
Cliente
'''

import os
import sys
import json
import signal

import psutil


import hashlib
import sys
import Ice

Ice.loadSlice('icegauntlet.ice')

import IceGauntlet
import getpass


class Client(Ice.Application):
    
    def run(self, argvs):
        try:
            proxy = argvs[1]
        except IndexError:
            print('Command arguments: {} <proxy autenticacion>')
            return 1

        proxy = self.communicator().stringToProxy(proxy)  
        ''' auth -> objeto remoto servidor autenticacion'''
        auth = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        '''hashlib.SHA256(password)'''

        opcion = int(input("opcion"))
        try:
            if opcion == 1:
                ''' 1.3.2 change password'''

                '''hashlib.sha256(password)'''

                user = input("user")
                password = getpass.getpass("password1")
                new_password = getpass.getpass("password2")
            
                hashsha = hashlib.sha256 ()
                hashsha.update(password.encode())

                hashsha2 = hashlib.sha256 ()
                hashsha2.update(new_password.encode())

                auth.changePassword(user, hashsha.hexdigest(), hashsha2.hexdigest())

                return 0
            elif opcion == 2:
                ''' 1.3.1. get new token'''
                user = input("user")
                password = getpass.getpass("password")  

                hashsha = hashlib.sha256 ()
                hashsha.update(password.encode())

                token = auth.getNewToken(user, hashsha.hexdigest())
                print(token)
                return 0               
        except OSError:
            print('ERROR: JSON file with user data not found!')

            
if __name__ == "__main__":
    app = Client()
    sys.exit(app.main(sys.argv))