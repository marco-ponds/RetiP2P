import socket
import random
import threading
import hashlib
import glob
import time

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
		self.owner._print("PEER ADDRESS "+ self.address + ":" + str(self.port), "SUC")

	def startServer ( self ):
		##launching peer server
		pass

	def stopServer(self):
		self.owner._print("CLOSING THREAD", "LOG")
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
						self.owner._print("MSG TYPE " + msg_type, "SUC")
					else:
						self.owner._print("closing socket connection","SUC")
				except:
					self.owner._print("exception inside our server","SUC")
					return
		except:
			self.owner._print("something wrong in our peer server. sorry","ERR")
			return

class BackgroundService(threading.Thread):

	def __init__ (self, owner):
		threading.Thread.__init__(self)
		self.owner = owner
		self.canRun = True
		self.setDaemon(True)

	def stop(self):
		self.canRun = False	

	def run(self):
		self.owner._print(glob.glob("shared/*.*"), "SUC")
		self.retrieveFiles()
		while self.canRun:
			time.sleep(1)
			self.checkFiles()
		return		

	def retrieveFiles(self):

		context["files"] = glob.glob("shared/*.*")

	def checkFiles(self):

		if context['files']:
			temp = glob.glob("shared/*.*")
			to_remove = list(set(context['files']) - set(temp))
			to_add = list(set(temp) - set(context['files']))
			if len(to_remove) > 0 :
				for f in to_remove:
					filename_rem = f.split("shared/")[1]
					md5_rem = context["md5_files"][filename_rem]
					self.owner._print("REMOVED " + filename_rem + " WITH MD5 " + md5_rem, "SUC")
					self.owner.removeFile(filename_rem,md5_rem)

			if len(to_add) > 0  :
				for f in to_add:
					filename_add = f.split("shared/")[1]
					md5_add = self.owner._calcMD5(filename_add)
					self.owner._print("ADDED " + filename_add + " WITH MD5 " + md5_add, "SUC")
					self.owner.addFile(filename_add,md5_add)

			context["files"] = temp
			self.storeMD5Files()

			self.printFilesToList()


		else:
			context["files"] = glob.glob("shared/*.*")

	def storeMD5Files(self):

		file_list = glob.glob("shared/*.*")
		context['md5_files'] = dict()
		for f in file_list:
			filename = f.split("shared/")[1]
			md5 = self.owner._calcMD5(filename)
			context['md5_files'][str(filename)] = md5

	def printFilesToList(self):
		file_list = glob.glob("shared/*.*")
		self.owner.fileList.delete(0, END)
		for f in file_list:
			filename = f.split("shared/")[1]
			self.owner.fileList.insert(END, filename)
				

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

			self.login()

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
		##self.loginButton.pack(side=LEFT)
		self.loginButton.grid(row=0, column=0)

		self.logoutButton = Button(self.frame, text="logout", command=self.logout)
		##self.logoutButton.pack(side=LEFT)
		self.logoutButton.grid(row=0, column=1)

		self.exitButton = Button(self.frame, text="exit", command=self.quit)
		##self.exitButton.pack(side=LEFT)
		self.exitButton.grid(row=0, column=2)

			

		self.search = Text(self.frame, width=100, height=1, background="yellow")	
		self.search.grid(row=0, column=3, columnspan=15)

		self.searchButton = Button(self.frame, text="search", command=self.searchFile)
		self.searchButton.grid(row=0, column=19)

		self.fileList = Listbox(self.frame, height=30)
		self.fileList.grid(row=1, column=0, columnspan=3, sticky=N+W+E, padx=10, pady=10)

		
		def onselect(evt):
		    # Note here that Tkinter passes an event object to onselect()
		    w = evt.widget
		    index = int(w.curselection()[0])
		    value = w.get(index)
		    self._print ('You selected item %d: "%s"' % (index, value))

		self.fileList.bind('<<ListboxSelect>>', onselect)


		self.console = Text(self.frame, width=100, height=30)
		##self.console.pack(side=RIGHT)
		self.console.grid(row=1, column=3, columnspan=16)

		self.console.tag_add("LOG", "1.0", "1.4")
		self.console.tag_add("ERR", "1.8", "1.13")
		self.console.tag_add("SUC", "1.0", "1.4")
		self.console.tag_config("LOG", foreground="blue")
		self.console.tag_config("ERR", foreground="RED")
		self.console.tag_config("SUC", foreground="green")


	def _print(self, message , messagetype="LOG"):
		if self.console:			
			self.console.insert(END, "\n"+str(message) , str(messagetype))

	def _calcMD5(self, filename):
		m = hashlib.md5()
		readFile = open(str("shared/"+filename) , "r")
		text = readFile.readline()
		while text:
			m.update(text)
			text = readFile.readline()

		digest = m.hexdigest()
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
		files = glob.glob("shared/*.*")
		for f in files:
			filename = f.split("shared/")[1]
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

	def removeFile(self, filename, md5):

		if context["sessionid"]:
			self.connection_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
			self.connection_socket.connect(self.directory)
			##aggiungiamo un file
		
			message = "DELF"+context["sessionid"]+md5
			self.connection_socket.send(message)

			message_type = self.connection_socket.recv(4)
			copy_numbers = self.connection_socket.recv(3)

			self._print("RECEIVED " + message_type)
			self._print("NUMBER OF COPIES: " + copy_numbers)

	def searchFile(self):

		searchString = self.search.get("1.0", END)[0:-1]
		if not len(searchString) == 0:
			
			if context["sessionid"]:
				self.connection_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
				self.connection_socket.connect(self.directory)
				##cerchiamo un file
				temp = searchString
				if len(temp) < 20:
					while len(temp) < 20:
						temp = temp + " "
				elif len(temp) > 20:
					temp = temp[0:20]

				message = "FIND"+context["sessionid"]+temp
				self.connection_socket.send(message)

				message_type = self.connection_socket.recv(4)
				num = int(self.connection_socket.recv(3))
				for f in range(num):
					self._print(self.connection_socket.recv(16))
					self._print(self.connection_socket.recv(100))
					copie = int(self.connection_socket.recv(3))
					for c in range(copie):
						self._print("\t"+self.connection_socket.recv(39))
						self._print("\t"+self.connection_socket.recv(5))
				



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
## fd00:0000:0000:0000:c646:19ff:fe69:b7a5
##print("STAR PEER")
##p = PeerClient("fd00:0000:0000:0000:e6ce:8fff:fe0a:5e0e" , "fd00:0000:0000:0000:22c9:d0ff:fe47:70a3","3000")
##print("SEND LOGIN")
##print("ciao")
##p.login()


def main():
	root  = Tk()
	p = PeerClient(root,"fd00:0000:0000:0000:e6ce:8fff:fe0a:5e0e" , "fd00:0000:0000:0000:c864:f17c:bb5e:e4d1","3000")
	root.mainloop()

if __name__ == '__main__':
    main() 


