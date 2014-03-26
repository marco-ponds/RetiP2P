# -*- coding: iso-8859-15 -*-

import sqlite3
from mylibrary import stampaRow
from myexception import SessionIdNotExist
class DownItem:
    __sessionID = ''
    __fileName = ''
    __md5file = ''

    def getDownload(self, pack):
        self.__sessionID = pack.getSessionId()
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
            select_query = "SELECT * FROM download WHERE md5='"+self.__md5file+"'"
            cur.execute(select_query)
            r = cur.fetchall()
            print r
            if len(r)!=0: #se il file e' stato scaricato almeno una volta
                update_query = "UPDATE download SET count = count+1 WHERE md5='" + self.__md5file +"'"
                cur.execute(update_query)
                conn.commit()
                select_query = "SELECT * FROM download WHERE md5='" + self.__md5file +"'"
                cur.execute(select_query)
                r = cur.fetchone()
                return r['count']
            else:# non esiste ancora un download per quel md5
                insert_query = "INSERT INTO download VALUES ('"+ self.__md5file + "', 1)"
                cur.execute(insert_query)
                conn.commit()
                return 1
        else: #utente non loggato
            cur.close()
            raise SessionIdNotExist, self.__sessionID 
