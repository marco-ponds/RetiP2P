# -*- coding: iso-8859-15 -*-
################################################
#	Main
#
#################################################

import mysocket
import socket
import threading 
import os.path
from serverThread import *

#inizializzo un database (creo tre tabelle) se non esiste gia'
if not(os.path.isfile('database')):
    initializeDB('database')

#crea una socket INET di tipo STREAM
serversocket = mysocket.mysocket()

#si associa il socket ad un host pubblico ed alla porta 3000
##serversocket.bind("fd00:0000:0000:0000:e6ce:8fff:fe0a:5e0e", 3007)
serversocket.bind("0000:0000:0000:0000:0000:0000:0000:0001" , 3013)
#serversocket.bind("fd00:0000:0000:0000:9afe:94ff:fe3f:b0f2", 3000)

#metto la socket in ascolto
serversocket.listen(100)

print "Directory listening..."

while True:
	print "Waiting for connection..."
	#accetta le connessioni dall'esternoi
	socketclient, address = serversocket.accept()
	#socketclient, address = s_sock.accept()
	print "Got connection from", address
	#elaboriamo le richieste con i thread in maniera tale da poter gestire piu' client contemporaneamente
	st = serverThread(socketclient, address)
	st.start()
	n = threading.activeCount() - 1
	print "" + repr(n) + " connections are active"
