import threading
import socket
##import os

class PeerToPeer(threading.Thread):

	def __init__(self, filename, socket):

		threading.Thread.__init__(self)
		self.filename = filename
		self.socket = socket

	def run(self):
		##filename = self.app.context["files_md5"][str(self.md5)]
		self.filename = self.filename.strip(" ")
		readFile = open(str("shared/"+self.filename) , "rb")
		##size = os.path.getsize("shared/"+filename)
		index = 0
		data = readFile.read(1024)
		message = "ARET"
		messagetemp = ""
		lunghezze = list()
		bytes = list()
		while data:
			##index += 1
			##messagetemp = messagetemp +"0"+str(len(data)) + str(data)
			lunghezze.append(str(len(data)))
			bytes.append(data)
			data = readFile.read(1024)
		## ha terminato di leggere il file
		##message = message + str(index) + messagetemp
		##self.socket.send(message)
		self.socket.send(message)
		l = len(str(int(len(bytes))))
		
		l_string = ("0" * (6 - l)) + str(int(len(bytes)))

		##self.socket.send(str(l_string).encode('utf-8'))
		self.socket.send(str(l_string))

		for i in range(len(bytes)):
			
			l_data = ("0" * (5 - len(str(lunghezze[i]))) + str(lunghezze[i]))

			self.socket.send(str(l_data).encode('utf-8'))
			self.socket.sendall(bytes[i])

		self.socket.close()
		return

class PacketHandler(threading.Thread):

	def __init__ (self, socket, type):
		threading.Thread.__init__(self)
		self.socket = socket
		self.type = type

	def run():
		if self.type == "NEAR":
			##abbiamo ricevuto richiesta di vicini
			packetID = self.socket.recv(16)
			ip = self.socket.recv(39)
			port = self.socket.recv(5)
			ttl = self.socket.recv(2)
			res = self.app.db.getPacchetto(packetID)
			if len(res) == 0:
				self.app.db.insertPacchetto(packetID, ip, port)
				if int(ttl) > 1:
					peers = self.app.db.getAllPeers()
					if len(peers) != 0:
						s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
						s.connect((ip, int(port)))
						for i in range(peers):
							p_ip , p_port = peers[i]
							message = "ANEA" + packetID + p_ip + p_port
						s.close()
			self.socket.close()
		if self.type == "ANEA":
			##ci stanno rispondendo con dei vicini
			#recupero i miei vicini e controllo di averne meno di tre
			peers = self.app.db.getAllPeers()
			if len(peers) < 3:
				packetID = self.socket.recv(16)
				ip = self.socket.recv(39)
				port = self.socket.recv(5)
				res = self.app.db.getPacchetto(packetID)
				if len(res) == 0:
					##non ho mai ricevuto questo pacchetto
					self.app.db.insertPacchetto(packetID, ip, port)
					self.app.db.insertPeer(ip, port)
			self.socket.close()

		if self.type == "QUER":
			#abbiamo ricevuto un pacchetto di query
			packetID = self.socket.recv(16)
			ip =  self.socket.recv(39)
			port = self.socket.recv(5)
			ttl = self.socket.recv(2)
			ricerca = self.socket.recv(20)
			#controllo se non ho ricevuto il pacchetto
			res = self.app.db.getPacchetto(packetID)
			if len(res) == 0:
				self.app.db.insertPacchetto(packetID, ip, port)
				files = self.app.db.searchFile(ricerca.trim(" "))
				if len(files) != 0:
					#abbiamo trovato i file
					s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
					s.connect((ip, int(port)))
					for i in range(len(files)):
						filename, md5 = files[i]
						temp = filename
						if len(temp) < 100:
							while len(temp) < 100:
								temp = temp + " "
						elif len(temp) > 100:
							temp = temp[0:100]
						message = "AQUE" + packetID + self.address + self.port + md5 + temp
						s.send(message)
					s.close()
					#non propaghiamo la ricerca
				else:
					if int(ttl) > 1:
						ttl = ttl - 1
						#propaghiamo la ricerca ai nostri vicini
						peers = self.app.db.getAllPeers()
						if len(peers) != 0:
							for i in range(len(peers)):
								p_ip, p_port = peers[i]
								s = socket.socket(socket.AF_INET6 , socket.SOCK_STREAM)
								s.connect((p_ip, int(p_port)))
								message = "QUER" + packetID + ip + port + ttl + ricerca
								s.send(message)
								s.close()
			self.socket.close()

			
		if self.type == "AQUE":
			packetID = self.socket.recv(4)
			ip = self.socket.recv(39)
			port = self.socket.recv(5)
			md5 = self.socket.recv(16)
			filename = self.socket.recv(100)
			s = str(nome) + "\t #copie" + str(copie)
			print(str(file_md5) + " - " + str(nome) + " - " + str(copie) )
			self.interface.log(s + " " + str(file_md5))
			self.app.context["peers_addr"].append(s)
			self.app.context["peers_index"] += 1
			self.interface.log("\t" + str(ip) + " " + str(port))
			self.app.context["peers_addr"].append(str(ip))
			key = str(self.app.context["peers_index"])+"_"+str(ip) 
			self.app.context["downloads_available"][str(key)] = dict()
			self.app.context["downloads_available"][str(key)]["porta"] = port
			self.app.context["downloads_available"][str(key)]["nome"] = filename.strip(" ")
			self.app.context["downloads_available"][str(key)]["md5"] = md5
			self.app.context["peers_index"] += 1
			self.app.peerList.adapter.data = self.app.context["peers_addr"]
			self.app.peerList.populate()


class Receiver(threading.Thread):

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
				try:
					socketclient, address = self.socket.accept()
					msg_type = socketclient.recv(4)
					if msg_type == "RETR":
						md5 = socketclient.recv(16)
						filename = self.app.context["files_md5"][str(md5)]
						PeerToPeer(filename, socketclient).start()
					else:
						PacketHandler(socketclient, msg_type).start()
					
						
				except:
					##self.interface.log("exception inside our server","SUC")
					return
		except:
			##self.interface.log("something wrong in our peer server. sorry","ERR")
			return