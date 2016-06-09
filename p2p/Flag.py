#This is a UDP based P2P Chat Application developed by Taimur Tufail, Tiziano Contaldo & Kristen Kivimaa

class Flag(object):
    ROUTINGUPDATE = bin(32) #b'00100000'
    SESSION = bin(16)#b'00010000'
    FILEDATA = bin(8)#b'00001000'
    TEXTMESSAGE = bin(4)#b'00000100'
    SEQUENCENUMBER = bin(2)#b'00000010'
    LASTFRAGMENT = bin(1)#b'00000001'
    SESSION = bin(64)#b'01000000'
    FILETRANSER = bin(32)#b'00100000'
    ROUTINGUPDATEINIT = bin(16)#b'00010000'
    KEEPALIVE = bin(8)#b'00001000'
    ACK = bin(4)#b'00000100'
    SEQUENCENUMBER = bin(2)#b'00000010'
    RST = bin(1)#b'00000001'
    AUTH_SUCCESS = bin(2)
    NO_AUTH = bin(1)
