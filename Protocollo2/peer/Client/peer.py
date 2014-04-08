import sys
import socket
import time
import random
import glob
import string
import random

class PeerClient(object):

	def __init__(self, app , ip_p2p):

		print("inside peer set")
		try:
			self.app = app

			if ip_p2p == None:

				short_ip = socket.getaddrinfo(socket.gethostname(),None, socket.AF_INET6)[1][4][0]
				short_ip_a = short_ip.split(":")
				last = short_ip_a[-1]
				ip = ""
				for i in short_ip_a:
					if len(i) == 0:
						ip = ip + "0000:0000:0000:"
					else:
						if i == last:
							ip = ip + i
						else:
							ip = ip + i + ":"
						
				self.ip_p2p = ip

			else:
				self.ip_p2p = ip_p2p
			self.port = str(random.randint(8000,9000))
			##we obtained a new port between 8000 and 9000
			print(self.ip_p2p +":"+self.port)
			
			##check if our addresses are in ipv6 format	
			if not (self.checkIPV6Format(self.ip_p2p)):
				print("indirizzo non corretto")	
				return	


		except:
			print("something wrong, sorry ", "ERR")
			print(sys.exc_info()[0], "ERR")
			print(sys.exc_info()[1], "ERR")
			print(sys.exc_info()[2], "ERR")
			return

	def searchFile(self):
		try:
			searchString = self.app.searchBox.text ##.get("1.0", END)[0:-1]
			print("INSIDE SEARCH " + searchString)

			chars = string.ascii_letters + string.digits
			packetID = "".join(choice(chars) for x in range(random.randint(16, 16)))
			if not len(searchString) == 0:
				# prima di una nuova ricerca azzero le liste precedenti
				self.app.context["peers_addr"] = list()
				self.app.context["downloads_available"] = dict()
				self.app.context["peers_index"] = 0

				peers = self.app.db.getAllPeers()
				print("about to send connection")

				temp = searchString
				if len(temp) < 20:
					while len(temp) < 20:
						temp = temp + " "
				elif len(temp) > 20:
					temp = temp[0:20]

				if len(peers) !=0:
					for i in range(len(peers)):
						ip, port = peers[i]

						self.connection_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
						self.connection_socket.connect((ip, int(port)))

						ttl = "02"
						message = "QUER"+packetID+""+self.ip_p2p+""+self.port+""+ttl+""+temp
						self.connection_socket.send(message)
						self.connection_socket.close()
		except:
			print("EXCEPTION IN SEARCH FILE")

	def addNear(self):
		near_addr = self.app.nearAddr.text
		near_port = self.app.nearPort.text
		if near_addr != "" and near_port != "":
			self.app.db.insertPeer(near_addr, near_port)

	def downloadFile(self, listadapter, *args):
		try:
			self.interface.log("ABOUT TO DOWNLOAD FROM " + listadapter.selection[0].text)
			s = listadapter.selection[0].text
			i = self.app.context["peers_addr"].index(s)
			print("INSIDE DOWNLOAD ")
			key = str(i)+"_"+str(s)
			if(self.app.context["downloads_available"][str(key)]):
				peer = self.app.context["downloads_available"][str(key)]
				print(peer)
				##possiamo far partire il download del file
				destination = (s , int(peer["porta"]))
				print(destination)
				print(peer["md5"])
				self.connection_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
				self.connection_socket.connect(destination)
				message = "RETR"+str(peer["md5"])
				self.connection_socket.send(message)
				message_type = self.connection_socket.recv(4)
				num_chunks = self.connection_socket.recv(6)
				f = open('shared/'+peer["nome"].strip(" "), "wb")
				if int(num_chunks) > 0 :
					self.interface.progress.max = int(num_chunks)
					for i in range(int(num_chunks)):
						len_chunk = self.connection_socket.recv(5)
						if (len_chunk > 0):
							self.interface.progress.value = self.interface.progress.value + 1
							chunk = self.connection_socket.recv(int(len_chunk))
							f.write(chunk)
					f.close()

				self.connection_socket.close()
				self.interface.progress.value = 0

			else:
				print("NOT AVAILABLE")
		except:
			print("exception!!")
			print(sys.exc_info()[0])
			print(sys.exc_info()[1])
			print(sys.exc_info()[2])



	def checkIPV6Format(self, address):
		try:
			socket.inet_pton(socket.AF_INET6, address)
			return True
		except:
			return False
