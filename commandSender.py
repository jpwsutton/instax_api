#!/usr/bin/env python

"""
A simple test client
"""
import socket
import sys


print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

host = ''
port = 8080

print("Instax API Command Sender")

def printByteArray(byteArray):
    hexString = ''.join('%02x'%i for i in byteArray)
    return(' '.join(hexString[i:i+4] for i in range(0, len(hexString), 4)))


def generatePayload(commandBit, mysteryInt, payloadArray, password):
    payload = bytearray() # The Command Packet is always 12 bytes
    payload.append(36 & 0xFF) # We always start with 36
    payload.append(commandBit & 0xFF) # Command Bit?
    payload.append((mysteryInt >> 8) & 0xFF) # Something else
    payload.append(mysteryInt & 0xFF) # Something else
    payload.append((payloadArray[0] >> 24) & 0xFF) # Something else
    payload.append((payloadArray[1] >> 16) & 0xFF) # Something else
    payload.append((payloadArray[2] >> 8) & 0xFF) # Something else
    payload.append(payloadArray[3] & 0xFF) # Something else
    payload.append((password >> 8) & 0xFF) # Password Shifted by 8
    payload.append(password & 0xFF) # Password
    payload.append(0) # Append Nothing
    payload.append(0) # Append Nothing
    print('Sending:  ' + printByteArray(payload))
    return payload

def sendAndRecv(payload):
    sock.sendall(payload)
    return(sock.recv(1024))

#Create a TCP/IP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))



try:
    response = sendAndRecv(generatePayload(192,50,[12,12,12,12],1111))
    print('Received: ' + printByteArray(response))

finally:
    print('Closing Socket')
    sock.close()
