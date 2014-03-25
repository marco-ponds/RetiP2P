import threading
import socket

class PeerServer(threading.Thread):

	def __init__ (self, app):

		self.canRun = True
		threading.Thread.__init__(self)
		self.app = app
		self.peer = app.peer 
		self.address = app.peer.ip_p2p
		self.port = int(app.peer.port)

		self.setDaemon(True)
		print("PEER ADDRESS "+ self.address + ":" + str(self.port), "SUC")

	def startServer ( self ):
		##launching peer server
		pass

	def stop(self):
		##self.interface.log("CLOSING THREAD", "LOG")
		self.canRun = False
		##trying to connect to my own port
		socket.socket(socket.AF_INET6, socket.SOCK_STREAM).connect((self.address, self.port))
		self.socket.close()
	
	def run(self):
		try:
			self.socket = socket.socket(socket.AF_INET6 , socket.SOCK_STREAM)
			self.server_address = ( self.address , int(self.port))
			self.socket.bind(self.server_address)
			self.socket.listen(1)
			while True:
				print(".")
				try:
					socketclient, address = self.socket.accept()
					msg_type = socketclient.recv(4)
					if msg_type:
						pass
						##self.interface.log("MSG TYPE " + msg_type, "SUC")
					else:
						pass
						##self.interface.log("closing socket connection","SUC")
				except:
					##self.interface.log("exception inside our server","SUC")
					return
		except:
			##self.interface.log("something wrong in our peer server. sorry","ERR")
			return