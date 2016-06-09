import hashlib, struct


class NetworkPacket(object):

    def __init__(self, packet):
        self.data = packet.data
        self.sourceUUID = packet.sourceUUID  # sourceUUID
        self.destinationUUID = packet.destinationUUID  # destinationUUID;
        self.type = packet.type
        self.hopCount = packet.hopCount
        self.flags = packet.flags
        self.length = packet.length

    def pack(self):
        pck = struct.pack(">B", 0x01)
        pck += str(self.sourceUUID).encode()
        pck += str(self.destinationUUID).encode()
        pck += struct.pack(">B", int(self.type, 2))
        pck += struct.pack(">B", int(self.flags, 2))
        pck += struct.pack(">B", self.hopCount)
        pck += struct.pack(">B", self.length)
        if self.data != None:
            pck += str(self.data).encode()
        return pck