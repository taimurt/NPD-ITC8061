#This is a UDP based P2P Chat Application developed by Taimur Tufail, Tiziano Contaldo & Kristen Kivimaa

import hashlib, struct


class PacketTypes(object):
    CONTROL = bin(2) #b'00000010'
    DATA = bin(1) #b'00000001'
    AUTHENTICATION = bin(4) #b'00000100'
