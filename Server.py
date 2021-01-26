#!/usr/bin/python3 -u
# -- coding: utf-8 --

import sys
import Ice
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet
import os
from os import remove
import json
import random
import string
from random import choice


class RoomManagerIntarface(IceGauntlet.RoomManager):

	#Metodo que lee los datos inicialmente desde el fichero
	def cargarDatos(self,current=None):
		with open("roomDatos.json") as f:
			self.roomsDict = json.load(f)

		
	#Metodo que escribe los datos en el fichero
	def escribirDatos(self,current=None):
		file=open("roomDatos.json","w")
		file.write(json.dumps(self.roomsDict))
		file.close()

	def __init__(self,proxy):

		self.Authentication = IceGauntlet.AuthenticationPrx.checkedCast(proxy)
		self.roomsDict={}
		self.cargarDatos()
		
		

	def publish(self, token="",roomData="", current=None):
		#Comprobamos que el token introducido es valido
		if (self.Authentication.isValid(token) == False):
			raise IceGauntlet.Unauthorized()

		roomJson = json.loads(roomData)
		#Comprobamos si falta alguno de los dos campos necesesarios para ser considerado un mapa
		if( not ('data' in roomJson) or not ('room' in roomJson)):
			raise IceGauntlet.WrongRoomFormat()

		nombreReal=(""+roomJson['room'])

		if( (nombreReal) in self.roomsDict) and (self.roomsDict[''+nombreReal][0]!=token):
			raise IceGauntlet.RoomAlreadyExist()
		
		#generamos un nombre aleatorio y lo guardamos en la carpeta de mapas del servidor
		roomName=''.join([choice(string.ascii_letters) for i in range(8)])
		file = open("mapasServidor/"+roomName+".json","w")
		file.write(roomData)
		file.close()
	
		#guardamos los datos de la room publicada en el diccionario de rooms, con el siguiente orden: nombre Mapa Real,token del usuario que la ha subido, nombre aleatorio con el que se ha guardado
		self.roomsDict[""+nombreReal]=token,roomName
		self.escribirDatos()


	def remove(self, token="",roomName="", current=None):

		if(self.Authentication.isValid(token)==False):
			raise IceGauntlet.Unauthorized()

		if(not(roomName in self.roomsDict)):
			raise IceGauntlet.RoomNotExists()

		if(token != self.roomsDict[''+roomName] [0]):
			raise IceGauntlet.Unauthorized()

		remove("mapasServidor/"+self.roomsDict[''+roomName][1]+".json")
		self.roomsDict.pop(""+roomName)
		self.escribirDatos()

class DungeonInterface(IceGauntlet.Dungeon):

	def getRoom(self,current=None):
		#Si la lista que obtenemos no tiene longitud significa que no hay ningun mapa
		if len(os.listdir("./mapasServidor"))== 0:
			raise IceGauntlet.RoomNotExists()
		ruta="mapasServidor/"+random.choice(os.listdir("./mapasServidor"))
		file = open(ruta, "r")
		room = file.read()
		file.close()
		return room





class Server(Ice.Application):

	def run(self, argv):
			
		broker = self.communicator()
		adapter = broker.createObjectAdapter("MapAdapter1")
		RoomManagerServant = RoomManagerIntarface(self.communicator().stringToProxy(argv[1]))
		DungeonServant = DungeonInterface()
		proxy = adapter.add(RoomManagerServant, broker.stringToIdentity("servidorGestionMapas"))
		proxy2 = adapter.add(DungeonServant, broker.stringToIdentity("servidorMapas"))
		
		print(proxy, flush=True)
		file = open("dungeon_proxy.txt","w")
		file.write(str(proxy2))
		file.close()
		adapter.activate()
		self.shutdownOnInterrupt()
		broker.waitForShutdown()

		return 0


server = Server()
sys.exit(server.main(sys.argv))
