# -*- coding: iso-8859-15 -*-
import string
class LogPack:
	__ip=''
	__porta=''

	def __init__(self,str):
		self.__ip=str[4:43]
		self.__porta=str[43:48]

	def setIp(self,i):
		self.__ip = i

	def setPort(self,p):
		self.__porta = p

	def getIp(self):
		return self.__ip

	def getPort(self):
		return self.__porta


class AddPack:
    __sessionId = ''
    __md5 = ''
    __filename = ''

    def __init__(self, str):
        self.__sessionId = str[4:20]
        self.__md5 = str[20:36]
        self.__filename = str[36:136]

    def setSessionId(self, id):
        self.__sessionId = id

    def getSessionId(self):
        return self.__sessionId

    def setMd5(self, md5):
        self.__md5 = md5

    def getMd5(self):
        return self.__md5

    def setFilename(self, fn):
        self.__filename = fn

    def getFilename(self):
        return self.__filename

#classe del pacchetto di rimozione
class RmvPack:
	def __init__(self, str):
		self.__sessionId = str[4:20]
		self.__md5 = str[20:36]

	def setSessionId(self, id):
		self.__sessionId = id

	def getSessionId(self):
		return self.__sessionId

	def setMd5(self, md5):
		self.__md5 = md5

	def getMd5(self):
		return self.__md5

# classe del pacchetto di logout
class LogoPack:
	def __init__(self, str):
		self.__sessionId = str [4:20]

	def setSessionId(self, id):
		self.__sessionId = id

	def getSessionId(self):
		return self.__sessionId

#classe del pacchetto di ricerca
class RicPack:
	def __init__(self,str):
		self.__sessionId= str [4:20]
		s = str [20:36]
		i = string.find(s," ")
		self.__ricerca= s[:i]


	def setSessionId(self, id):
		self.__sessionId = id

	def getSessionId(self):
		return self.__sessionId

	def setRicerca(self, r):
		self.__ricerca = r

	def getRicerca(self):
		return self.__ricerca

class DownPack:
	def __init__(self,str):
		self.__sessionId = str[4:20]
		self.__md5 = str [20:36]
		#self.__ipp2p= str[36:51]
		#self.__pp2p = str [51:56]

	def setSessionId(self, id):
		self.__sessionId = id

	def getSessionId(self):
		return self.__sessionId

	def setMd5(self, md5):
		self.__md5 = md5

	def getMd5(self):
		return self.__md5

    #def setIp(self,i):
	#	self.__ipp2p = i
	#
	#def setPort(self,p):
	#	self.__pp2p = p
	#
	#def getIp(self):
	#	return self.__ipp2p
	#
	#def getPort(self):
	#	return self.__pp2p




