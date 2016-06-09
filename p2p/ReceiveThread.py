#This is a UDP based P2P Chat Application developed by Taimur Tufail, Tiziano Contaldo & Kristen Kivimaa

import socket, threading, struct, select
from p2p import *
from p2p.Packet import Packet
from p2p.PacketTypes import PacketTypes
from p2p.Flag import Flag
from p2p.Types import Types

class ReceiveThread(threading.Thread):
	def __init__(self, sock, p2p):
		self.sock = sock
		self.p2p = p2p
		
		threading.Thread.__init__(self)
    
	def stop(self):
		self.running = 0
    
	def run(self):
		self.running = 1
		while self.running:
			inputready,outputready,exceptready = select.select([self.sock],[],[])
			for sock in inputready:
				try:
					data, addr = sock.recvfrom(1024)
					#version = struct.unpack(">h", data[:2])
					version, = struct.unpack(">B", data[:1])
					#print("v: " + str(version))
					source_uuid = str(data[1:5], "UTF-8")
					#print("source: " + source_uuid)
					dest_uuid = str(data[5:9], "UTF-8")
					#print("dest: " + dest_uuid)
					type_p = bin(struct.unpack(">B",data[9:10])[0])
					#print("type: " + str(type_p))
					flag_p = bin(struct.unpack(">B",data[10:11])[0])
					#print("flag: " + str(flag_p) + ", KEEPALIVE: " + str(Flag.KEEPALIVE))
					hopCount, = struct.unpack(">B", data[11:12])
					#print("hopCount: " + str(hopCount))
					lenght, = struct.unpack(">B", data[12:13])
					#print("lenght: " + str(lenght))
					if type_p == PacketTypes.DATA:
						pkt_data = str(data[13:],"UTF-8")
						packet = Packet(self.p2p.getNextHop(dest_uuid), source_uuid, dest_uuid, type_p, hopCount, flag_p, len(data), pkt_data)
					elif type_p == PacketTypes.CONTROL:
						packet = Packet(self.p2p.getNextHop(dest_uuid), source_uuid, dest_uuid, type_p, hopCount, flag_p, len(data), None)
					elif type_p == PacketTypes.AUTHENTICATION:
						packet = Packet(addr,source_uuid, dest_uuid,type_p, hopCount, flag_p, len(data), None)
					self.p2p.handle(packet)
				except:
					print("Errore connessinoe")
					break
				'''''
				packet = Packet(addr, handlerId, pkt_data)
				
				if packet.handlerId != Types.VERIFYHANDLER:
					self.p2p.send(Packet(addr, Types.VERIFYHANDLER, packet.hash))
                
				self.p2p.handle(packet)
				'''''
				
				

		
	


