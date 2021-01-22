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

Ice.loadSlice('IceGauntlet.ice')

import IceGauntlet
import getpass
    
class Client(Ice.Application):
    
    def run(self, argvs):
        try:
            proxyMapas = argvs[1]
        except IndexError:
            print("falta el proxy")
            return 1
        
        proxyMapas = self.communicator().stringToProxy(proxyMapas)  
        ''' room -> objeto remoto servidor RoomManager'''
        room = IceGauntlet.RoomManagerPrx.checkedCast(proxyMapas)

        opcion = int(input("opcion"))

        try:
            if opcion == 1:
                ''' upload new map'''
                mapName = input("map")
                token = input("token")    
                
                room.publish(token, mapName)
                return 0
            elif opcion == 2:
                ''' delete map'''
                roomName = input("roomName")
                token = input("token")    
                
                room.remove(token, roomName)
                return 0
        except OSError:
            print('ERROR: JSON file with user data not found!')


if __name__ == "__main__":
    app = Client()
    sys.exit(app.main(sys.argv))