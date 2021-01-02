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

<<<<<<< HEAD
from manage_topics import *

class RoomManagerI(IceGauntlet.RoomManager):
    '''room manager servant'''

    roomManager = None

=======
class RoomManagerI(IceGauntlet.RoomManager):
    '''room manager servant'''
>>>>>>> ae8d3d7da3b8188cbe424af783bb5e96bc0aa03f
    def __init__(self, auth, roomGestion):
        self._roomGestion = roomGestion
        self._auth_ = auth

<<<<<<< HEAD
=======
    def refresh(self, *args, **kwargs):
        '''Reload user DB to RAM'''
        self._roomGestion.refresh()

>>>>>>> ae8d3d7da3b8188cbe424af783bb5e96bc0aa03f
    def publish(self, token, roomData, current=None):
        '''Comprobar con el server de autenticacion si el token es valido'''      
        owner = self._auth_.getOwner(token)
        self._roomGestion.publish(owner, roomData)

    def remove(self, token, roomName, current=None):
        '''Comprobar con el server de autenticacion si el token es valido'''
        owner = self._auth_.getOwner(token)
        self._roomGestion.remove(owner, roomName)

<<<<<<< HEAD
    def availableRooms(self, current=None):
        '''Devuelve el nombre de todos los mapas disponibles'''

    def getRoom(self, roomName, current=None):
        '''Devuelve el room solicitado'''


class RoomManagerSyncI(IceGauntlet.RoomManagerSync):
    '''
    Room Manager event
    '''
    roomManager = None

    def hello(self, roomManager, managerId, current=None):
        if self.roomManager:
            self.roomManager.hello(roomManager, managerId)
            
    def announce(self, roomManager, managerId, current=None):
        if self.roomManager:
            self.roomManager.announce(roomManager, managerId)

    def newRoom(self, roomName, managerId, current=None):
        if self.roomManager:
            self.roomManager.añadir_room(roomName, managerId)

    def removedRoom(self, roomName, current=None):
        if self.roomManager:
            self.roomManager.eliminar_room(roomName)

class InitRoomManagers():
    ''' Manage RoomManager class '''

    def __init__(self, broker, auth, topic_room_manager):        
        '''Crear roomManager'''
        self.roomManagers_dict = {}
        self.topic_room_manager = topic_room_manager

        '''Instancia roomGestion'''
        roomGestion = RoomGestionI()

        logging.debug('Initializing server...')
        self.roomManager = RoomManagerI(auth, roomGestion)
        self.roomManager.roomManager = self

        self.adapter = broker.createObjectAdapter("RoomManagerAdapter")
        ident = broker.getProperties().getProperty("Identity")
        self.proxy = self.adapter.add(self.roomManager, broker.stringToIdentity(ident))
        self.proxy_room_manager = self.adapter.createDirectProxy(self.proxy.ice_getIdentity())
        print('"{}"'.format(self.proxy), flush=True)

        '''Crear room manager channel'''
        self.crear_roomManagerSync_channel()

        ''' Activar adapter y llamar hello event '''
        self.adapter.activate()
        self.publisher.hello(IceGauntlet.RoomManagerPrx.checkedCast(self.proxy_room_manager), self.roomManager.ice_toString())

    def crear_roomManagerSync_channel(self):
        ''' Crear room manager sync channel'''
        self.subscriptor = RoomManagerSyncI()
        self.subscriptor.roomManager = self
        self.proxy_event = self.adapter.addWithUUID(self.subscriptor)
        ident = self.proxy_event.ice_getIdentity()
        self.proxy_subscriptor = self.adapter.createDirectProxy(ident)
        self.topic_room_manager.subscribeAndGetPublisher({}, self.proxy_subscriptor)
        self.publisher = IceGauntlet.RoomManagerPrx.uncheckedCast(self.topic_room_manager.getPublisher())

    def hello(self, roomManager, managerId):
        ''' Hello a un room manager'''
        if roomManager.ice_toString() in self.roomManagers_dict:
            return
        print("Hi! soy %s" % roomManager.ice_toString())
        self.roomManagers_dict[roomManager.ice_toString()] = roomManager
        roomManager.announce(IceGauntlet.RoomManagerPrx.checkedCast(self.proxy_room_manager), roomManager.ice_toString())

    def announce(self, roomManager, managerId):
        ''' Announce room manager '''
        if roomManager.ice_toString() in self.roomManagers_dict:
            return
        print("Hi! yo soy %s" % roomManager.ice_toString())
        self.roomManagers_dict[roomManager.ice_toString()] = roomManager

    def añadir_room(self, roomName, managerId, current=None):
        '''Añadir room'''

    def eliminar_room(self, roomName, current=None):
        '''Eliminar room'''
    
=======
>>>>>>> ae8d3d7da3b8188cbe424af783bb5e96bc0aa03f
class Server(Ice.Application):
    '''
    Maps Server
    '''
    def run(self, args):
        proxyAuth = args[1]
<<<<<<< HEAD
=======
        
>>>>>>> ae8d3d7da3b8188cbe424af783bb5e96bc0aa03f
        proxyAuth = self.communicator().stringToProxy(proxyAuth)  
        ''' auth -> objeto remoto servidor Authentication'''
        auth = IceGauntlet.AuthenticationPrx.checkedCast(proxyAuth)

<<<<<<< HEAD
        broker = self.communicator()
        manage = ManageTopics(broker, "RoomManagerSyncChannel")
        topic_room_manager = manage.topic_room_manager
        roomManager = InitRoomManagers(broker, auth, topic_room_manager)
=======
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
>>>>>>> ae8d3d7da3b8188cbe424af783bb5e96bc0aa03f

        logging.debug('Entering server loop...')
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0


if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))
