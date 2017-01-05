#!/usr/bin/env python
import socket
from .commands import Commands
from .utilities  import Utilities

class TestServer:
    """ A Test Server for the Instax Library,
        Simply returns dummy responses of the
        correct type.
    """

    def __init__(self):
        print("Instax API EchoServer")
        self.host = ''
        self.port = 8080
        self.backlog = 5


    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.backlog)
        print('Listening on %s port %s' % (self.host, self.port))
        while 1:
            client, address = self.socket.accept()
            print('-----------------------------------------------------------')
            header_data = client.recv(4)
            msg_len = ((header_data[2] &0xFF) << 8 | (header_data[3] &0xFF) << 0)
            print('message length: ',  msg_len)
            if msg_len:
                data = client.recv(msg_len - 4)
                payload = header_data + data
                client.send(payload)
                print('received: %s' % self.printByteArray(payload))
                self.processIncomingCommand(payload)
                print('-----------------------------------------------------------')
            #client.close()


    def printByteArray(self, byteArray):
        hexString = ''.join('%02x'%i for i in byteArray)
        return(' '.join(hexString[i:i+4] for i in range(0, len(hexString), 4)))

    #def generateResponse(self, cmdBit, time)


    def processIncomingCommand(self, byteArray):
        print("Processing incoming command...")
        startBit = (byteArray[0] & 0xFF)
        cmdBit = (byteArray[1] &0xFF)
        packetLength = ((byteArray[2] &0xFF) << 8 | (byteArray[3] &0xFF) << 0)
        time = ((byteArray[4] &0xFF) << 24 | (byteArray[5] &0xFF) << 16 | (byteArray[6] &0xFF) << 8 | (byteArray[7] &0xFF) << 0)
        pinCode = ((byteArray[8] &0xFF) << 8 | (byteArray[9] &0xFF) << 0)
        extraPayloadLength = 0
        extraPayload = bytearray()
        if(packetLength > 16):
            # This command has an extra payload!
            extraPayloadLength = packetLength - 16
            startIndex = 12
            endIndex = startIndex + extraPayloadLength
            extraPayload = byteArray[startIndex:endIndex]

        print('Start Bit (0)         : ' + str(startBit))
        print('Command Bit (1)       : ' + str(cmdBit))
        print('Packet Length (2 & 3) : ' + str(packetLength) + ' bytes')
        print('Time        (4,5,6,7) : ' + str(time))
        print('Pin Code    (8, 9)    : ' + str(pinCode))
        print('Null Bits   (10, 11)  : 0,0')
        if(extraPayloadLength > 0):
            print('Extra Payload! Length: %s, Payload: %s' %(extraPayloadLength, self.printByteArray(extraPayload)))
        if(self.validatePayload(byteArray, packetLength)):
            print("Valid Packet!")
        else:
            print("Invalid Packet!")


    def validatePayload(self, byteArray, payloadLength):
        """ This method will validate that a command packet
            is correct by performing a checksum on the
            payload. May work for responses too....
        """
        sumOfBytes = 0;
        countOfBytes = 0;
        while countOfBytes < (payloadLength - 4):
            sumOfBytes += (byteArray[countOfBytes] &0xFF)
            countOfBytes += 1
        if((byteArray[countOfBytes + 2] == 13) and (byteArray[countOfBytes + 3] == 10)):
            expectedCheckByte = (sumOfBytes + (((byteArray[countOfBytes] &0xFF) << 8) | ((byteArray[countOfBytes+1] &0xFF) << 0)))
            if (expectedCheckByte & 65535) != 65535:
                print('Invalid Checksum')
                return False
            else:
                return True
        else:
            print('Invalid end bytes')
            return False
