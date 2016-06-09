#This is a UDP based P2P Chat Application developed by Taimur Tufail, Tiziano Contaldo & Kristen Kivimaa

from p2p import *
from gui.tk import TkGui
from Handlers.MessageHandler import *
from Handlers.ChatPeerHandler import *
from Handlers.ControlHandler import *
from Handlers.AuthentificationHandler import *

import sys

uuid = sys.argv[1]
if len(sys.argv[1]) != 4:
    print("Input no valid. UUID must be of 4 characters")
    exit (1)

port = int(sys.argv[2])

user = User(uuid,port)

p2p = P2P(user.port,user.uuid)
chat = TkGui(p2p,user.uuid)

MsgHandler = MessageHandler(p2p, chat)
p2p.addHandler(MsgHandler)

PeerHandler = ChatPeerHandler(p2p, chat)
p2p.addHandler(PeerHandler)

controlHandler = ControlHandler(p2p, chat)
p2p.addHandler(controlHandler)

authentificationHandler = AuthentificationHandler(p2p,chat)
p2p.addHandler(authentificationHandler)

p2p.startTimers()
chat.start()

