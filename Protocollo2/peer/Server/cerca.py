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

	def run(self):
		while self.canRun:
			try:
				peers = self.app.db.getAllPeers()
				if len(peers) != 0 and len(peers) < 3:
					chars = string.ascii_letters + string.digits
					packetID = "".join(random.choice(chars) for x in range(random.randint(16, 16)))
					for i in range(len(peers)):
						ip , port = peers[i]
						s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
						s.connect((ip, int(port)))
						ttl = "02"
						message = "NEAR" + packetID + self.address + self.port + ttl
						s.send(message)
						s.close()
				time.sleep(10)
			except:
				print("something wrong, sorry ", "ERR")
				print(sys.exc_info()[0], "ERR")
				print(sys.exc_info()[1], "ERR")
				print(sys.exc_info()[2], "ERR")
				return