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
            proxyMapas = argvs[1]
            proxyAuth = argvs[2]
        except IndexError:
            print("falta alguno de los proxy")
            return 1

        proxyMapas = self.communicator().stringToProxy(proxyMapas)  
        proxyAuth = self.communicator().stringToProxy(proxyAuth)  
        ''' room -> objeto remoto servidor RoomManager'''
        room = IceGauntlet.RoomManagerPrx.checkedCast(proxyMapas)

        ''' auth -> objeto remoto servidor Authentication'''
        auth = IceGauntlet.AuthenticationPrx.checkedCast(proxyAuth)

        opcion = int(input("opcion"))

        try:
            if opcion == 1:
                ''' upload new map'''
                mapName = input("map")
                token = input("token")    
                '''Comprobar con el server de autenticacion si el token es valido'''
                if not auth.isValid(token):
                    raise IceGauntlet.Unauthorized()
                    return 1
                room.publish(token, mapName)
                return 0
            elif opcion == 2:
                ''' delete map'''
                roomName = input("roomName")
                token = input("token")    
                '''Comprobar con el server de autenticacion si el token es valido'''
                if not auth.isValid(token):
                    raise IceGauntlet.Unauthorized()
                    return 1
                room.remove(token, roomName)
                return 0
        except OSError:
            print('ERROR: JSON file with user data not found!')


if __name__ == "__main__":
    app = Client()
    sys.exit(app.main(sys.argv))