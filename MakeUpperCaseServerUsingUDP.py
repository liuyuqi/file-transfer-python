""" MakeUpperCaseServerUsingUDP.py

  Yuqi Liu, Libin Feng
  CISC-650 Fall 2014
  Sep 24, 2014
  This module will:
        a. Receive a message from serverPort;
        b. Converts the message to upper case;
        c. Sends back the message to the client.
"""

from socket import *

# STUDENTS - you should randomize your port number.
# This port number in practice is often a "Well Known Number"
serverPort = 12306

# create UDP socket and bind to your specified port
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))

# output to console that server is listening
print ("The Make Upper Case Server running over UDP is ready to receive ... ")

while 1:
    # read client's message AND REMEMBER client's address (IP and port)
    message, clientAddress = serverSocket.recvfrom(2048)

    # output to console the sentence received from client over UDP
    print ("Received from Client: ", message)

    # change client's sentence to upper case letters
    modifiedMessage = message.upper()

    # send back modified sentence to the client using remembered address
    serverSocket.sendto(modifiedMessage, clientAddress)

    # output to console the modified sentence sent back to client
    print ("Sent back to Client: ", modifiedMessage)
