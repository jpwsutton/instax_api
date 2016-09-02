#!/usr/bin/env python

"""
A simple test client
"""
import socket

host = ''
port = 8080

print("Instax API Command Sender")

def printByteArray(byteArray):
    hexString = ''.join('%02x'%i for i in byteArray)
    print(' '.join(hexString[i:i+4] for i in range(0, len(hexString), 4)))


def sendCommand(commandBit, password):
    payload = bytearray() # The Command Packet is always 12 bytes
    payload.append(36 & 0xFF) # We always start with 36
    payload.append(commandBit & 0xFF) # Command Bit?
    payload.append(0) # Something else
    payload.append(0) # Something else
    payload.append(0) # Something else
    payload.append(0) # Something else
    payload.append(0) # Something else
    payload.append(0) # Something else
    payload.append((password >> 8) & 255) # Password Shifted by 8
    payload.append(password & 255) # Password
    payload.append(0) # Append Nothing
    payload.append(0) # Append Nothing
    printByteArray(payload)
    return payload

myPayload = sendCommand(192, 1111)
#Create a TCP/IP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

try:
    sock.sendall(myPayload)
    print(sock.recv(1024))

finally:
    print('Closing Socket')
    sock.close()
