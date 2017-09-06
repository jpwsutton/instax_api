#!/usr/bin/env python
import socket
from .packet import Packet, PacketFactory, SpecificationsCommand, \
    VersionCommand, PrintCountCommand, ModelNameCommand, PrePrintCommand


class TestServer:
    """ A Test Server for the Instax Library,
        Simply returns dummy responses of the
        correct type.
    #"""

    def __init__(self):
        print("Instax API EchoServer")
        self.host = ''
        self.port = 8080
        self.backlog = 5
        self.packetFactory = PacketFactory()

        self.returnCode = Packet.RTN_E_RCV_FRAME
        self.ejecting = 0
        self.battery = 2
        self.printCount = 7

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.backlog)
        print(('Listening on %s port %s' % (self.host, self.port)))
        while True:
            client, address = self.socket.accept()
            while True:
                header_data = client.recv(4)
                if(len(header_data) > 1):
                    print('--------------------------------------------------')
                    print(('len: %s' % len(header_data)))
                    print(('header: %s' % self.printByteArray(header_data)))
                    msg_len = ((header_data[2] & 0xFF) << 8 |
                               (header_data[3] & 0xFF) << 0)
                    print(('message length: ', msg_len))
                    if msg_len:
                        data = client.recv(msg_len - 4)
                        payload = header_data + data
                        print(('received: %s' % self.printByteArray(payload)))
                        response = self.processIncomingMessage(payload)
                        client.send(response)
                    print('--------------------------------------------------')
                else:
                    print('No data, closing client')
                    client.close()
                    break

    def printByteArray(self, byteArray):
        hexString = ''.join('%02x' % i for i in byteArray)
        return(' '.join(hexString[i:i + 4] for i in range(
                0, len(hexString), 4)))

    def processIncomingMessage(self, payload):
        """Takes an incoming message and returns the response"""
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(payload)
        decodedPacket.printDebug()

        if(decodedPacket.TYPE == Packet.MESSAGE_TYPE_PRINTER_VERSION):
            return self.processVersionCommand(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_SPECIFICATIONS):
            return self.processSpecificationsCommand(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_MODEL_NAME):
            return self.processModelNameCommand(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_PRINT_COUNT):
            return self.processPrintCountCommand(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_PRE_PRINT):
            return self.processPrePrintCommand(decodedPacket)
        else:
            print('Unknown Command. Failing!')

    def processVersionCommand(self, decodedPacket):
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = VersionCommand(Packet.MESSAGE_MODE_RESPONSE,
                                   unknown1=254,
                                   firmware=275,
                                   hardware=0)
        encodedResponse = resPacket.encodeResponse(sessionTime, self.returnCode,
                                                   self.ejecting, self.battery,
                                                   self.printCount)
        return encodedResponse

    def processSpecificationsCommand(self, decodedPacket):
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = SpecificationsCommand(Packet.MESSAGE_MODE_RESPONSE,
                                          maxHeight=800,
                                          maxWidth=600,
                                          maxColours=256,
                                          unknown1=10,
                                          maxMsgSize=60000,
                                          unknown2=16,
                                          unknown3=0)
        encodedResponse = resPacket.encodeResponse(sessionTime, self.returnCode,
                                                   self.ejecting, self.battery,
                                                   self.printCount)
        return encodedResponse

    def processModelNameCommand(self, decodedPacket):
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = ModelNameCommand(Packet.MESSAGE_MODE_RESPONSE,
                                     modelName='SP-2')
        encodedResponse = resPacket.encodeResponse(sessionTime, self.returnCode,
                                                   self.ejecting, self.battery,
                                                   self.printCount)
        return encodedResponse

    def processPrintCountCommand(self, decodedPacket):
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = PrintCountCommand(Packet.MESSAGE_MODE_RESPONSE,
                                      printHistory=20)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting, self.battery,
                                                   self.printCount)
        return encodedResponse

    def processPrePrintCommand(self, decodedPacket):
        cmdNumber = decodedPacket.payload['cmdNumber']
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = PrePrintCommand(Packet.MESSAGE_MODE_RESPONSE,
                                    cmdNumber=cmdNumber,
                                    respNumber=1)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting,
                                                   self.battery,
                                                   self.printCount)
        return encodedResponse
