#!/usr/bin/env python

"""
A simple echo server
"""

print("Instax API EchoServer")

import socket

host = ''
port = 8080
backlog = 5
size = 1024

def printByteArray(byteArray):
    hexString = ''.join('%02x'%i for i in byteArray)
    return(' '.join(hexString[i:i+4] for i in range(0, len(hexString), 4)))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(backlog)
print('Listening on %s port %s' % (host, port))
while 1:
    client, address = s.accept()
    data = client.recv(size)
    if data:
        client.send(data)
        print('received: %s' % printByteArray(data))
    client.close()
