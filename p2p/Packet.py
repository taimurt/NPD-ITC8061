#This is a UDP based P2P Chat Application developed by Taimur Tufail, Tiziano Contaldo & Kristen Kivimaa

import hashlib, struct
from p2p.Flag import *
from p2p.PacketTypes import *

class Packet(object):
	def __init__(self, nextHop, source, destination, type,hopCount,flags,length, data):
		self.nextHop = nextHop
		self.type = type
		self.data = data
		self.sourceUUID = source  # sourceUUID
		self.destinationUUID = destination  # destinationUUID;
		self.type = type
		self.hopCount = hopCount
		self.flags = flags
		self.length = length
		

	def pack(self):
		pck = struct.pack(">B",0x01)
		pck += str(self.sourceUUID).encode()
		pck += str(self.destinationUUID).encode()
		pck += struct.pack(">B", int(self.type,2))
		pck += struct.pack(">B", int(self.flags,2))
		pck += struct.pack(">B", self.hopCount)
		pck += struct.pack(">B", self.length)
		pck += str(self.data).encode()
		print(pck)

		print("Sending Packet: \n" + str(pck))
		return  pck

	def changeInAck(self, nextHop):
		self.type = PacketTypes.CONTROL
		self.flags = Flag.ACK
		self.hopCount = 15
		self.data = None
		tmp = self.destinationUUID
		self.destinationUUID = self.sourceUUID
		self.sourceUUID = tmp
		self.nextHop = nextHop
