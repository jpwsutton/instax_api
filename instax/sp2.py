"""Main SP2 Interface Class."""

from .comms import SocketClientThread, ClientCommand, ClientReply
import time
import queue
from .exceptions import CommandTimedOutException, ConnectError
from .packet import PacketFactory, Packet, SpecificationsCommand,  \
    VersionCommand, PrintCountCommand, ModelNameCommand, PrePrintCommand, \
    PrinterLockCommand, ResetCommand, PrepImageCommand, SendImageCommand, \
    Type83Command, Type195Command, LockStateCommand


class SP2:
    """SP2 Client interface."""

    def __init__(self, ip='192.168.0.251', port=8080,
                 timeout=10, pinCode=1111):
        """Initialise the client."""
        print("Initialising Instax SP-2 client")
        self.currentTimeMillis = int(round(time.time() * 1000))
        self.ip = ip
        self.port = port
        self.timeout = 10
        self.pinCode = pinCode
        print('currentTimeMillis %s ' % self.currentTimeMillis)
        self.packetFactory = PacketFactory()

    def connect(self):
        """Connect to a printer."""
        print("Connecting to Instax SP-2 with timeout of: %s" % self.timeout)
        self.comms = SocketClientThread()
        self.comms.start()
        self.comms.cmd_q.put(ClientCommand(ClientCommand.CONNECT,
                                           [self.ip, self.port]))
        # Get current time
        start = int(time.time())
        while(int(time.time()) < (start + self.timeout)):
            try:
                reply = self.comms.reply_q.get(False)
                if reply.type == ClientReply.SUCCESS:
                    return
                else:
                    raise(ConnectError(reply.data))
            except queue.Empty:
                time.sleep(0.1)
                pass
        raise(CommandTimedOutException())

    def send_and_recieve(self, cmdBytes, timeout):
        """Send a command and waits for a response.

        This is a blocking call and will not check that the response is
        the correct command type for the command.
        """
        self.comms.cmd_q.put(ClientCommand(ClientCommand.SEND, cmdBytes))
        self.comms.cmd_q.put(ClientCommand(ClientCommand.RECEIVE))

        # Get current time
        start = int(time.time())
        while(int(time.time()) < (start + timeout)):
            try:
                reply = self.comms.reply_q.get(False)
                if reply.data is not None:
                    if reply.type == ClientReply.SUCCESS:
                        return reply
                    else:
                        raise(ConnectError(reply.data))
            except queue.Empty:
                time.sleep(0.1)
                pass
        raise(CommandTimedOutException())

    def sendCommand(self, commandPacket):
        """Send a command packet and returns the response."""
        encodedPacket = commandPacket.encodeCommand(self.currentTimeMillis,
                                                    self.pinCode)
        decodedCommand = self.packetFactory.decode(encodedPacket)
        decodedCommand.printDebug()
        reply = self.send_and_recieve(encodedPacket, 5)
        decodedResponse = self.packetFactory.decode(reply.data)
        return decodedResponse

    def getPrinterVersion(self):
        """Get the version of the Printer hardware."""
        cmdPacket = VersionCommand(Packet.MESSAGE_MODE_COMMAND)
        response = self.sendCommand(cmdPacket)
        return response

    def getPrinterModelName(self):
        """Get the Model Name of the Printer."""
        cmdPacket = ModelNameCommand(Packet.MESSAGE_MODE_COMMAND)
        response = self.sendCommand(cmdPacket)
        return response

    def getPrintCount(self):
        """Get the historical number of prints."""
        cmdPacket = PrintCountCommand(Packet.MESSAGE_MODE_COMMAND)
        response = self.sendCommand(cmdPacket)
        return response

    def getPrinterSpecifications(self):
        """Get the printer specifications."""
        cmdPacket = SpecificationsCommand(Packet.MESSAGE_MODE_COMMAND)
        response = self.sendCommand(cmdPacket)
        return response

    def sendPrePrintCommand(self, cmdNumber):
        """Send a PrePrint Command."""
        cmdPacket = PrePrintCommand(Packet.MESSAGE_MODE_COMMAND,
                                    cmdNumber=cmdNumber)
        response = self.sendCommand(cmdPacket)
        return response

    def sendLockCommand(self, lockState):
        """Send a Lock State Commmand."""
        cmdPacket = PrinterLockCommand(Packet.MESSAGE_MODE_COMMAND,
                                       lockState=lockState)
        response = self.sendCommand(cmdPacket)
        return response

    def sendResetCommand(self):
        """Send a Reset Command."""
        cmdPacket = ResetCommand(Packet.MESSAGE_MODE_COMMAND)
        response = self.sendCommand(cmdPacket)
        return response

    def sendPrepImageCommand(self, format, options, imgLength):
        """Send a Prep for Image Command."""
        cmdPacket = PrepImageCommand(Packet.MESSAGE_MODE_COMMAND,
                                     format=format,
                                     options=options,
                                     imgLength=imgLength)
        response = self.sendCommand(cmdPacket)
        return response

    def sendSendImageCommand(self, sequenceNumber, payloadBytes):
        """Send an Image Segment Command."""
        cmdPacket = SendImageCommand(Packet.MESSAGE_MODE_COMMAND,
                                     sequenceNumber=sequenceNumber,
                                     payloadBytes=payloadBytes)
        response = self.sendCommand(cmdPacket)
        return response

    def sendT83Command(self):
        """Send a Type 83 Command."""
        cmdPacket = Type83Command(Packet.MESSAGE_MODE_COMMAND)
        response = self.sendCommand(cmdPacket)
        return response

    def sendT195Command(self):
        """Send a Type 195 Command."""
        cmdPacket = Type195Command(Packet.MESSAGE_MODE_COMMAND)
        response = self.sendCommand(cmdPacket)
        return response

    def sendLockStateCommand(self):
        """Send a LockState Command."""
        cmdPacket = LockStateCommand(Packet.MESSAGE_MODE_COMMAND)
        response = self.sendCommand(cmdPacket)
        return response

    def close(self, timeout=10):
        """Close the connection to the Printer."""
        print("Closing connection to Instax SP2")
        self.comms.cmd_q.put(ClientCommand(ClientCommand.CLOSE))
        # Get current time
        start = int(time.time())
        while(int(time.time()) < (start + timeout)):
            try:
                reply = self.comms.reply_q.get(False)
                if reply.type == ClientReply.SUCCESS:
                    self.comms.join()
                    self.comms = None
                    return
                else:
                    raise(ConnectError(reply.data))
            except queue.Empty:
                time.sleep(0.1)
                pass
        raise(CommandTimedOutException())
        self.comms.join()
        self.comms = None

    def getPrinterInformation(self):
        """Primary function to get SP-2 information."""
        self.connect()
        printerVersion = self.getPrinterVersion()
        printerModel = self.getPrinterModelName()
        printerSpecifications = self.getPrinterSpecifications()
        printCount = self.getPrintCount()
        printerInformation = {
            'version': printerVersion.payload,
            'model': printerModel.payload['modelName'],
            'specs': printerSpecifications.payload,
            'count': printCount.payload['printHistory']
        }
        self.close()
        return printerInformation

    def printPhoto(self, imageBytes):
        """Print a Photo to the Printer."""
        # Send Pre Print Commands
        self.connect()
        for x in range(1, 9):
            prePrintCmd = self.sendPrePrintCommand(x)
            print("PrePrint - C: %s, R: %s" % (x, prePrintCmd.respNumber))
        self.close()

        # Lock The Printer
        time.sleep(1)
        self.connect()
        self.sendLockCommand(1)
        self.close()

        # Reset the Printer
        time.sleep(1)
        self.connect()
        self.sendResetCommand()
        self.close()

        # Send the Image
        time.sleep(1)
        self.connect()
        self.sendPrepImageCommand(16, 0, 1440000)
        for segment in range(24):
            start = segment * 60000
            end = start + 60000
            segmentBytes = imageBytes[start:end]
            self.sendSendImageCommand(segment, bytes(segmentBytes))
        self.sendT83Command()
        self.close()

        # Send Print State Req
        time.sleep(1)
        self.connect()
        printStateCmd = self.sendLockStateCommand()
        if(printStateCmd.header['returnCode'] in [Packet.RTN_E_PRINTING,
                                                  Packet.RTN_E_EJECTING]):
            # Print has started, poll for status
            printComplete = self.checkPrintStatus(30)
            print("Print Complete: %s" % printComplete)
        else:
            print("Doesn't seem to be printing...")

        # Check the status of the print
        time.sleep(1)
        self.connect()
        t195Cmd = self.sendT195Command()
        t195Cmd.printDebug()
        self.close()

    def checkPrintStatus(self, timeout=30):
        """Check the status of a print."""
        for x in range(timeout):
            printStateCmd = self.sendLockStateCommand()
            if printStateCmd.header['returnCode'] is Packet.RTN_E_RCV_FRAME:
                return True
            else:
                time.sleep(1)
        return False
