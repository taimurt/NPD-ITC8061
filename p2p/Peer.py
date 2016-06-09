#This is a UDP based P2P Chat Application developed by Taimur Tufail, Tiziano Contaldo & Kristen Kivimaa

class Peer(object):
    def __init__(self, addr,  id):
        self.address = addr
        self.id = id
