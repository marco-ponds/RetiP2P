import socket
import random
import threading

context = dict()

class PeerServer(threading.Thread):

	def __init__ (self, address, port):

		threading.Thread.__init__(self)
		self.address = address
		self.port = int(port)
		print("PEER ADDRESS "+ self.address + ":" + str(self.port))

	def startServer ( self ):
		##launching peer server
		pass
	
	def run(self):
		self.socket = socket.socket(socket.AF_INET6 , socket.SOCK_STREAM)
		self.server_address = ( self.address , int(self.port))
		self.socket.bind(self.server_address)
		self.socket.listen(1)
		while True:
			print(".")
			socketclient, address = self.socket.accept()
			print("CONNESSIONE AVVENUTA")
			msg_type = socketclient.recv(4)
			print("MSG TYPE " + msg_type)
				

class PeerClient(object):

	## azioni ammesse dal peer
	## login
	## logout
	## storage ( key, value )
	def __init__(self , ip_p2p , ip_dir="none" , porta_dir="none"):
		##we should retrieve our ipv6 address and create a new port
		##print([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]])
		##self.ip_p2p = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]][0]
		self.ip_p2p = ip_p2p
		self.port = str(random.randint(8000,9000))
		##we obtained a new port between 8000 and 9000
		print(self.ip_p2p +":"+self.port)

		if ip_dir == "none" and porta_dir == "none":
			print("non hai inserito l'indirizzo della directory")
		else: 
			self.ip_dir = ip_dir
			self.porta_dir = int(porta_dir)	
			self.directory = (self.ip_dir , int(self.porta_dir))

		
		##check if our addresses are in ipv6 format	
		if not (self.checkIPV6Format(self.ip_p2p)):
			print("indirizzo non corretto")	
			return

		self.peer_server = PeerServer(self.ip_p2p , self.port)
		self.peer_server.start()


	def login(self):
		self.connection_socket = socket.socket(socket.AF_INET6 , socket.SOCK_STREAM)
 		self.connection_socket.connect(self.directory)
 		##mandiamo il messaggio di login
 		message = "LOGI"+str(self.ip_p2p)+str(self.port)
 		
 		print(message)
 		self.connection_socket.send(message)

 		message_type = self.connection_socket.recv(4)
 		session_id = self.connection_socket.recv(16)

 		print("TYPE " + message_type)
 		print("SESSION ID "+session_id)

		receivedLogin( session_id )


	def checkIPV6Format(self, address):
		try:
			socket.inet_pton(socket.AF_INET6, address)
			return True
		except:
			return False


def receivedLogin( sessionId ):
	context['sessionid'] = sessionId
	print(sessionId)

## fd00:0000:0000:0000:c864:f17c:bb5e:e4d1 giulio
## fd00:0000:0000:0000:7481:4a85:5d87:9a52 altri
## fd00:0000:0000:0000:22c9:d0ff:fe47:70a3
print("STAR PEER")
p = PeerClient("fd00:0000:0000:0000:e6ce:8fff:fe0a:5e0e" , "fd00:0000:0000:0000:22c9:d0ff:fe47:70a3","3000")
print("SEND LOGIN")
print("ciao")
p.login()
