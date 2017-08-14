#!/usr/bin/env python
import socket
from .commands import Commands
from .utilities import Utilities
from .packet import Packet


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
        self.packetFactory = PacketFactory()

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.backlog)
        print('Listening on %s port %s' % (self.host, self.port))
        while True:
            client, address = self.socket.accept()
            print('----------------------------------------------------------')
            header_data = client.recv(4)
            msg_len = ((header_data[2] & 0xFF) << 8 |
                       (header_data[3] & 0xFF) << 0)
            print('message length: ', msg_len)
            if msg_len:
                data = client.recv(msg_len - 4)
                payload = header_data + data
                client.send(payload)
                print('received: %s' % self.printByteArray(payload))
                packet = self.packetFactory.getPacket(payload)
                print('---------------------------------------------------')
            # client.close()

    def printByteArray(self, byteArray):
        hexString = ''.join('%02x' % i for i in byteArray)
        return(' '.join(hexString[i:i + 4] for i in range(
                0, len(hexString), 4)))

    # def generateResponse(self, cmdBit, time)
