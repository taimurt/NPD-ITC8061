#This is a UDP based P2P Chat Application developed by Taimur Tufail, Tiziano Contaldo & Kristen Kivimaa

def enum(**enums):
	return type('Enum', (), enums)
	
Types = enum(
	VERIFYHANDLER = 1,
	MESSAGEHANDLER = 2
)

Types.ACKTYPE = b'00000100'
