#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pylint: disable=W1203
# pylint: disable=W0613

'''
   ICE Gauntlet Maps Server
'''

import sys
import json
import random
import signal
import string
import logging
import os.path
import os
import random

import Ice
Ice.loadSlice('IceGauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413
import IceGauntlet

from roomGestion import RoomGestionI

class RoomManagerI(IceGauntlet.RoomManager):
    '''room manager servant'''
    def __init__(self, auth, roomGestion):
        self._roomGestion = roomGestion
        self._auth_ = auth

    def refresh(self, *args, **kwargs):
        '''Reload user DB to RAM'''
        self._roomGestion.refresh()

    def publish(self, token, roomData, current=None):
        '''Comprobar con el server de autenticacion si el token es valido'''      
        owner = self._auth_.getOwner(token)
        self._roomGestion.publish(owner, roomData)

    def remove(self, token, roomName, current=None):
        '''Comprobar con el server de autenticacion si el token es valido'''
        owner = self._auth_.getOwner(token)
        self._roomGestion.remove(owner, roomName)

class Server(Ice.Application):
    '''
    Maps Server
    '''
    def run(self, args):
        proxyAuth = args[1]
        
        proxyAuth = self.communicator().stringToProxy(proxyAuth)  
        ''' auth -> objeto remoto servidor Authentication'''
        auth = IceGauntlet.AuthenticationPrx.checkedCast(proxyAuth)

        roomGestion = RoomGestionI()

        '''
        Server loop
        '''
        logging.debug('Initializing server...')
        servant = RoomManagerI(auth, roomGestion)
        signal.signal(signal.SIGUSR1, servant.refresh)

        adapter = self.communicator().createObjectAdapter('RoomManagerAdapter')
        proxy = adapter.add(servant, self.communicator().stringToIdentity('default'))
        adapter.addDefaultServant(servant, '')
        adapter.activate()
        logging.debug('Adapter ready, servant proxy: {}'.format(proxy))
        print('"{}"'.format(proxy), flush=True)

        logging.debug('Entering server loop...')
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0


if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))
