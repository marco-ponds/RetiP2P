# -*- coding: iso-8859-15 -*-
import sqlite3
from myexception import SessionIdNotExist
from InfoItem import *
import mylibrary
class ResultItem:
	def __init__(self, pack):
		self.__sessionId = pack.getSessionId()
		self.__search = pack.getRicerca()
		
	def search(self):
		conn = sqlite3.connect('database')
		conn.text_factory = str
		conn.row_factory = sqlite3.Row
		cur = conn.cursor()
		#controlliamo se l'utente è loggato
		control_query = "SELECT * FROM client WHERE sessionId='"+self.__sessionId+"'"
		cur.execute(control_query)
		r = cur.fetchall()
		if len(r) == 1:
			search_query = "SELECT * FROM file WHERE UPPER(filename) LIKE UPPER('%" +\
				self.__search + "%')"
			cur.execute(search_query)
			match_list = [] 
			r = cur.fetchall()
			for row in r:
				
				match_list.append(InfoItem(row['sessionId'], row['md5'], row['filename']))
#				match_list.append(InfoItem(row[0], row[1], row[2]))
#				r = cur.fetchone()				
			md5_list = {}
			final_string = ''
			#ciclo in cui per ogni md5 trova il numero di copie e chi ha quel file
			
			partial_string = '' 
			for i in range(len(match_list)):
				md5 = match_list[i].getMd5()
				if not(md5_list.has_key(md5)):
					md5_list[md5] = 1
					str_ip_port = ''
					filename = ''
					n_copy = 0
					for j in range(i, len(match_list)):
						if match_list[j].getMd5() == md5 :
							filename = match_list[j].getFilename() 
							str_ip_port += match_list[j].getAddress(cur)
							n_copy += 1
					md5_list[md5] = n_copy
					partial_string = md5 + filename + mylibrary.itos(n_copy, 3) + str_ip_port 
					final_string += partial_string
				else: continue
			final_string = mylibrary.itos(len(md5_list), 3) + final_string 
			return final_string	
		else:
			cur.close()
			raise SessionIdNotExist, self.__sessionId
		
		#con un ciclo confronto la lista dei filename con la stringa di ricerca
			#per ogni match metto in una lista l'md5 corrispondente controllando che non sia gia' presente con lo stesso filename
		#per ogni md5 trovato riporto il filename e l'eventuale numero di cop
