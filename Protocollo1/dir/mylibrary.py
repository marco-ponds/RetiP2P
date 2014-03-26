# -*- coding: iso-8859-15 -*-
#################################################################
# libreria di funzioni custom
#
#	librerie necessarie:
#		-string
#################################################################

#Aggiornate Lunghezze Stringhe

import string
import sqlite3
import myexception
from random import *

LOGIN = 0
UPLOAD = 1
REMOVE = 2
SEARCH = 3
LOGOUT = 4
DOWNLOAD = 5

LOGI_LEN = 48
UP_LEN = 136
RM_LEN = 36
SR_LEN = 40
LOGO_LEN = 20
DOWN_LEN = 36
#DIZIONARIO DELLE VARIE LUNGHEZZE DEI PACCHETTI
list_len = {LOGIN:LOGI_LEN, UPLOAD: UP_LEN, REMOVE: RM_LEN, \
		SEARCH: SR_LEN, LOGOUT: LOGO_LEN, DOWNLOAD: DOWN_LEN}


#funzione che determina se un parametro dato e' un intero o no
def is_integer(x):
	try:
		int(x)
		return True
	except TypeError:
		return False

#funzione che identifica il tipo di pacchetto
def identifyPack(stringa):
	tipo = string.upper(stringa[0:4])
	if tipo == "LOGI":
		return LOGIN
	elif tipo == "ADDF":
		return UPLOAD
	elif tipo == "DELF":
		return REMOVE
	elif tipo == "FIND":
		return SEARCH
	elif tipo == "LOGO":
		return LOGOUT
	elif tipo == "DREG":
		return DOWNLOAD
	else:
		raise myexception.PackTypeNotDefinedException, tipo

#stabilisce la lunghezza massima che potrà avere il pacchetto ricevuto
def pack_length(tipo):
	return list_len[tipo]

def initializeDB(filename):
	file = filename
	conn = sqlite3.connect('database')
	cursor = conn.cursor()
	c_str = '''CREATE TABLE client (ip TEXT, port TEXT, sessionId TEXT PRIMARY KEY NOT NULL)'''
	cursor.execute(c_str)
	c_str = '''CREATE TABLE file (sessionId TEXT NOT NULL, md5 TEXT NOT NULL, filename TEXT,PRIMARY KEY (sessionId, md5) )'''
	cursor.execute(c_str)
	c_str = '''CREATE TABLE download (md5 TEXT NOT NULL, count INTEGER,PRIMARY KEY (md5) )'''
	cursor.execute(c_str)
	conn.commit()
	cursor.close()

#converte un intero n in una stringa di lunghezza data length
def itos(n, length):
	stringa = str(n)
	while (length - len(stringa)) > 0 :
		stringa = '0'+stringa
	return stringa


def random_sessionID():
    chars = string.ascii_letters + string.digits
    return "".join(choice(chars) for x in range(randint(16, 16)))

#def stampaRow(cursor, s_id):
#	query = "SELECT * FROM file WHERE sessionId='" + s_id + "'"
#	cursor.execute(query)
#	for row in cursor:
#		print repr(row)
#	print "\n"

def stampaRow(cursor, s_id):
	query = "SELECT * FROM file WHERE sessionId='" + s_id + "'"
	cursor.execute(query)
	r = cursor.fetchall()
	for i in range(len(r)):
		print r[i]
	print "\n"

