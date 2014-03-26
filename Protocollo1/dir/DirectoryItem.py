# -*- coding: iso-8859-15 -*-
import sqlite3
from mylibrary import stampaRow
from myexception import SessionIdNotExist
class DirectoryItem:
	__sessionID = ''
	__fileName = ''
	__md5file = ''

	def addFile(self, pack):
		self.__sessionID = pack.getSessionId()
		self.__fileName = pack.getFilename()
		self.__md5file = pack.getMd5()
		
		conn = sqlite3.connect('database')
		conn.text_factory = str
		conn.row_factory = sqlite3.Row
		cur = conn.cursor()
		#controlla se l'utente è loggato
		control_query="SELECT * FROM client WHERE sessionId='"+self.__sessionID+"'"
		cur.execute(control_query)
		r = cur.fetchall()
		if len(r)!=0:
			#utente effettivamente loggato, controllo se esiste già il file
			select_query = "SELECT * FROM file WHERE sessionId='"+self.__sessionID + "' AND md5='"+ self.__md5file + "'"
			cur.execute(select_query)
			r = cur.fetchall()
			stampaRow(cur, self.__sessionID)
			if len(r)==0:
				#se il file non esiste, viene aggiunto 
				insert_query = "INSERT INTO file VALUES ('"+self.__sessionID + "', '" +	self.__md5file + "', '" + self.__fileName + "')"
				cur.execute(insert_query)
			else:
				#altrimenti il filename viene aggiornato
				update_query = "UPDATE file SET filename='" + self.__fileName + "'" +\
					" WHERE sessionId='" + self.__sessionID + "' AND md5='" + self.__md5file + "'"	
				cur.execute(update_query)
			conn.commit()
			
			stampaRow(cur, self.__sessionID)
			#calcolo del numero di copie
			select_query = "SELECT * FROM file WHERE md5='"+ self.__md5file + "'"
			cur.execute(select_query)
			r = cur.fetchall()
			cur.close()
			return len(r)
		else: #utente non loggato
			cur.close()
			raise SessionIdNotExist, self.__sessionID 
			
	#rimouve il record del file in questione dal database					
	def removeFile(self, pack):
		self.__sessionID = pack.getSessionId()
		self.__md5file = pack.getMd5()
		conn = sqlite3.connect('database')
		conn.text_factory = str
		conn.row_factory = sqlite3.Row
		cur = conn.cursor()
		stampaRow(cur, self.__sessionID)
		#da testare
		delete_query = "DELETE FROM file WHERE sessionId='" + self.__sessionID +\
		 "' AND md5='" + self.__md5file + "'"
		#vedere eccezioni che solleva la execute
		cur.execute(delete_query)
		conn.commit()
		stampaRow(cur, self.__sessionID)
		select_query = "SELECT * FROM file WHERE md5='"+ self.__md5file + "'"
		cur.execute(select_query)
		r = cur.fetchall()
		cur.close()
		return len(r)

			
	def getSessionID(self):
		return self.__sessionID
	
	def setSessionID(self, id):
		self.__sessionID=id
	
	def getFilename(self):
		return self.__fileName
	
	def setFilename(self, f):
		self.__fileName=f
	
	def getMd5(self):
		return self.__md5file
	
	def setMd5(self, m):
		self.__md5file=m
