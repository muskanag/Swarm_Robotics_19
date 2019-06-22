import time
from socket import *

pings = 1

#Send ping 10 times
while pings < 11:

   #Create a UDP socket
   clientSocket1 = socket(AF_INET, SOCK_DGRAM)
   clientSocket2 = socket(AF_INET, SOCK_DGRAM)
   #Set a timeout value of 1 second
   clientSocket1.settimeout(1)
   clientSocket2.settimeout(1)

   #Ping to server
   message1 = input('> ').encode()
   message2 = input('> ').encode()

   addr1 = ("192.168.0.120", 5007)
   addr2 = ("192.168.0.103", 5007)

   #Send ping
   start = time.time()
   clientSocket1.sendto(message1, addr1)
   clientSocket2.sendto(message2, addr2)

   #If data is received back from server, print
   try:
       data, server = clientSocket1.recvfrom(1024)
       end = time.time()
       elapsed = end - start
       print(data)

   #If data is not received back from server, print it has timed out
   except timeout:
       print('REQUEST TIMED OUT1')

   try:
        data, server = clientSocket2.recvfrom(1024)
        end = time.time()
        elapsed = end - start
        print(data)

   except timeout:
        print('REQUEST TIMED OUT2')

   pings = pings - 1
