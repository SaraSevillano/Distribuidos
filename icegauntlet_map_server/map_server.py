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


import Ice
Ice.loadSlice('icegauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413
import IceGauntlet

ROOMS_FILE = 'rooms.json'
CURRENT_TOKEN = 'current_token'


class RoomManagerI(IceGauntlet.RoomManager):
    '''room manager servant'''
    def __init__(self):
        self._rooms_ = {}
        if os.path.exists(ROOMS_FILE):
            self.refresh()
        else:
            self.__commit__()

    def refresh(self, *args, **kwargs):
        '''Reload user DB to RAM'''
        logging.debug('Reloading rooms database')
        with open(ROOMS_FILE, 'r') as contents:
            self._rooms_ = json.load(contents)

    def __commit__(self):
        logging.debug('Rooms database updated!')
        with open(ROOMS_FILE, 'w') as contents:
            json.dump(self._rooms_, contents, indent=4, sort_keys=True)

    def publish(self, token, roomData, current=None):
        '''Publish new map'''
        with open(roomData, 'r') as contents:
            newRoom = json.load(contents)
        t = {"token": token}
        newRoom.update(t)
        if roomData in self._rooms_ and self._rooms_[roomData]["token"] != token:
            '''lanzar exception RoomAlreadyExists y borrar print'''
            print("room already exists y es de otro usuario")
            return 1
        '''Añadir el resto de condiciones con las excepciones correspondientes'''
        self._rooms_[roomData] = newRoom
        self.__commit__()

    '''def remove(self, token, roomData, current=None):'''
    


class Server(Ice.Application):
    '''
    Maps Server
    '''
    def run(self, args):
        '''
        Server loop
        '''
        logging.debug('Initializing server...')
        servant = RoomManagerI()
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
