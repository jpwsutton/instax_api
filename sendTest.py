#!/usr/bin/env python

"""
A simple test client
"""

print("Instax API Send Test")

import socket


host = ''
port = 8080

def printByteArray(byteArray):
    hexString = ''.join('%02x'%i for i in byteArray)
    print(' '.join(hexString[i:i+4] for i in range(0, len(hexString), 4)))


#Create a TCP/IP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

try:
    message = "This is the message"
    sock.sendall(message)
    print(sock.recv(1024))

finally:
    print('Closing Socket')
    sock.close()
