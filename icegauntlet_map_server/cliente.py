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
            print("falta el proxy")
            return 1

        proxy = self.communicator().stringToProxy(proxy)  
        ''' room -> objeto remoto servidor RoomManager'''
        room = IceGauntlet.RoomManagerPrx.checkedCast(proxy)

        try:
            '''upload new map'''
            mapName = input("map")
            token = input("token")                    
            room.publish(token, mapName)
            return 0
        except OSError:
            print('ERROR: JSON file with user data not found!')

        try:
            ''' remove new map'''
            mapName = input("map")
            token = input("token")                    
            room.remove(token, mapName)
            return 0
        except OSError:
            print('ERROR: JSON file with user data not found!')




if __name__ == "__main__":
    app = Client()
    sys.exit(app.main(sys.argv))