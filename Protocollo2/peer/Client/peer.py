import sys
import socket
import time
import random
import glob

class PeerClient(object):

	def __init__(self, app):

		print("inside peer set")
		try:
			self.app = app

			short_ip = socket.getaddrinfo(socket.gethostname(),None, socket.AF_INET6)[0][4][0]
			short_ip_a = short_ip.split(":")
			ip = ""
			for i in short_ip_a:
				if len(i) == 0:
					ip = ip + "0000:0000:0000:"
				else:
					ip = ip + i + ":"

			self.ip_p2p = ip

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


		except:
			print("something wrong, sorry ", "ERR")
			print(sys.exc_info()[0], "ERR")
			print(sys.exc_info()[1], "ERR")
			print(sys.exc_info()[2], "ERR")
			return

	def searchFile(self):

		searchString = self.interface.searchBox.text ##.get("1.0", END)[0:-1]
		print("INSIDE SEARCH " + searchString)
		if not len(searchString) == 0:
			
			print("about to send connection")
			self.connection_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
			self.connection_socket.connect(self.directory)
			##cerchiamo un file
			temp = searchString
			if len(temp) < 20:
				while len(temp) < 20:
					temp = temp + " "
			elif len(temp) > 20:
				temp = temp[0:20]

			message = "FIND"+self.app.context["sessionid"]+temp
			self.connection_socket.send(message)
			print("messaggio mandato")
			self.app.context["peers_addr"] = list()
			self.app.context["downloads_available"] = dict()

			message_type = self.connection_socket.recv(4)
			num = int(self.connection_socket.recv(3))

			print("messaggio ricevuto")
			if num != 0:
				print("abbiamo dei file")
				print("NUM " + str(num))
				i = 0
				for f in range(num):
					print("stampiamo file")
					print("INSIDE FOR "+ str(i))
					file_md5 = self.connection_socket.recv(16)
					nome = self.connection_socket.recv(100)
					copie = int(self.connection_socket.recv(3))
					s = str(nome) + "\t #copie" + str(copie)
					print(str(file_md5) + " - " + str(nome) + " - " + str(copie) )
					self.interface.log(s + " " + str(file_md5))
					self.app.context["peers_addr"].append(s)
					i += 1
					for c in range(copie):
						print("stampiamo i peer")
						ip = self.connection_socket.recv(39)
						port = int(self.connection_socket.recv(5))
						print("peer " + str(ip) + " - " + str(port) )
						self.interface.log("\t" + str(ip) + " " + str(port))
						self.app.context["peers_addr"].append(str(ip))
						key = str(i)+"_"+str(ip) 
						self.app.context["downloads_available"][str(key)] = dict()
						self.app.context["downloads_available"][str(key)]["porta"] = port
						self.app.context["downloads_available"][str(key)]["nome"] = nome.strip(" ")
						self.app.context["downloads_available"][str(key)]["md5"] = file_md5
						self.app.context["downloads_available"][str(key)]["numcopie"] = copie
						i += 1

				self.isready = False
				print("ALREADY SET self.isready " + str(self.isready))
				self.interface.peerList.adapter.data = self.app.context["peers_addr"]
				self.interface.peerList.populate()
				self.connection_socket.close()

			else:
				print("sono appena fallito")
				self.interface.peerList.adapter.data = list()
				self.interface.peerList.populate()
				self.connection_socket.close()
				self.interface.log("NON HO TROVATO NESSUN FILE." , "ERR")
		else:
			print("INSIDE SEARCH errore")


	def checkIPV6Format(self, address):
		try:
			socket.inet_pton(socket.AF_INET6, address)
			return True
		except:
			return False
