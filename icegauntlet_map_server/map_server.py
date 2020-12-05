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
Ice.loadSlice('icegauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413
import IceGauntlet

DIRECTORY_MAPS = 'mapas'
ROOMS_PATH = 'mapas/rooms.json'

def id_generator(size=6, chars= string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class RoomManagerI(IceGauntlet.RoomManager):
    '''room manager servant'''
    def __init__(self):
        self._rooms_ = {}
        if os.path.exists(ROOMS_PATH):
            self.refresh()
        else:
            self.__commit__()

    def refresh(self, *args, **kwargs):
        '''Reload user DB to RAM'''
        logging.debug('Reloading rooms database')
        with open(ROOMS_PATH, 'r') as contents:
            self._rooms_ = json.load(contents)

    def __commit__(self):
        logging.debug('Rooms database updated!')
        if not os.path.isdir(DIRECTORY_MAPS):
            os.mkdir(DIRECTORY_MAPS)
        with open(ROOMS_PATH, 'w') as contents:
            json.dump(self._rooms_, contents, indent=4, sort_keys=True)

    def publish(self, token, roomData, current=None):
        '''Publish new map'''
        with open(roomData, 'r') as contents:
            newRoom = json.load(contents)

        roomName = newRoom["room"]
        mapFile = ''

        '''RoomAlreadyExists'''
        if roomName in self._rooms_:
            '''Ese mapa pertence a otro usuario'''
            if self._rooms_[roomName]["token"] != token:
                raise IceGauntlet.RoomAlreadyExists()
                return 1
            '''Actualiza el contenido del mapa existente'''
            mapFile = self._rooms_[roomName]["file"]
            with open(DIRECTORY_MAPS + '/' + mapFile, 'w') as contents:
                json.dump(newRoom, contents, indent=4, sort_keys=True)
            return 0
        
        '''Actualizar rooms.json con el nuevo mapa, el token  y el json asociado'''
        mapFile = id_generator() + '.json'
        self._rooms_[roomName] = {"token": token, "file": mapFile}
        self.__commit__()

        '''Añadir nuevo json del mapa a la carpeta mapas del servidor'''
        with open(DIRECTORY_MAPS + '/' + mapFile, 'w') as contents:
            json.dump(newRoom, contents, indent=4, sort_keys=True)

    def remove(self, token, roomName, current=None):
        '''Remove mapa'''
        '''RoomAlreadyExists'''
        if roomName in self._rooms_:
            '''Ese mapa pertence a otro usuario'''
            if self._rooms_[roomName]["token"] != token:
                raise IceGauntlet.Unauthorized()
                return 1
            '''Borrar mapa'''
            mapFile = self._rooms_[roomName]["file"]
            self._rooms_.pop(roomName)
            with open(ROOMS_PATH, 'w') as contents:
                json.dump(self._rooms_, contents, indent=4, sort_keys=True)
            if os.path.exists(DIRECTORY_MAPS + '/' + mapFile):
                os.remove(DIRECTORY_MAPS + '/' + mapFile)
            return 0
        
        '''EL room no existe'''
        raise IceGauntlet.RoomNotExists()
        return 1
        

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
