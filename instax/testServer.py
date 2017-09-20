"""
Fujifilm Instax-SP2 Server for testing.

James Sutton - 2017 - jsutton.co.uk
"""
import socket
from .packet import Packet, PacketFactory, SpecificationsCommand, \
    VersionCommand, PrintCountCommand, ModelNameCommand, PrePrintCommand, \
    PrinterLockCommand, ResetCommand, PrepImageCommand, SendImageCommand
from pprint import pprint


class TestServer:
    """A Test Server for the Instax Library."""

    def __init__(self, verbose=False, log=None, host='0.0.0.0', port=8080,
                 dest="images", battery=2, remaining=10, total=20):
        """Initialise Server."""
        self.packetFactory = PacketFactory()
        self.host = host
        self.verbose = verbose
        self.log = log
        self.dest = dest
        self.port = port
        self.backlog = 5
        self.returnCode = Packet.RTN_E_RCV_FRAME
        self.ejecting = 0
        self.battery = battery
        self.printCount = total
        self.remaining = remaining

    def start(self):
        """Start the Server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.backlog)
        print(('Server Listening on %s port %s' % (self.host, self.port)))
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
                        print(('sending: %s' % self.printByteArray(response)))
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
        decodedPacketObj = decodedPacket.getPacketObject()
        print("****************************************")
        pprint(decodedPacketObj)
        print("****************************************")

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
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_LOCK_DEVICE):
            return self.processLockPrinterCommand(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_RESET):
            return self.processResetCommand(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_PREP_IMAGE):
            return self.processPrepImageCommand(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_SEND_IMAGE):
            return self.processSendImageCommand(decodedPacket)
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
        if(cmdNumber in [6, 7, 8]):
            respNumber = 0
        elif(cmdNumber in [4, 5]):
            respNumber = 1
        elif(cmdNumber in [1, 2, 3]):
            respNumber = 2
        else:
            print("Unknown cmdNumber")
            respNumber = 0
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = PrePrintCommand(Packet.MESSAGE_MODE_RESPONSE,
                                    cmdNumber=cmdNumber,
                                    respNumber=respNumber)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting,
                                                   self.battery,
                                                   self.printCount)
        return encodedResponse

    def processLockPrinterCommand(self, decodedPacket):
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = PrinterLockCommand(Packet.MESSAGE_MODE_RESPONSE)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting, self.battery,
                                                   self.printCount)
        return encodedResponse

    def processResetCommand(self, decodedPacket):
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = ResetCommand(Packet.MESSAGE_MODE_RESPONSE)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting, self.battery,
                                                   self.printCount)
        return encodedResponse

    def processPrepImageCommand(self, decodedPacket):
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = PrepImageCommand(Packet.MESSAGE_MODE_RESPONSE,
                                     maxLen=60000)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting, self.battery,
                                                   self.printCount)
        return encodedResponse

    def processSendImageCommand(self, decodedPacket):
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = SendImageCommand(Packet.MESSAGE_MODE_RESPONSE,
                                     maxLen=60000)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting, self.battery,
                                                   self.printCount)
        return encodedResponse
