from multiprocessing import Queue
import socket
from p2p import *
import json
from gui import *

import random
from p2p.KeepAliveThread import KeepAliveThread
from p2p.SendRoutingTableThread import SendRoutingTableThread

from threading import Thread
import time

class P2P(object):
	def __init__(self, port=1234, uuid=""):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('',port))

		self.uuid = uuid

		self.neighborTable = [] # [ {'dest': <uuid_neighbor0>, 'ipaddress': <ipaddress_neightbor0>}, {...} ]
		self.routingTable = [] # [ {'dest': <uuid_dest0>, 'via':<uuid_nexthop>}, {...} ]
		self.aliveTable = {}  # { 'uuid0' : <is_alive>, 'uuid1': <is_alive>, ... }
		ip="127.0.0.1"
		port=1111

		#I KNOW FROM THE BEGGING HOW TO REACH MYSELF
		self.routingTable.append({'dest' : self.uuid, 'via' : self.uuid, 'cost' : 0})
		self.handler = []
		self.packetHandler = {}		#{0x01:[callback1,callback2],0x04:[callback4],0x08:[callback1,callback4]}

		self.send_queue = queue.Queue()
		self.out_queue = queue.Queue()
		self.data_out = []

		self.receiveThread = ReceiveThread(self.sock, self)
		self.sendThread = SendThread(self.sock, self.send_queue, self.out_queue, self.data_out)
		self.watchThread = WatchThread(self.out_queue, self.send_queue, self.data_out)
		self.sendKeepAlive = KeepAliveThread(self, True)
		self.checkKeepAlive = KeepAliveThread(self, False)
		self.sendRoutingTable = SendRoutingTableThread(self)
		self.receiveThread.start()
		self.sendThread.start()
		self.watchThread.start()
		self.addHandler(VerifyHandler(self))

	def stop(self):
		self.receiveThread.stop()
		self.sendThread.stop()
		self.watchThread.stop()
		self.checkKeepAlive.stop()
		self.sendKeepAlive.stop()
		self.sendRoutingTable.stop()

	
	def close(self):
		self.stop()
	
	def __del__(self):
		self.stop()
	
	def addHandler(self, handler):
		self.handler.append(handler)

	def handle(self, packet):
		if packet.type in self.packetHandler:
			for callback in self.packetHandler[packet.type]:
				callback(packet)
	
	def send(self, packet):
		self.sock.sendto(Packet.pack(packet),packet.nextHop)

	def getNextHop(self, uuid):
		via = None
		for info_routing in self.routingTable:
			if info_routing['dest'] == uuid:
				via = info_routing['via']
				break
		if via == None : return None
		nextHop = None
		for info_neighbor in self.neighborTable:
			if info_neighbor['dest'] == via:
				nextHop = info_neighbor['address']
				break
		return nextHop

	def updateRoutingTable(self, packet):

		routingTableReceived = json.loads(packet.data)

		for other_row in routingTableReceived:
			if other_row['dest'] not in [r['dest'] for r in self.routingTable]:
				if other_row['via'] != self.uuid:
					self.routingTable.append({'dest' : other_row['dest'], 'via' : packet.sourceUUID, 'cost': other_row['cost'] + 1 })
			else:
				for my_row in self.routingTable:
					if my_row['dest'] == other_row['dest']:
						if other_row['cost'] + 1 < my_row['cost']:
							my_row['cost'] = other_row['cost'] + 1
							my_row['via'] = packet.sourceUUID
		for row in self.routingTable:
			if row['dest'] not in [r['dest'] for r in routingTableReceived ]:
				if row['via'] == packet.sourceUUID:
					self.routingTable.remove(row)


	def startTimers(self):
		self.checkKeepAlive.start()
		self.sendKeepAlive.start()
		self.sendRoutingTable.start()


	def addPeer(self, uuid, ip, port):
		self.neighborTable.append({'dest':uuid, 'address': (ip, port)})
		if uuid not in [r['dest'] for r in self.routingTable]:
			self.routingTable.append({'dest' :  uuid , 'via' : uuid, 'cost' : 1})
		else:
			for my_row in self.routingTable:
				if my_row['dest'] == uuid:
					my_row['cost'] = 1
					my_row['via'] = uuid

		self.aliveTable[uuid] = False


	def sendText(self, dest, text):
		packet = Packet(self.getNextHop(dest),self.uuid,dest,PacketTypes.DATA,15,Flag.TEXTMESSAGE, 90, text)
		self.send(packet)