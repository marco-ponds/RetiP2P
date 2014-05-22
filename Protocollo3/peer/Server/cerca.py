import threading
import socket
import string
import random
import sys
import time

class CercaVicini (threading.Thread):

	def __init__(self, app):
		threading.Thread.__init__(self)
		self.app = app
		self.address = self.app.peer.ip_p2p
		self.port = self.app.peer.port
		self.canRun = True
		self.numErr = 0

	def stop(self):
		self.canRun = False

	def run(self):

		now = int(round(time.time()))
		while (int(round(time.time())) - now) < 10:
			try:
				self.app.log("searching super")
				peers = self.app.db.getAllPeers()
				if len(peers) != 0:
					chars = string.ascii_letters + string.digits
					packetID = "".join(random.choice(chars) for x in range(random.randint(16, 16)))
					for i in range(len(peers)):
						ip , port = peers[i]
						s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
						s.connect((ip, int(port)))
						self.app.log("sending near to " + str((ip, int(port))))
						ttl = "04"
						port_message = ("0" * (5-len(str(self.port)))) + str(self.port)
						message = "SUPE" + packetID + self.address + port_message + ttl
						self.app.log("SENDING " + message)
						s.send(message)
						s.close()
				time.sleep(10)
			except:
				self.numErr += 1
				self.app.log("CERCAVICINI ERRORE", "ERR")
				print(sys.exc_info()[0], "ERR")
				print(sys.exc_info()[1], "ERR")
				print(sys.exc_info()[2], "ERR")

		self.app.log("PASSATI 10 SECONDI. FINE RICERCA")	
		self.app.peer.isSearching = False
		#mi setto il superPeer a cui sono collegato
		if self.app.peer.iamsuper:
			self.app.log("ABOUT TO CHOOSE SUPER PEER")
			l = int(len(self.app.peer.superList))
			if l > 0:
				index = random.randint(0, l)
				self.app.peer.login(self.app.peer.superList[index])
			self.app.log("I'm super peer")	
		return










