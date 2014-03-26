# -*- coding: iso-8859-15 -*-

from random import *
import sqlite3
from mylibrary import random_sessionID

class SessionItem:
	__ipp2p= ''
	__pp2p= ''
	__sessionID= ''


	def addSession(self, pacchetto):
		cont=0
		p = pacchetto.getIp()
		s = pacchetto.getPort()
		self.__ipp2p = p
		self.__pp2p = s
		self.__sessionID = random_sessionID()
		conn = sqlite3.connect('database')
		cur = conn.cursor()
		#verifica dell'inserimento di un sessionID unico
		r=[1]
		while(len(r)!=0):
			control_query="SELECT * FROM client WHERE sessionId='"+self.__sessionID+"'"
			cur.execute(control_query)
			r=cur.fetchall()
			if len(r)!=0:
				self.__sessionID = random_sessionID()
		# fine verifica dell'inserimento stesso sessionID
		
		
		#verifica se già loggato
		que="SELECT * FROM client WHERE ip='"+self.__ipp2p+ "' AND port='"+ self.__pp2p + "'"
		cur.execute(que)
		r=cur.fetchall()
		if (len(r)==0) :
			#in questo caso l'utente non è già loggato...
		
			query = "INSERT INTO client VALUES ('"+self.__ipp2p + "', '" +	self.__pp2p + "', '" + self.__sessionID + "')"
	#		print query
			cur.execute(query)
			conn.commit()		
			cur.execute("SELECT * FROM client ")
			for row in cur:
				print row
			cur.close()
			return self.__sessionID
		else:
			#utente già loggato
			return '0000000000000000'

	def getIp(self):
		return self.__ipp2p
		
	def getPort(self):
		return self.__pp2p
		
	def getId(self):
		return self.__sessionID