"""  FTPClientUsingTCP.py                                     

[STUDENTS FILL IN THE ITEMS BELOW]  
  Libin Feng, Yuqi Liu                                 
  CISC-650 Fall 2014                    
  Sep 26, 2014                                         
  This module will:
	a. start a TCP control connection to the server
	b. ask the client to input the name of a file
	c. receive the response from server. If the response is 'yes', then start using TCP 
	   transfer to receive the file. If the response is 'no', then give the client a
	   prompt and exit.
"""

from socket import *

# server machine's name 
serverName = "hostname"

# port numbers of server
serverPort_ctrl = 12306
serverPort_transf= 12307

# start using TCP transfer to transfer the file 
def start_transfer():
	# create TCP transfer socket on client to use for connecting to remote
	# server. Indicate the server's remote listening port
	clientSocket_transf = socket(AF_INET,SOCK_STREAM)

	# open the TCP transfer connection
	clientSocket_transf.connect((serverName,serverPort_transf))
	
	# connection prompt
	print("TCP transfer connected. | Server: %s, Port: %d" % (serverName, serverPort_transf))
	
	# get the data back from the server
	filedata = clientSocket_transf.recv(5000)
	
	# creat a file named "filename" and ready to write binary data to the file
	filehandler = open(filename, 'wb')
	
	# write the data to the file
	filehandler.write(filedata)
	
	# close the file
	filehandler.close()
	
	# close the TCP transfer connection
	return clientSocket_transf.close()
	

# create TCP socket on client to use for connecting to remote
# server. Indicate the server's remote listening port
clientSocket_ctrl = socket(AF_INET, SOCK_STREAM)

# open the TCP control connection
clientSocket_ctrl.connect((serverName,serverPort_ctrl))

# connection prompt
print("TCP control connected. | Server: %s, Port: %d" % (serverName, serverPort_ctrl))

# input the file name client wants 
filename = input("Input file name: ")

# send the file name to the server
clientSocket_ctrl.send(bytes(filename, "utf-8"))

# get the status of the file from server "yes" or "No"
filestatus = clientSocket_ctrl.recv(1024).decode("utf-8").strip()

# check whether the file is on the server. If yes, receive the file.
# If no, do give a prompt
if filestatus == "yes":
	# download prompt
	print("Start downloading..")
	
	# start using TCP transfer
	start_transfer()
	
	# success prompt
	print("Done!")
else:
	# cannot find the file on the server
	print("No such file found on the server!")

# close the TCP control connection
clientSocket_ctrl.close()