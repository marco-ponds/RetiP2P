import socket
import random
import threading
import hashlib
import glob

from Tkinter import *

context = dict()

class PeerServer(threading.Thread):

	def __init__ (self, address, port , owner):

		self.canRun = True
		threading.Thread.__init__(self)
		self.address = address
		self.port = int(port)
		self.owner = owner

		self.setDaemon(True)
		self.owner._print("PEER ADDRESS "+ self.address + ":" + str(self.port))

	def startServer ( self ):
		##launching peer server
		pass

	def stopServer(self):
		self.owner._print("CLOSING THREAD")
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
						self.owner._print("MSG TYPE " + msg_type)
					else:
						self.owner._print("closing socket connection")
				except:
					self.owner._print("exception inside our server")
					return
		except:
			self.owner._print("something wrong in our peer server. sorry")
			return

class BackgroundService(threading.Thread):

	def __init__ (self, owner):
		threading.Thread.__init__(self)
		self.owner = owner
		self.canRun = True

	def stop(self):
		self.canRun = False	

	def run(self):
		self.owner._print(glob.glob("data/*.*"))
		self.retrieveFiles()
		while self.canRun:
			self.checkFiles()
		return		

	def retrieveFiles(self):

		context["files"] = glob.glob("data/*.*")

	def checkFiles(self):

		if context['files']:
			temp = glob.glob("data/*.*")
			to_remove = list(set(context['files']) - set(temp))
			to_add = list(set(temp) - set(context['files']))
			if len(to_remove) > 0 :
				for f in to_remove:
					filename_rem = f.split("data/")[1]
					md5_rem = self.owner._calcMD5(filename_rem)
					self.owner._print("REMOVE " + filename_rem)
					##self.owner.removeFile(filename_rem,md5_rem)

			if len(to_add) > 0  :
				for f in to_add:
					filename_add = f.split("data/")[1]
					md5_add = self.owner._calcMD5(filename_add)
					self.owner._print("ADD " + filename_add)
					##self.owner.addFile(filename_add,md5_add)

			context["files"] = temp


		else:
			context["files"] = glob.glob("data/*.*")
				

class PeerClient(object):

	## azioni ammesse dal peer
	## login
	## logout
	## storage ( key, value )
	def __init__(self , master, ip_p2p , ip_dir="none" , porta_dir="none"):
		try:

			self._createLayout(master)

			##we should retrieve our ipv6 address and create a new port
			##print([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]])
			##self.ip_p2p = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]][0]
			self.ip_p2p = ip_p2p
			self.port = str(random.randint(8000,9000))
			##we obtained a new port between 8000 and 9000
			self._print(self.ip_p2p +":"+self.port)

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

			self.peer_server = PeerServer(self.ip_p2p , self.port , self)
			self.peer_server.start()

			## initializine background service
			self.background_service = BackgroundService(self)
			self.background_service.start()

		except:
			print("something wrong, sorry")
			return
		
	def _createLayout(self, master):
		##creating layout
		self.frame = Frame(master)
		self.frame.pack()

		self.loginButton = Button(self.frame, text="login" , command=self.login)
		self.loginButton.pack(side=LEFT)

		self.logoutButton = Button(self.frame, text="logout", command=self.logout)
		self.logoutButton.pack(side=LEFT)

		self.exitButton = Button(self.frame, text="exit", command=self.quit)
		self.exitButton.pack(side=LEFT)

		self.console = Text(self.frame, width=50, height=30)
		self.console.pack()

	def _print(self, message):
		if self.console:
			self.console.insert(END, "\n"+str(message))

	def _calcMD5(self, filename):
		m = hashlib.md5()
		readFile = open(str("data/"+filename) , "r")
		text = readFile.readline()
		while text:
			m.update(text)
			text = readFile.readline()

		digest = m.hexdigest()
		self._print(digest);
		return digest


	def quit(self):
		##effettuo il logout
		##self.logout()
		self.peer_server.stopServer()
		self.background_service.stop();
		self._print(self.peer_server.isAlive())
		self.frame.quit()

	def login(self):
		self.connection_socket = socket.socket(socket.AF_INET6 , socket.SOCK_STREAM)
 		self.connection_socket.connect(self.directory)
 		##mandiamo il messaggio di login
 		message = "LOGI"+str(self.ip_p2p)+str(self.port) 		
 		self._print(message)
 		self.connection_socket.send(message)
 		message_type = self.connection_socket.recv(4)
 		session_id = self.connection_socket.recv(16)
 		self._print("TYPE " + message_type)
 		self._print("SESSION ID "+session_id)
		receivedLogin( session_id )
		self.connection_socket.close()

		##adding all files
		files = glob.glob("data/*.*")
		for f in files:
			filename = f.split("data/")[1]
			md5 = self._calcMD5(filename)
			self.addFile(filename,md5)

	def logout(self):
		if (context['sessionid']):
			self.connection_socket = socket.socket(socket.AF_INET6 , socket.SOCK_STREAM)
			self.connection_socket.connect(self.directory)
			##mandiamo messsaggio di logout
			message = "LOGO"+str(context['sessionid'])
			self._print("SENDING LOGOUT " + message)
			self.connection_socket.send(message)

			message_type = self.connection_socket.recv(4)
			file_deleted = self.connection_socket.recv(3)
			self._print("RECEIVED " + message_type)
			self._print("REMOVED " + file_deleted + " FILES") 

			self.connection_socket.close()

	def addFile(self, filename, md5):
		if context["sessionid"]:
			self.connection_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
			self.connection_socket.connect(self.directory)
			##aggiungiamo un file
			temp = filename
			if len(temp) < 100:
				while len(temp) < 100:
					temp = temp + " "
			message = "ADDF"+context["sessionid"]+md5+temp
			self.connection_socket.send(message)

			message_type = self.connection_socket.recv(4)
			copy_numbers = self.connection_socket.recv(3)

			self._print("RECEIVED " + message_type)
			self._print("NUMBER OF COPIES: " + copy_numbers)




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
##print("STAR PEER")
##p = PeerClient("fd00:0000:0000:0000:e6ce:8fff:fe0a:5e0e" , "fd00:0000:0000:0000:22c9:d0ff:fe47:70a3","3000")
##print("SEND LOGIN")
##print("ciao")
##p.login()


root  = Tk()
p = PeerClient(root,"fd00:0000:0000:0000:e6ce:8fff:fe0a:5e0e" , "fd00:0000:0000:0000:22c9:d0ff:fe47:70a3","3000")
root.mainloop()



