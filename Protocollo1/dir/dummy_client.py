# -*- coding: iso-8859-15 -*-
from socket import *

#variabile in cui è contenuta l'indirizzo del server
#s_addr = raw_input("Inserisci indirizzo server\n")
#s_addr = gethostname()
#s_addr = gethostbyaddr('127.0.0.1')[0]
s_addr = '::1'
sock = socket(AF_INET6, SOCK_STREAM)
sock.connect((s_addr, 3000))
i = 0
while i < 1:
    #stringa da inviare
#    send_str = raw_input("Inserisci stringa da inviare\n")
#    send_str = "LOGI1234:1234:1234:1234:1234:1234:1235:123450001"
#    send_str = "ADDF9sI8ZrEk2wnXko3K1234567890123459" + ('r'*100)
#    send_str = "ADDF2e5Bmkn7GiIYXCOB1234567890123458" + 'a' + ('r'*99)
#    send_str = "DELFa37MiACFPhzcMGSp1234567890123457"
#    send_str = "FINDa37MiACFPhzcMGSprrr"+(' '*17)
#    send_str = "LOGOa37MiACFPhzcMGSp"
    send_str = "DREG9sI8ZrEk2wnXko3K1234567890123457"
    print send_str
    
    sock.send(send_str)

    #stringa da ricevere
    recv_str = sock.recv(1024)
    print recv_str
    recv_str = sock.recv(1024)
    i = i + 1
