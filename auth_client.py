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

Ice.loadSlice('IceGauntlet.ice')

import IceGauntlet
import getpass


class Client(Ice.Application):
    
    def run(self, argvs):
        try:
            proxy = argvs[1]
        except:
            print('Command arguments: {} <proxy autenticacion>')
            return 1

        proxy = self.communicator().stringToProxy(proxy)  
        ''' auth -> objeto remoto servidor autenticacion'''
        auth = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        '''hashlib.SHA256(password)'''

        try:
            ''' 1.3.2 change password'''

            '''hashlib.sha256(password)'''
            
            user = input("Introduce el user: ")
            password = getpass.getpass("Introduce password: ")
            new_password = getpass.getpass("Introduce new password: ")
            
            hashsha = hashlib.sha256 ()
            hashsha.update(password.encode())

            hashsha2 = hashlib.sha256 ()
            hashsha2.update(new_password.encode())

            auth.changePassword(user, hashsha.hexdigest(), hashsha2.hexdigest())

            return 0               
        except OSError:
            print('ERROR: JSON file with user data not found!')

            
if __name__ == "__main__":
    app = Client()
    sys.exit(app.main(sys.argv))