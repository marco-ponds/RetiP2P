# -*- coding: iso-8859-15 -*-
#Aggiornati Codici Operativi

import string
import mylibrary
#probabile funzione da ridefinire o cancellare
def removeSession(id,lista):
	cont=0
	for i in lista:
		if(lista[cont].getId()==id):
			del lista[cont]
		cont=cont+1

#probabile funzione da ridefinire o cancellare
def getIndexbyID(id,lista):
	cont=0
	for i in lista:
		if(lista[cont].getId()==id):
			return cont
		cont=cont+1

def LogAck(id):
	str='ALGI'+id
	return str

def AddAck(n):
    str = "AADD" + mylibrary.itos(n, 3)
    return str

def RmvAck(n):
	str = "ADEL" + mylibrary.itos(n, 3)
	return str

def LogoAck(n):
	str = "ALOG" + mylibrary.itos(n, 3)
	return str

def RicAck(s):
	str = "AFIN" + s
	return str

def DownAck(n):
	str = "ADRE" + mylibrary.itos(n, 5)
	return str
