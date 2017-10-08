from .comms import SocketClientThread, ClientCommand, ClientReply
import time
import queue
from .exceptions import CommandTimedOutException, ConnectError, CommandError
from .response import ResponseCode
from .packet import PacketFactory, Packet, SpecificationsCommand,  \
    VersionCommand, PrintCountCommand, ModelNameCommand, PrePrintCommand, \
    PrinterLockCommand, ResetCommand, PrepImageCommand


class SP2:

    'SP2 Control Class'

    def __init__(self):
        print("Initialising Instax SP-2 class")
        self.comms = SocketClientThread()
        self.comms.start()
        self.currentTimeMillis = int(round(time.time() * 1000))
        self.pinCode = 1111
        print('currentTimeMillis %s ' % self.currentTimeMillis)
        self.packetFactory = PacketFactory()

    def connect(self, ip='192.168.0.251', port=8080, timeout=10):
        print("Connecting to Instax SP-2 with timeout of: " + str(timeout))
        self.comms.cmd_q.put(ClientCommand(ClientCommand.CONNECT, [ip, port]))
        # Get current time
        start = int(time.time())
        while(int(time.time()) < (start + timeout)):
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
        """ Sends a command and waits for a response
            to be sent back. This is a blocking call
            and will not check that the response is
            the correct command type for the command.
        """
        self.comms.cmd_q.put(ClientCommand(ClientCommand.SEND, cmdBytes))
        self.comms.cmd_q.put(ClientCommand(ClientCommand.RECEIVE))

        # Get current time
        start = int(time.time())
        while(int(time.time()) < (start + timeout)):
            try:
                reply = self.comms.reply_q.get(False)
                if reply.data != None:
                    if reply.type == ClientReply.SUCCESS:
                        return reply
                    else:
                        raise(ConnectError(reply.data))
            except queue.Empty:
                time.sleep(0.1)
                pass
        raise(CommandTimedOutException())

    def getPrinterVersion(self):
        print("Getting the Printer version... 192")
        # Get ByteArray for Getting Status command
        getVersionBytes = self.commands.generateCommand(
            self.currentTimeMillis, 192, None, 0, self.pinCode)
        print("Sending:  ", self.utilities.printByteArray(getVersionBytes))
        reply = self.send_and_recieve(getVersionBytes, 5)
        print("Response: ", self.utilities.printByteArray(reply.data))
        response = self.commands.processResponse(
            reply.data, self.currentTimeMillis, 192)
        if(response.responseCode == ResponseCode.RET_OK):
            return response
        else:
            print("The response failed verification")

    def getPrinterModel(self):
        print("Getting printer model... 194")
        getModelBytes = self.commands.generateCommand(self.currentTimeMillis, 194, None, 0, self.pinCode)
        print("Sending: ", self.utilities.printByteArray(getModelBytes))
        reply = self.send_and_recieve(getModelBytes, 5)
        print("Response: ", self.utilities.printByteArray(reply.data))
        response = self.commands.processResponse(
            reply.data, self.currentTimeMillis, 194)
        if(response.responseCode == ResponseCode.RET_OK):
            return response
        else:
            print("The response failed verification")

    def getPrintCount(self):
        print("Getting print count... 193")
        printCountBytes = self.commands.generateCommand(self.currentTimeMillis, 193, None, 0, self.pinCode)
        print("Sending: ", self.utilities.printByteArray(printCountBytes))
        reply = self.send_and_recieve(printCountBytes, 5)
        print("Response: ", self.utilities.printByteArray(reply.data))
        response = self.commands.processResponse(
            reply.data, self.currentTimeMillis, 193)
        if(response.responseCode == ResponseCode.RET_OK):
            return response
        else:
            print("The response failed verification")

    def getPrinterSpecifications(self):
        print("Getting printer specification... 79")
        cmdPacket = SpecificationsCommand(PacketFactory.MESSAGE_MODE_COMMAND)
        encodedPacket = cmdPacket.encodeCommand(self.currentTimeMillis,
                                                self.pinCode)
        reply = self.send_and_recieve(encodedPacket, 5)
        decodedResponse = self.packetFactory.decode(reply.data)
        return decodedResponse

    def sendPrePrintCommand(self, cmdNumber):
        """Send a PrePrint Command."""
        cmdPacket = PrePrintCommand(Packet.MESSAGE_MODE_COMMAND, cmdNumber=cmdNumber)
        encodedPacket = cmdPacket.encodeCommand(self.currentTimeMillis,
                                                self.pinCode)
        reply = self.send_and_recieve(encodedPacket, 5)
        decodedResponse = self.packetFactory.decode(reply.data)
        return decodedResponse

    def close(self, timeout=10):
        print("Closing connection to Instax SP2")
        self.comms.cmd_q.put(ClientCommand(ClientCommand.CLOSE))
        # Get current time
        start = int(time.time())
        while(int(time.time()) < (start + timeout)):
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
