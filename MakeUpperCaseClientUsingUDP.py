"""  MakeUpperCaseClientUsingUDP.py

  Yuqi Liu, Libin Feng
  CISC-650 Fall 2014
  Sep 24, 2014
  This module will:
        a. Send an user-input lowercase sentence to the server;
        b. Receive the converted sentence from the server and displays on the screen.
"""

from socket import *

# STUDENTS - replace with your server machine's name
serverName = "128.4.246.11"

# STUDENTS - randomize your port number (use the same one in the server)
# This port number in practice is often a "Well Known Number"
serverPort = 35281

# create UDP socket
# Error in book? clientSocket = socket(socket.AF_INET, socket.SOCK_DGRAM)
#    corrected by  Amer 4-2013
clientSocket = socket(AF_INET, SOCK_DGRAM)


# get user's input from keyboard
# raw_input changed to input for Python 3  Amer 4-2013
message = input("Input lowercase sentence: ")

# send user's sentence out socket; destination host and port number req'd
# need to cast message to bytes for Python 3   Amer 4-2013
clientSocket.sendto(bytes(message,"utf-8"), (serverName, serverPort))

print ("Sent to Make Upper Case Server running over UDP: ", message)

# receive modified sentence in all upper case letters from server
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

# output modified sentence and close the socket
print ("Received back from Server: ", modifiedMessage)

# close the UDP socket
clientSocket.close()

