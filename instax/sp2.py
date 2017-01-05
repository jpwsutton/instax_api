from .commands import Commands
from .comms import SocketClientThread, ClientCommand, ClientReply
import time
import queue
from .exceptions import CommandTimedOutException, ConnectError, CommandError
from .utilities  import Utilities

class SP2:
    'SP2 Control Class'

    def __init__(self):
        print("Initialising Instax SP-2 class")
        self.commands = Commands()
        self.utilities = Utilities()
        self.comms = SocketClientThread()
        self.comms.start()
        self.currentTimeMillis = int(round(time.time() * 1000))
        self.pinCode = 1111
        print('currentTimeMillis %s ' % self.currentTimeMillis)

    def connect(self, timeout=10):
        print("Connecting to Instax SP-2 with timeout of: " + str(timeout))
        self.comms.cmd_q.put(ClientCommand(ClientCommand.CONNECT, ['192.168.0.251', 8080]))
        # Get current time
        start = int(time.time())
        while(int(time.time()) < (start + timeout)):
            try:
                reply = self.comms.reply_q.get(False)
                if reply.type ==  ClientReply.SUCCESS:
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
                    if reply.type ==  ClientReply.SUCCESS:
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
        #statusBytes = self.commands.getTestCommand()
        getVersionBytes = self.commands.generateCommand(self.currentTimeMillis, 192, None, 0, self.pinCode)
        print("Sending:", self.utilities.printByteArray(getVersionBytes))
        reply = self.send_and_recieve(getVersionBytes, 5)
        print("Response Received", self.utilities.printByteArray(reply.data))
        if(self.commands.verifyResponse(reply.data, self.currentTimeMillis, 192)):
            self.commands.command192Processor(reply.data)
        else:
            print("The response failed verification")

    def getPrinterModel(self):
        print("Getting printer model... 194")
        mysteryCommandBytes = self.commands.generateCommand(self.currentTimeMillis, 194, None, 0, self.pinCode)
        print("Sending:", self.utilities.printByteArray(mysteryCommandBytes))
        reply = self.send_and_recieve(mysteryCommandBytes, 5)
        print("Response Received", self.utilities.printByteArray(reply.data))
        if(self.commands.verifyResponse(reply.data, self.currentTimeMillis, 194)):
            self.commands.command194Processor(reply.data)
        else:
            print("The response failed verification")


    def getCmd193(self):
        print("Getting the weird Facebook thing... 193")
        mysteryCommandBytes = self.commands.generateCommand(self.currentTimeMillis, 193, None, 0, self.pinCode)
        print("Sending:", self.utilities.printByteArray(mysteryCommandBytes))
        reply = self.send_and_recieve(mysteryCommandBytes, 5)
        print("Response Received", self.utilities.printByteArray(reply.data))
        if(self.commands.verifyResponse(reply.data, self.currentTimeMillis, 193)):
            self.commands.command193Processor(reply.data)
        else:
            print("The response failed verification")

    def getCmd79(self):
        print("Getting the next thing... 79")
        mysteryCommandBytes = self.commands.generateCommand(self.currentTimeMillis, 79, None, 0, self.pinCode)
        print("Sending:", self.utilities.printByteArray(mysteryCommandBytes))
        reply = self.send_and_recieve(mysteryCommandBytes, 5)
        print("Response Received", self.utilities.printByteArray(reply.data))
        if(self.commands.verifyResponse(reply.data, self.currentTimeMillis, 79)):
            self.commands.command79Processor(reply.data)
        else:
            print("The response failed verification")


    def sendPayload(self):
        print("Sending random payload")
        randomPayload = bytearray()
        randomPayload.append(42)
        randomPayload.append(42)
        randomPayload.append(42)
        randomPayload.append(42)
        statusBytes = self.commands.generateCommand(self.currentTimeMillis, 192, randomPayload, 4, self.pinCode)
        print("Sending:", self.utilities.printByteArray(statusBytes))
        reply = self.send_and_recieve(statusBytes, 5)
        print("Response Received", self.utilities.printByteArray(reply.data))


    def close(self, timeout=10):
        print("Closing connection to Instax SP2")
        self.comms.cmd_q.put(ClientCommand(ClientCommand.CLOSE))
        # Get current time
        start = int(time.time())
        while(int(time.time()) < (start + timeout)):
            try:
                reply = self.comms.reply_q.get(False)
                if reply.type ==  ClientReply.SUCCESS:
                    return
                else:
                    raise(ConnectError(reply.data))
            except queue.Empty:
                time.sleep(0.1)
                pass
        raise(CommandTimedOutException())
