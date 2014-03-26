# -*- coding: iso-8859-15 -*-
####################################################
#	socket personalizzata
#
#
########################################################


from socket import *
from myexception import PackLengthNotValid
from mylibrary import *
class mysocket:
	
	__MSGLEN = 100
		
	def __init__(self, sock=None):
		if sock is None:
			self.__sock = socket(AF_INET6, SOCK_STREAM) #Socket Ipv6 Ready...
			self.__sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		else: self.__sock = sock

	def connect(self, host, port):
		self.__sock.connect((host, port))
	
	#ridefinisce la send in maniera tale da inviare messaggi piÃ¹ lunghi di __MSGLEN (lunghezza del messaggio bufferizzato)

	def send(self, msg):
		totalsent = 0
		while totalsent < self.__MSGLEN:
			sent = self.__sock.send(msg[totalsent:])
			if sent == 0:
				raise RuntimeError, "connessioni socket interrotta"
			totalsent = totalsent + sent
	
	#ridefinisce la receive in maniera tale da ricevere messaggi più lunghi di __MSGLEN (lunghezza del messaggio bufferizzato)
	def receive(self, flag):
		msg = self.__sock.recv(self.__MSGLEN + flag*10)
		if msg == '':
			raise RuntimeError, "connessione socket interrotta"
		if len(msg) != self.__MSGLEN:
			raise PackLengthNotValid, "la lunghezza del pacchetto ricevuto " + \
				"è diversa da quella attesa"
		return msg

	#definisce il bind
	def bind(self, host, port):
		self.__sock.bind((host, port))
		
	#definisce listen
	def listen (self, value):
		self.__sock.listen(value)
	
	#definisce accept
	def accept(self):
		return self.__sock.accept()

	#definisce shutdown
	def shutdown(self, arg):
		return self.__sock.shutdown(arg)

	#definisce close
	def close(self):
		return self.__sock.close()

	#imposta la lunghezza massima del messaggio bufferizzato
	def setLength(self, length):
		if(not(is_integer(length))): 
			print "errore lunghezza messaggio bufferizzato, impostato valore di default 100B"
		else: self.__MSGLEN = length
			
