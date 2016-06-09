#This is a UDP based P2P Chat Application developed by Taimur Tufail, Tiziano Contaldo & Kristen Kivimaa

from p2p.Handlers import *
from p2p.Peer import *
from p2p.Flag import *
from p2p.PacketTypes import *
import json

class AuthentificationHandler(Handler):
    def onEnable(self, p2p, chat):
        self.chat = chat
        self.p2p = p2p
        self.register(PacketTypes.AUTHENTICATION, self.onAuthentificationMessage)

    def onAuthentificationMessage(self, packet):
        print("Authentification Message received")
        if packet.flags == Flag.NO_AUTH:
            ip = packet.nextHop[0]
            port = packet.nextHop[1]
            self.p2p.neighborTable.append({'dest': packet.sourceUUID, 'address': (ip,port), 'timer':18})
            string_neighborTable = json.dumps(self.p2p.neighborTable)
            print("NeighborTable aggiornata: " + string_neighborTable)
            self.p2p.routingTable.append({'dest': packet.sourceUUID, 'via': packet.sourceUUID, 'cost': 1})
            string_routingTable = json.dumps(self.p2p.routingTable)
            print("RoutingTable aggiornata: " + string_routingTable)
            packet.destinationUUID = packet.sourceUUID
            packet.sourceUUID = self.p2p.uuid
            packet.flags = Flag.AUTH_SUCCESS
            self.p2p.send(packet)
        else:
            print("Conferma ricevuta")
            self.p2p.neighborTable.append({'dest': packet.sourceUUID, 'address': packet.nextHop, 'timer':18})
            string_neighborTable = json.dumps(self.p2p.neighborTable)
            print("NeighborTable aggiornata: " + string_neighborTable)
            self.p2p.routingTable.append({'dest': packet.sourceUUID, 'via': packet.sourceUUID, 'cost': 1})
            string_routingTable = json.dumps(self.p2p.routingTable)
            print("RoutingTable aggiornata: " + string_routingTable)

