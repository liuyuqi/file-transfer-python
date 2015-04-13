""" FTPServerUsingUDP.py

  Yuqi Liu, Libin Feng
  CISC-650 Fall 2014
  Sep 26, 2014

  This module will:
    a. Creates a TCP socket and listens to connection request on port 12306;
    b. Accept request from client and receives the client's desired filename;
    c. Search for the file under current working directory. If not found, sends "no" back to the client, and closes the TCP connection;
    d. If file is found, sends "yes" back to the client via the TCP connection, and sends the MD5 value of the desired file's content, then closes the TCP connection;
    e. Waits for client's start signal from UDP:12307.
    f. Once received the client's start signal, send the content of the desired file to the client using UDP.
    g. Goto b, continuing with the next loop of iteration.

"""

from socket import *
from hashlib import *

TCPPort = 12306
UDPPort = 12307

# creates TCP socket and bind to specified port first (for FTP-PDU control information)
TCPSocket = socket(AF_INET, SOCK_STREAM)
try:
    TCPSocket.bind(("", TCPPort))
except:
    print("***** FTPServerUsingUDP: error: Port 12306 is not available, Quitting... ")
    exit(0)

TCPSocket.listen(1)

# create UDP socket and bind to your specified port
UDPSocket = socket(AF_INET, SOCK_DGRAM)
UDPSocket.bind(("", UDPPort))
print ("The FTP server using UDP is listening to user request on port TCP: %d ... " % TCPPort)
print ("FTPServerUsingUDP: the UDP port to this server is %d." % UDPPort)

while True:
    # read the FILENAME included in client's message
    #    AND REMEMBER client's address (IP and port)
    connectionSocket, addr = TCPSocket.accept()
    file_name = connectionSocket.recv(255).decode('utf-8').strip()

    # tries to open the file. If yes, sends 'yes' to the client;
    #    otherwise, sends 'no' to the client and closes the TCP connection.
    try:
        file_handler = open(file_name, 'rb')
        connectionSocket.send(b'yes')
    except:
        print ("***** Server log: file \"%s\" cannot open!" % file_name)
        connectionSocket.send(b'no')
        connectionSocket.close()
        continue

    # get file content and md5
    file_content = file_handler.read()
    md5_val = md5(file_content).hexdigest()

    # sends the md5 value to the client using TCP. Then, closes the TCP connection.
    connectionSocket.send(bytes(md5_val, 'utf-8'))
    connectionSocket.close()

    # Waits the signal message from the client before start sending the file contents.
    message, clientAddr = UDPSocket.recvfrom(255)

    # sends the file content to clientAddress
    UDPSocket.sendto(file_content, clientAddr)
    print("Sent file \"%s\" to client (IP, port) = %s\n" % (file_name, str(clientAddr)))

