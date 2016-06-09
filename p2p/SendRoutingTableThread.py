#This is a UDP based P2P Chat Application developed by Taimur Tufail, Tiziano Contaldo & Kristen Kivimaa

import queue, threading, datetime
import time

from p2p.Packet import Packet
from p2p.PacketTypes import PacketTypes
from p2p.Flag import Flag
import json

class SendRoutingTableThread(threading.Thread):
    def __init__(self, p2p):
        self.p2p = p2p
        threading.Thread.__init__(self)

    def stop(self):
        self.running = 0

    def run(self):
        self.running = 1
        self.sendRoutingTable()

    def sendRoutingTable(self):
            while self.running:
                time.sleep(10) # 30
                string_routingTable = json.dumps(self.p2p.routingTable)
                for row in self.p2p.neighborTable:
                    print("I SEND ROUTING TABLE PACKET TO " + row['dest'] + "\n  " + string_routingTable)
                    nextHop = self.p2p.getNextHop(row['dest'])
                    self.p2p.send(Packet(nextHop, self.p2p.uuid, row['dest'], PacketTypes.DATA, 15, Flag.ROUTINGUPDATE, len(string_routingTable),string_routingTable))

