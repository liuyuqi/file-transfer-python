"""  FTPClientUsingUDP.py                                     

[STUDENTS FILL IN THE ITEMS BELOW]  
  Libin Feng, Yuqi Liu                                 
  CISC-650 Fall 2014                    
  Sep 26, 2014                                         
  This module will:
	a. start a TCP connection to the server
	b. ask the user to input the name of a file
	c. receive the response from server. If the response is 'yes', get the md5 value of file, 
	   then start UDP and receive the file.
	   If the response is 'no', then give the client a prompt and exit.
	d. get the md5 value of the received file, and compare it with the md5 value sent from the
       server. If two values are same, the file received is intact. If two values are not same, 
	   the file received has been damaged.
"""

from socket import *
from hashlib import *

# start using UDP to transfer the file 
def startUsingUDP():
	# create UDP socket 
	clientUDPSocket = socket(AF_INET, SOCK_DGRAM)
	
	# start using UDP
	print("Start using UDP | Server: %s, Port: %d" % (serverName, serverUDPPort))
	
	# send a null string out socket; destination host and port number req'd
	clientUDPSocket.sendto(b'', (serverName, serverUDPPort))
	
	# download prompt
	print("Start downloading..")
	
	# get the file back from the server
	filedata, serverAddr= clientUDPSocket.recvfrom(5000)

	# get the md5 of the transferred data
	newMD5 = md5(filedata).hexdigest()

	# if the transmitted data has no error, then write the data to file. 
	# if the data has error, do nothing
	if newMD5 == filemd5:
		# no error prompt
		print("MD5 check success, no transmission error")
		
		# creat a file named "filename" and ready to write binary data to the file
		filehandler = open(filename, 'wb')
	
		# write the data to the file
		filehandler.write(filedata)
	
		# close the file
		filehandler.close()
		
		# success prompt
		print("Done!")
	else:
		# error prompt
		print("Error found")
			
	# close the UDP socket
	return	clientUDPSocket.close()

	
# server machine's name 
serverName = "128.4.53.163"

# port numbers of server  
serverTCPPort = 12306
serverUDPPort = 12307

# create TCP socket on client to use for connecting to remote
# server. Indicate the server's remote listening port
clientTCPSocket = socket(AF_INET, SOCK_STREAM)

# open the TCP connection
clientTCPSocket.connect((serverName,serverTCPPort))

# connection prompt
print("TCP connection established! | Server: %s, Port: %d" % (serverName, serverTCPPort))

# input the file name client wants 
filename = input("Input file name: ")

# send the file name to the server
clientTCPSocket.send(bytes(filename, "utf-8"))

# get the status of the file from server "yes" or "No"
filestatus = clientTCPSocket.recv(1024).decode("utf-8").strip()

# check whether the file is on the server. If yes, receive the file.
# If no, do nothing
if filestatus == "yes":
	# get the md5 back from the server
	filemd5 = clientTCPSocket.recv(5000).decode("utf-8").strip()
	
	# print the md5 value of the data expected to transfer
	print ("File md5: %s" % filemd5)
	
	# close the TCP connection
	clientTCPSocket.close()
	
	# start use UDP to download the file
	startUsingUDP()
	
else:
	# cannot find the file on the server
	print ("No such file found on the server!")
	# close the TCP connection
	clientTCPSocket.close()