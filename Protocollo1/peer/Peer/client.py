import sys
import socket
import time
import random

class PeerClient(object):

	## azioni ammesse dal peer
	## login
	## logout
	## storage ( key, value )


	def set(self, app, ip_p2p , ip_dir="none" , porta_dir="none"):
		print("inside peer set")
		try:
			self.app = app
			self.interface = app	

			##we should retrieve our ipv6 address and create a new port
			##self.interface.log([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]])
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


		except:
			print("something wrong, sorry ", "ERR")
			print(sys.exc_info()[0], "ERR")
			print(sys.exc_info()[1], "ERR")
			print(sys.exc_info()[2], "ERR")
			return

	def quit(self):
		##effettuo il logout
		##self.logout()
		##self.peer_server.stopServer()
		##self.background_service.stop();
		##self.interface.log(self.peer_server.isAlive())
		##frame.quit()
		pass

	def login(self):

		self.connection_socket = socket.socket(socket.AF_INET6 , socket.SOCK_STREAM)
 		self.connection_socket.connect(self.directory)
 		##mandiamo il messaggio di login
 		message = "LOGI"+str(self.ip_p2p)+"0"+str(self.port) 		
 		self.interface.log(message)
 		self.connection_socket.send(message)
 		message_type = self.connection_socket.recv(4)
 		session_id = self.connection_socket.recv(16)
 		self.interface.log("TYPE " + message_type)
 		self.interface.log("SESSION ID "+session_id)
		receivedLogin( session_id )
		self.connection_socket.close()

		##adding all files
		files = glob.glob("shared/*.*")
		for f in files:
			filename = f.split("shared/")[1]
			md5 = str(self.app.calcMD5(filename))
			self.addFile(filename,md5)

		##self.peer_server = PeerServer(self.ip_p2p , self.port , self)
		##self.peer_server.start()

		## initializine background service
		##self.background_service = BackgroundService(self)
		##self.background_service.start()


	def logout(self):
		if (self.app.context['sessionid']):
			self.connection_socket = socket.socket(socket.AF_INET6 , socket.SOCK_STREAM)
			self.connection_socket.connect(self.directory)
			##mandiamo messsaggio di logout
			message = "LOGO"+str(self.app.context['sessionid'])
			self.interface.log("SENDING LOGOUT " + message)
			self.connection_socket.send(message)

			message_type = self.connection_socket.recv(4)
			file_deleted = self.connection_socket.recv(3)
			self.interface.log("RECEIVED " + message_type)
			self.interface.log("REMOVED " + file_deleted + " FILES") 

			self.connection_socket.close()

	def addFile(self, filename, md5):
		if self.app.context["sessionid"]:
			self.connection_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
			self.connection_socket.connect(self.directory)
			##aggiungiamo un file
			temp = filename
			if len(temp) < 100:
				while len(temp) < 100:
					temp = temp + " "
			message = "ADDF"+self.app.context["sessionid"]+md5+temp
			self.interface.log(str(message))
			self.connection_socket.send(message)

			message_type = self.connection_socket.recv(4)
			copy_numbers = self.connection_socket.recv(3)

			self.interface.log("RECEIVED " + message_type)
			self.interface.log("NUMBER OF COPIES: " + copy_numbers)

	def removeFile(self, filename, md5):

		if self.app.context["sessionid"]:
			self.connection_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
			self.connection_socket.connect(self.directory)
			##aggiungiamo un file
		
			message = "DELF"+self.app.context["sessionid"]+md5
			self.connection_socket.send(message)

			message_type = self.connection_socket.recv(4)
			copy_numbers = self.connection_socket.recv(3)

			self.interface.log("RECEIVED " + message_type)
			self.interface.log("NUMBER OF COPIES: " + copy_numbers)

	def searchFile(self):

		searchString = self.interface.searchBox.text ##.get("1.0", END)[0:-1]
		if not len(searchString) == 0:
			
			if self.app.context["sessionid"]:
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

				message_type = self.connection_socket.recv(4)
				num = int(self.connection_socket.recv(3))
				if num != 0:
					for f in range(num):
						self.interface.log(self.connection_socket.recv(16))
						self.interface.log(self.connection_socket.recv(100))
						copie = int(self.connection_socket.recv(3))
						for c in range(copie):
							self.interface.log("\t"+self.connection_socket.recv(39))
							self.interface.log("\t"+self.connection_socket.recv(5))
				else:
					self.interface.log("NON HO TROVATO NESSUN FILE." , "ERR")
				



	def checkIPV6Format(self, address):
		try:
			socket.inet_pton(socket.AF_INET6, address)
			return True
		except:
			return False