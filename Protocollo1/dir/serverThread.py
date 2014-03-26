# -*- coding: iso-8859-15 -*-
#	Questa e' la classe serverThread, una subclasse di Thread che ridefinisce il costruttore __init() ed il metodo run()	


from threading import Thread
import mysocket
from mylibrary import *
from myexception import *
from pack_classes import *
from ack_function import *
from DirectoryItem import *
from SessionItem import *
from LogoutItem import *
from ResultItem import *
from DownItem import *
SHUT_RD = 0
SHUT_WR = 1
SHUT_RDWR = 2
class serverThread(Thread):
	def __init__(self, client_sock, client_address):
		Thread.__init__(self)
		#socket del client
		self.c_sock = mysocket.mysocket(client_sock)
		#self.c_ad = self.c_sock.ntohs(client_address)
		self.c_ad = client_address
		return

	def run(self):
		tipo = -1
		while True:
			print "thread"
			#imposto la lunghezza dei receive ai primi 4 bit
						
			try:
				self.c_sock.setLength(4)
				request = self.c_sock.receive(0)
				#la variabile tipo identifica il tipo di pacchetto ricevuto
				tipo = identifyPack(request)
				#lunghezza pacchetto
				p_len = pack_length(tipo)
				#alla lunghezza totale del pacchetto andranno sottratti i 4 Byte già letti
				self.c_sock.setLength(p_len-4)
				request = request + self.c_sock.receive(1)
			except PackTypeNotDefinedException, ptnde:
				print "Non esistono pacchetti di questo tipo:", ptnde.value, "\n"
				print "chiusura socket ed interruzione thread\n"
				self.c_sock.shutdown(SHUT_RD)
				self.c_sock.close()
				return
			except PackLengthNotValid, plnv:
				print "Il pacchetto ricevuto non è della lunghezza giusta"
				print "Interruzione thread\n"
				self.c_sock.shutdown(SHUT_RD)
				self.c_sock.close()
				return
			except RuntimeError, re:
				print "connessione socket interrotta"
				print "Interruzione thread\n"
				self.c_sock.shutdown(SHUT_RD)
				self.c_sock.close()
				#exit()
				return
			
			if (tipo == LOGIN):
				pack = LogPack(request)
				si = SessionItem()
				s_id = si.addSession(pack)				
				response = LogAck(s_id)
				self.c_sock.setLength(len(response))
				self.c_sock.send(response)
				
			elif (tipo == UPLOAD):
				pack = AddPack(request)
				di = DirectoryItem()
				try:
					n_copy = di.addFile(pack)
				except SessionIdNotExist, sine:
					print "Il sessionId dato: " + sine.value + " non esiste. Utente non loggato\n "
					print "chiusura socket ed interruzione thread\n"
					self.c_sock.shutdown(SHUT_RD)
					self.c_sock.close()
					return
				else:
					response = AddAck(n_copy)
					self.c_sock.setLength(len(response))
					self.c_sock.send(response)
				
			elif (tipo == REMOVE):
				pack = RmvPack(request)
				di = DirectoryItem()
				n_copy = di.removeFile(pack)
				response = RmvAck(n_copy)
				self.c_sock.setLength(len(response))
				self.c_sock.send(response)	
			
			elif (tipo == LOGOUT):
				pack = LogoPack(request)
				li = LogoutItem()
				try:
					n_delete = li.logout(pack)
				except SessionIdNotExist, sine:
					print "Il sessionId dato: " + sine.value + " non esiste. Utente non loggato\n "
					print "chiusura socket ed interruzione thread\n"
					self.c_sock.shutdown(SHUT_RD)
					self.c_sock.close()
					return
				else:
					response = LogoAck(n_delete)
					self.c_sock.setLength(len(response))
					self.c_sock.send(response)	
					
			elif (tipo == SEARCH):
				pack = RicPack(request)
				rs = ResultItem(pack)
				str = rs.search()				
				response = RicAck(str)
				self.c_sock.setLength(len(response))
				self.c_sock.send(response)
			elif (tipo == DOWNLOAD):
				pack = DownPack(request)
				dp = DownItem()
				n_of_download = dp.getDownload(pack)
				
				response = DownAck(n_of_download)
				self.c_sock.setLength(len(response))
				self.c_sock.send(response)
			#...
			#inserire elaborazione qui
			#...
			####### GESTIRE LE ECCEZIONI DELLE SEND E RECEIVE ##########
			
