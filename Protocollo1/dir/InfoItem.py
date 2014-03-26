# -*- coding: iso-8859-15 -*-

class InfoItem:
    
    def __init__(self, s_id, md5, fn):
        self.__sessionId = str(s_id)
        self.__md5 = str(md5)
        self.__filename = str(fn)
        
    def getSessionId(self):
        return self.__sessionId
    
    def getMd5(self):
        return self.__md5
    
    def getFilename(self):
        return self.__filename
    
    def getAddress(self, cursor):
        select_query = "SELECT * FROM client WHERE sessionId='" + self.__sessionId + "'"
        cursor.execute(select_query)
        r = cursor.fetchone()
        return str(r['ip'] + r['port'])
        
    
    