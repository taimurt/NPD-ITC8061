import queue, threading, datetime
import time

from p2p.Packet import Packet
from p2p.PacketTypes import PacketTypes
from p2p.Flag import Flag

class KeepAliveThread(threading.Thread):
    def __init__(self, p2p, isSend):
        self.p2p = p2p
        self.isSend = isSend
        threading.Thread.__init__(self)

    def stop(self):
        self.running = 0

    def run(self):
        self.running = 1
        if self.isSend:
            self.sendKeepAlive()
        else:
            self.checkKeepAlive()

    def sendKeepAlive(self):
            while self.running:
                time.sleep(5)
                print("I send keep alive")
                for row in self.p2p.neighborTable:
                    self.p2p.send(Packet(row['address'], self.p2p.uuid, row['dest'], PacketTypes.CONTROL, 1, Flag.KEEPALIVE, 0, None))
                    print("Keep alive send to + " + row['dest'])


    def checkKeepAlive(self):
        while self.running:
            time.sleep(1)
            for row in self.p2p.neighborTable:
                print(row)
                row['timer'] = row['timer']-1
                if(row['timer'] == 0 ):
                    self.p2p.neighborTable.remove(row)
                    for record in self.p2p.routingTable:
                        if(row['dest'] == record['via']):
                            self.p2p.routingTable.remove(record)

