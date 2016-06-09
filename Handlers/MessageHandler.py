#This is a UDP based P2P Chat Application developed by Taimur Tufail, Tiziano Contaldo & Kristen Kivimaa

#from p2p.Handlers.Handler import Handler
from p2p.Handlers import *
from p2p.Flag import *
from p2p.PacketTypes import *

class MessageHandler(Handler):
    def onEnable(self, p2p, chat):
        self.p2p = p2p
        self.chat = chat
        self.register(PacketTypes.DATA,self.onMessage)

    def onMessage(self, packet):
        print("I HAVE RECEIVED A DATA MASSAGE")
        if packet.destinationUUID == self.p2p.uuid:
            print("I AM THE RECEIVER")
            if packet.flags == Flag.ROUTINGUPDATE:
                print("IT IS A ROUTING UPDATE")
                self.p2p.updateRoutingTable(packet)
            elif packet.flags == Flag.TEXTMESSAGE:
                print("IT IS TEXTMESSAGE")
                self.chat.addMessage('<' + packet.sourceUUID + '> ', packet.data)
        else:
            print("I AM NOT THE RECEIVER")
            packet.nextHop = self.p2p.getNextHop(packet.destinationUUID)
            packet.hopCount -= 1
            self.p2p.send(packet)

