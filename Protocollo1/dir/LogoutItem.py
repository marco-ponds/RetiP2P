# -*- coding: iso-8859-15 -*-
import sqlite3
from myexception import *
from mylibrary import stampaRow
class LogoutItem:
    __sessionID = ''
        
    def logout(self, pack):
        self.__sessionID = pack.getSessionId()
        conn = sqlite3.connect('database')
        conn.text_factory = str
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        #premessa di controllo 
        control_query = "SELECT * FROM client WHERE sessionId='"+self.__sessionID+"'"
        cur.execute(control_query)
        r = cur.fetchall()
        if len(r) == 1:
            stampaRow(cur, self.__sessionID)
            #prima query di cancellazione, elimina i record dei file associati 
            #al sessionId in questione nella table file
            delete_query = "DELETE FROM file WHERE sessionId='" + self.__sessionID + "'"
            cur.execute(delete_query)
            #numero di record relativi ai file cancellati dall'apertura della connessione
            #number of deleted file
            nodf = cur.rowcount
            conn.commit()
            stampaRow(cur, self.__sessionID)
            #seconda query di cancellazione, rimuove il record del sessionId 
            #nella table client
            delete_query = "DELETE FROM client WHERE sessionId='" + self.__sessionID + "'"
            cur.execute(delete_query)
            conn.commit()
            
            return nodf
            
        else:
            raise SessionIdNotExist, self.__sessionID
        
        
        