#This is a UDP based P2P Chat Application developed by Taimur Tufail, Tiziano Contaldo & Kristen Kivimaa

class User(object):
    def __init__(self, uuid, port):
        self.uuid=uuid
        self.port=port
