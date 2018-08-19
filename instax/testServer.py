"""
Fujifilm Instax-SP2 Server for testing.

James Sutton - 2017 - jsutton.co.uk
"""
import socket
from .packet import Packet, PacketFactory, SpecificationsCommand, \
    VersionCommand, PrintCountCommand, ModelNameCommand, PrePrintCommand, \
    PrinterLockCommand, ResetCommand, PrepImageCommand, SendImageCommand, \
    Type83Command, Type195Command, LockStateCommand
from .instaxImage import InstaxImage
import signal
import sys
import time
import json
import threading
import logging



class TestServer:
    """A Test Server for the Instax Library."""

    def __init__(self, host='0.0.0.0', port=8080,
                 dest="images", battery=2, remaining=10, total=20, version=2):
        """Initialise Server."""
        self.logger = logging.getLogger('instax_server')
        self.packetFactory = PacketFactory()
        self.host = host
        self.dest = dest
        self.port = port
        self.backlog = 5
        self.returnCode = Packet.RTN_E_RCV_FRAME
        self.ejecting = 0
        if version in [2,3]:
            self.version = version
        else:
            self.logger.warning("Invalid Instax SP version, defaulting to SP-2")
            self.version = 2
        self.printingState = 0
        self.battery = battery
        self.printCount = total
        self.remaining = remaining
        self.running = True
        self.finished = False
        self.messageLog = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        signal.signal(signal.SIGINT, self.signal_handler)
        self.imageMap = {}

    def start(self):
        """Start the Server."""
        self.socket.listen(self.backlog)
        self.logger.info(('Instax SP-%d Server Listening on %s port %s' % (self.version, self.host, self.port)))
        while True:
            client, address = self.socket.accept()
            client.settimeout(60)
            threading.Thread(target=self.listenToClient,
                             args=(client, address)).start()

    def listenToClient(self, client, address):
        """Interact with client."""
        self.logger.info('New Client Connected')
        length = None
        buffer = bytearray()
        while True:
            data = client.recv(70000)
            if not data:
                break
            buffer += data
            while True:
                if length is None:
                    length = ((buffer[2] & 0xFF) << 8 |
                              (buffer[3] & 0xFF) << 0)
                if len(buffer) < length:
                    break

                response = self.processIncomingMessage(buffer)
                client.send(response)
                buffer = bytearray()
                length = None
                break
        self.logger.info('Client Disconnected')

    def signal_handler(self, signal, frame):
        """Handle Ctrl+C events."""
        print('You pressed Ctrl+C! Saving Log and shutting down.')
        self.logger.info("Shutting down Server")
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = "instaxServer-" + timestr + ".json"
        self.logger.info("Saving Log to: %s" % filename)
        with open(filename, 'w') as outfile:
            json.dump(self.messageLog, outfile, indent=4)
        self.logger.info("Log file written, have a nice day!")
        sys.exit(0)

    def decodeImage(self, segments):
        """Decode an encoded image."""
        self.logger.info("Decoding Image of %s segments." % len(segments))
        combined = bytearray()
        for seg_key in range(len(segments)):
            combined += segments[seg_key]
        self.logger.info("Combined image is %s bytes long" % len(combined))
        instaxImage = InstaxImage(type=self.version)
        instaxImage.decodeImage(combined)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = timestr + ".bmp"
        instaxImage.saveImage(filename)
        self.logger.info("Saved image to: %s" % filename)

    def printByteArray(self, byteArray):
        """Print a Byte Array.

        Prints a Byte array in the following format: b1b2 b3b4...
        """
        hexString = ''.join('%02x' % i for i in byteArray)
        data = ' '.join(hexString[i:i + 4]
                        for i in range(0, len(hexString), 4))
        info = (data[:80] + '..') if len(data) > 80 else data
        return(info)

    def processIncomingMessage(self, payload):
        """Take an incoming message and return the response."""
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(payload)
        decodedPacketObj = decodedPacket.getPacketObject()
        self.messageLog.append(decodedPacketObj)
        self.logger.info("Processing message type: %s" % decodedPacket.NAME)
        response = None

        if(decodedPacket.TYPE == Packet.MESSAGE_TYPE_PRINTER_VERSION):
            response = self.processVersionCommand(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_SPECIFICATIONS):
            response = self.processSpecificationsCommand(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_MODEL_NAME):
            response = self.processModelNameCommand(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_PRINT_COUNT):
            response = self.processPrintCountCommand(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_PRE_PRINT):
            response = self.processPrePrintCommand(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_LOCK_DEVICE):
            response = self.processLockPrinterCommand(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_RESET):
            response = self.processResetCommand(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_PREP_IMAGE):
            response = self.processPrepImageCommand(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_SEND_IMAGE):
            response = self.processSendImageCommand(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_83):
            response = self.processType83Command(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_195):
            response = self.processType195Command(decodedPacket)
        elif(decodedPacket.TYPE == Packet.MESSAGE_TYPE_SET_LOCK_STATE):
            response = self.processSetLockStateCommand(decodedPacket)
        else:
            self.logger.info('Unknown Command. Failing!: ' + str(decodedPacket.TYPE))

        decodedResponsePacket = packetFactory.decode(response)
        self.messageLog.append(decodedResponsePacket.getPacketObject())
        return response

    def processVersionCommand(self, decodedPacket):
        """Process a version command."""
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = VersionCommand(Packet.MESSAGE_MODE_RESPONSE,
                                   unknown1=254,
                                   firmware=275,
                                   hardware=0)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting,
                                                   self.battery,
                                                   self.printCount)
        return encodedResponse

    def processSpecificationsCommand(self, decodedPacket):
        """Process a specifications command."""
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = SpecificationsCommand(Packet.MESSAGE_MODE_RESPONSE,
                                          maxHeight=800,
                                          maxWidth=600,
                                          maxColours=256,
                                          unknown1=10,
                                          maxMsgSize=60000,
                                          unknown2=16,
                                          unknown3=0)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting,
                                                   self.battery,
                                                   self.printCount)
        return encodedResponse

    def processModelNameCommand(self, decodedPacket):
        """Process a model name command."""
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = ModelNameCommand(Packet.MESSAGE_MODE_RESPONSE,
                                     modelName= ("SP-%d" % self.version))
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting,
                                                   self.battery,
                                                   self.printCount)
        return encodedResponse

    def processPrintCountCommand(self, decodedPacket):
        """Process a Print Count command."""
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = PrintCountCommand(Packet.MESSAGE_MODE_RESPONSE,
                                      printHistory=20)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting,
                                                   self.battery,
                                                   self.printCount)
        return encodedResponse

    def processPrePrintCommand(self, decodedPacket):
        """Process a Pre Print command."""
        cmdNumber = decodedPacket.payload['cmdNumber']
        if(cmdNumber in [6, 7, 8]):
            respNumber = 0
        elif(cmdNumber in [4, 5]):
            respNumber = 1
        elif(cmdNumber in [1, 2, 3]):
            respNumber = 2
        else:
            self.logger.warning("Unknown cmdNumber")
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
        """Process a Lock Printer Command."""
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = PrinterLockCommand(Packet.MESSAGE_MODE_RESPONSE)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting,
                                                   self.battery,
                                                   self.printCount)
        return encodedResponse

    def processResetCommand(self, decodedPacket):
        """Process a Rest command."""
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = ResetCommand(Packet.MESSAGE_MODE_RESPONSE)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting,
                                                   self.battery,
                                                   self.printCount)
        return encodedResponse

    def processPrepImageCommand(self, decodedPacket):
        """Process a Prep Image Commnand."""
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = PrepImageCommand(Packet.MESSAGE_MODE_RESPONSE,
                                     maxLen=60000)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting,
                                                   self.battery,
                                                   self.printCount)
        return encodedResponse

    def processSendImageCommand(self, decodedPacket):
        """Process a Send Image Command."""
        sessionTime = decodedPacket.header['sessionTime']
        sequenceNumber = decodedPacket.payload['sequenceNumber']
        payloadBytes = decodedPacket.payload['payloadBytes']
        resPacket = SendImageCommand(Packet.MESSAGE_MODE_RESPONSE,
                                     sequenceNumber=sequenceNumber)
        if sessionTime not in self.imageMap:
            self.imageMap[sessionTime] = {}
        self.imageMap[sessionTime][sequenceNumber] = payloadBytes
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting,
                                                   self.battery,
                                                   self.printCount)
        return encodedResponse

    def processType83Command(self, decodedPacket):
        """Process a Type 83 command."""
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = Type83Command(Packet.MESSAGE_MODE_RESPONSE)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting,
                                                   self.battery,
                                                   self.printCount)
        # Start a thread to decode the image
        imageSegments = self.imageMap[sessionTime]
        threading.Thread(target=self.decodeImage,
                         args=(imageSegments,)).start()
        return encodedResponse

    def processType195Command(self, decodedPacket):
        sessionTime = decodedPacket.header['sessionTime']
        returnCode = Packet.RTN_E_PRINTING
        if self.printingState == 100:
            returnCode = Packet.RTN_E_RCV_FRAME
            self.printingState = 0
        else:
            self.printingState += 25
        resPacket = Type195Command(Packet.MESSAGE_MODE_RESPONSE)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   returnCode,
                                                   self.ejecting,
                                                   self.battery,
                                                   self.printCount)
        return encodedResponse

    def processSetLockStateCommand(self, decodedPacket):
        """Process a Lock State Command."""
        unknownFourByteInt = 100
        sessionTime = decodedPacket.header['sessionTime']
        resPacket = LockStateCommand(Packet.MESSAGE_MODE_RESPONSE,
                                     unknownFourByteInt=unknownFourByteInt)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   self.returnCode,
                                                   self.ejecting,
                                                   self.battery,
                                                   self.printCount)
        return encodedResponse
