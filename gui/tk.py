#This is a UDP based P2P Chat Application developed by Taimur Tufail, Tiziano Contaldo & Kristen Kivimaa

import sys
from tkinter import *
from tkinter import ttk
from p2p import *
import errno
import json

class TkGui(Tk):
    def __init__(self, p2p, nickname):
        Tk.__init__(self)
        self.p2p = p2p
        self.peers = {}
        self.nickname = nickname
        
    def start(self):
        self.title("Network Chat Application: " + self.nickname)
        
        menubar = Menu(self)
        self.config(menu=menubar)

        filemenu = Menu(menubar)
        peers = Menu(menubar)

        filemenu.add_command(label="Add peer", command=self.addPeer)
        filemenu.add_command(label="Show Routing Table", command=self.showRoutingTable)
        filemenu.add_command(label="Show Users", command=self.showUser)

        menubar.add_cascade(label="Commands", menu=filemenu)




        self.resizable(width=FALSE, height=FALSE)
        
        mainframe = ttk.Frame(self)
        mainframe.grid(column=0, row=0)
        mainframe.grid_columnconfigure(0, weight=1)
        mainframe.grid_rowconfigure(0, weight=1)

        self.chat = Text(mainframe, width=50, state="disabled")
        
        self.chat.tag_configure('answer', foreground='red', font=('Verdana', 10))
        self.chat.tag_configure('normal', foreground='blue', font=('Verdana', 10, 'italic'))
        self.chat.tag_configure('error', foreground='red', font=('Verdana', 10) )
        self.chat.tag_configure('showing', foreground="black" )
         
        self.chat.grid(column=0, row=0, columnspan=2, sticky=(N,E,W,S))
       
        self.scroll = ttk.Scrollbar(mainframe, orient=VERTICAL, command=self.chat.yview)
        self.scroll.grid(column=2, row=0, sticky=(N,S))
        
        self.chat.configure(yscrollcommand=self.scroll.set)
        
        self.eingabe = ttk.Entry(mainframe)
        self.eingabe.grid(column=0, row=1, sticky=(W,E))
        self.eingabe.bind('<Return>', self.send)
        
        self.btn_send = ttk.Button(mainframe, text='Send', command=self.send)
        self.bind('<Destroy>', self.shutdown)
        
        self.btn_send.grid(column=1, row=1, columnspan=2)
        
        self.mainloop()
        
    def addMessage(self, name, msg):
        self.addText("{0}: {1}".format(name, msg), "answer")

    def showRoutingTable(self):
        #string_routingTable = json.dumps(self.p2p.routingTable)
        self.addText(" dest    via    cost","error")
        for i in self.p2p.routingTable:
            self.addText(i['dest'] + "  " + i['via'] +"  "+ str(i['cost']),"showing")

    def showUser(self):
        for i in self.p2p.routingTable:
            self.addText(i['dest'])

    def addPeer(self):
        self.peerdialog = Toplevel(self)
        self.peerdialog.title("Add a Neighbor: Enter Address: (ip:port)")
        self.peerdialog.resizable(width=FALSE, height=FALSE)  
        self.peeraddr = ttk.Entry(self.peerdialog, width=30)
        self.peeraddr.grid(column=0, row=0, sticky=(W, E))
        ttk.Button(self.peerdialog, text='Add', command=self.addPeerAction).grid(column=1, row=0, sticky=(W, E))
        

    def addPeerAction(self):
        # uuid = self.peeraddr.get()
        addr_port = self.peeraddr.get();
        if ":" not in addr_port:
            self.addText("Formato non corretto","error")
        addr_port_t = addr_port.split(":")
        print("addr: " + addr_port_t[0] + ", port: " + addr_port_t[1])
        packet = Packet((addr_port_t[0],int(addr_port_t[1])),self.p2p.uuid,"FFFF",PacketTypes.AUTHENTICATION,15,Flag.NO_AUTH,0,None)
        self.p2p.send(packet)
        Packet.pack(packet) #function that let me to see in the console the packet sent
        self.peerdialog.destroy()


    def send(self, *args):
        if ">" not in self.eingabe.get():
            self.addText("INVALID FORMAT")
            return
        self.addText("You: {0}".format(self.eingabe.get()))
        vect = self.eingabe.get().split('>')
        text = vect[0]; dest = vect[1]
        #if(dest != self.p2p.uuid):
        if dest == "ALL":
            for i in self.p2p.routingTable:
                if i['dest'] != self.p2p.uuid:
                    #print(i['dest'])
                    self.p2p.sendText(i['dest'], text)
        else:
            try:
                self.p2p.sendText(dest,text)
            except:
                self.addText("The peer doesn't exist or he is not reachablle", "error")


        # eingabe = self.eingabe.get()
        #
        # for peer_id in self.peers:
        #     peer = self.peers[peer_id]
        #     packet = p2p.Packet(peer.address, p2p.Types.MESSAGEHANDLER, "{0}:{1}".format(self.nickname,eingabe))
        #     self.p2p.send(packet)
        # self.eingabe.delete(0, END)
        
    def addText(self, text, tag = 'normal'):
        self.chat.configure(state="normal")
        self.chat.insert(END, text + "\n", tag)
        self.chat.configure(state="disabled")
        
    def shutdown(self, *args):
        self.p2p.close()
        self.destroy()
        sys.exit(0)

