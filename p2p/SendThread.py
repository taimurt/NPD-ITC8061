#This is a UDP based P2P Chat Application developed by Taimur Tufail, Tiziano Contaldo & Kristen Kivimaa

import socket, queue, threading, datetime
#from p2p.Packet import Packet
#from p2p.Types import Types
from p2p import *
from p2p.NetworkPacket import NetworkPacket

class SendThread(threading.Thread):
	def __init__(self, socket, send_queue, out_queue, data_out):
		self.socket = socket
		self.send_queue = send_queue
		self.out_queue = out_queue
		self.data_out = data_out
		
		threading.Thread.__init__(self)
		
	def stop(self):
		self.running = 0
		
	def run(self):
		self.running = 1
		while self.running:
			packet = self.send_queue.get(True)
			networkPacket = NetworkPacket(packet)
			try:
				self.socket.sendto(networkPacket.pack(), packet.nextHop)
			except:
				print("Error")



		
		
		
