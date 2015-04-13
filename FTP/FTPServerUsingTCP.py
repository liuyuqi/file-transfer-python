""" FTPServerUsingTCP.py

  Yuqi Liu, Libin Feng
  CISC-650 Fall 2014
  Sep 26, 2014

  This module will:
      a. Creates a TCP socket and listens to connection request on port 12306;
      b. Accepts request from client and receives the client's desired filename;
      c. Searches the file under current directory. If not found, sends "no" bcak to the client, and closes the TCP connection; Other wise, sends "yes" back to the client and transmit the content of the file;
      d. Closes the TCP connection.

"""

from socket import *

serverPort = 12306
filePort = 12307

# Creates TCP welcoming and file transfer socket
serverSocket = socket(AF_INET,SOCK_STREAM)
fileSocket = socket(AF_INET,SOCK_STREAM)
try:
    serverSocket.bind(("",serverPort))
except:
    print ("***** FTPServerUsingTCP: error: Port 12306 is not available, quitting...")
    exit(0)

try:
    fileSocket.bind(("",filePort))
except:
    print ("***** FTPServerUsingTCP: error: Port 12307 is not available, quitting...")
    exit(0)

# Server begins listening for incoming TCP requests
serverSocket.listen(1)
print ("The FTP Server running over TCP is listening on port %d ..." % serverPort)
fileSocket.listen(1)
print ("The FTP Server running over TCP is listening on port %d ... \n" % filePort)

while 1:
    # Waits for incoming requests; new socket created on return
    connectionSocket, addr = serverSocket.accept()
    print ("Connection established for client (IP, port) = %s" % str(addr))

    # Reads the filename from socket sent by the client.
    file_name = connectionSocket.recv(255)
    file_name = file_name.decode("utf-8").strip()

    # Opens the desired file.
    # If success to open, send "yes" to the client, and closes the TCP control connection;
    #     otherwise, send "no" to the client, closes the TCP control connection, and continue to the next loop
    try:
        file_handler = open(file_name, 'rb')
    except:
        connectionSocket.send(b"no")
        print ("***** Server log: file %s is not found, sent no to the client.\n" % file_name)
        connectionSocket.close()
        print("Connection to (IP, addr) = %s closed." % str(addr))
        continue
    connectionSocket.send(b"yes")
    connectionSocket.close()
    print("Connection to (IP, addr) = %s closed." % str(addr))

    # accepts the new file transfer connection
    transferSocket, addr = fileSocket.accept()
    print ("File Transfer connection established for client (IP, port) = %s" % str(addr))

    # Reads the content of the file
    file_content = file_handler.read()

    # Tries to send the file to the client using the TCP file transfer connection.
    #   On success, prints the success informtion on the screen;
    #       otherwise, prints the FAILURE information on the screen.
    try:
        transferSocket.send(file_content)
        file_handler.close()
        print ("file \"%s\" sent successfully!" % file_name)
    except:
        print ("***** Server log: file \"%s\" sent FAILED!!!" % file_name)

    # Closes the TCP file transfer connection.
    transferSocket.close()
    print("Connection to (IP, addr) = %s closed.\n" % str(addr))

