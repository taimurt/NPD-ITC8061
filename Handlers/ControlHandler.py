#This is a UDP based P2P Chat Application developed by Taimur Tufail, Tiziano Contaldo & Kristen Kivimaa

from p2p.Handlers import *
from p2p.Peer import *
from p2p.Flag import *
from p2p.PacketTypes import *

class ControlHandler(Handler):
    def onEnable(self, p2p, chat):
        self.chat = chat
        self.p2p = p2p
        self.register(PacketTypes.CONTROL, self.onControlMessage)

    def onControlMessage(self, packet):
        if packet.destinationUUID == self.p2p.uuid:
            if packet.flags == Flag.KEEPALIVE:
                print("I have received a keep alive from:  " + packet.sourceUUID)
                for row in self.p2p.neighborTable:
                    if(row['dest'] == packet.sourceUUID):
                        row['timer'] = 18
            elif packet.flags == Flag.ACK:
                #TODO ACK handler
                return
        else:
            if packet.flags == Flag.ACK:
                packet.hopCount -= 1
                packet.nextHop = self.p2p.getNextHop(packet.destinationUUID)
