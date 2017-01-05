from .utilities  import Utilities

class Commands:
    """Command Processing Class

    Contains methods to process the command specific output
    from each command.
    """

    def __init__(self):
        self.utilities = Utilities()
        pass

    """Test Command"""
    def getTestCommand(self):
        #return bytearray.fromhex('2ac0 0014 e759 eede 0457 0000 f700 0027 fad7 0d0a')
        return bytearray.fromhex('24c0 0010 e759 eede ffff 0000 fa01 0d0a')



    def generateCommand(self, currentTimeMillis, commandType, extraPayload, extraPayloadLength, pinCode):
        """ Takes Command arguments and packs them into a byteArray to be
            sent to the Instax SP-2.
        """
        commandPayloadLength = 16 + extraPayloadLength
        commandPayload = bytearray()
        commandPayload.append(36 & 0xFF) # Start of payload is 36
        commandPayload.append(commandType & 0xFF) # The Command bytes
        commandPayload.append((commandPayloadLength >> 8) & 0xFF) # Packet Length B1
        commandPayload.append((commandPayloadLength >> 0) & 0xFF) # Packet Length B2
        commandPayload.append((currentTimeMillis >> 24) & 0xFF) # TimeStamp B1
        commandPayload.append((currentTimeMillis >> 16) & 0xFF) # TimeStamp B2
        commandPayload.append((currentTimeMillis >> 8) & 0xFF)  # TimeStamp B3
        commandPayload.append((currentTimeMillis >> 0) & 0xFF)  # TimeStamp B4
        commandPayload.append((pinCode >> 8) & 0xFF) # Pin Code B1
        commandPayload.append((pinCode >> 0) & 0xFF) # Pin Code B2
        commandPayload.append(0) # Nothing
        commandPayload.append(0) # Nothing
        if(extraPayloadLength > 0):
            commandPayload = commandPayload + extraPayload
        # Generating the Checksum & End of payload
        checkSumIndex = 0
        checkSum = 0
        while(checkSumIndex < (commandPayloadLength - 4)):
            checkSum += (commandPayload[checkSumIndex] & 0xFF)
            checkSumIndex += 1
        commandPayload.append(((checkSum ^ -1) >> 8) & 0xFF)
        commandPayload.append(((checkSum ^ -1) >> 0) & 0xFF)
        commandPayload.append(13)
        commandPayload.append(10)
        return commandPayload

    def getCurrentTimeByteArray(self, currentTimeMillis):
        timeByteAray = bytearray()
        timeByteAray.append((currentTimeMillis >> 24) & 0xFF) # TimeStamp B1
        timeByteAray.append((currentTimeMillis >> 16) & 0xFF) # TimeStamp B2
        timeByteAray.append((currentTimeMillis >> 8) & 0xFF)  # TimeStamp B3
        timeByteAray.append((currentTimeMillis >> 0) & 0xFF)  # TimeStamp B4
        return timeByteAray



    def verifyResponse(self, byteArray, currentTimeMillis, commandType):
        """ Takes a response byteArray and verifies that it matches
            the correct currentTimeMillis, commandType and has a
            valid checksum.
        """
        startByte = (byteArray[0] & 0xFF)
        cmdByte = (byteArray[1] &0xFF)
        packetLength = ((byteArray[2] &0xFF) << 8 | (byteArray[3] &0xFF) << 0)
        responseTime = ((byteArray[4] &0xFF) << 24 | (byteArray[5] &0xFF) << 16 | (byteArray[6] &0xFF) << 8 | (byteArray[7] &0xFF) << 0)
        commandTimePacked = self.getCurrentTimeByteArray(currentTimeMillis)
        commandTime = ((commandTimePacked[0] &0xFF) << 24 | (commandTimePacked[1] &0xFF) << 16 | (commandTimePacked[2] &0xFF) << 8 | (commandTimePacked[3] &0xFF) << 0)
        returnCode = (byteArray[12] & 0xFF)
        print('Returncode was: %s' % returnCode)
        #print('Start Byte: %s' % startByte)
        #print('Command Byte: %s' % cmdByte)
        #print('Response Length: %s' % packetLength)
        #print('Response Time: %s' % responseTime)
        #print('Command Time: %s' % commandTime)
        #print('Return Code: %s' % returnCode)
        if((startByte == 42) and (responseTime == commandTime) and (commandType == cmdByte) and (len(byteArray) == packetLength) and (self.validateEndOfPayload(byteArray, packetLength))):
            return True
        else:
            return False



    def validateEndOfPayload(self, byteArray, packetLength):
        """ Validates that a payload ends correctly by
            checking the end bytes and the checksum.
        """
        checkSumIndex = 0
        checkSum = 0
        while(checkSumIndex < (packetLength - 4)):
            checkSum += (byteArray[checkSumIndex] & 0xFF)
            checkSumIndex += 1
        if ((byteArray[checkSumIndex + 2] == 13) and (byteArray[checkSumIndex + 3] == 10)):
            expectedCheckByte = (checkSum + (((byteArray[checkSumIndex] &0xFF) << 8) | ((byteArray[checkSumIndex+1] &0xFF) << 0)))
            if (expectedCheckByte & 65535) == 65535:
                return True
            else:
                return False
        else:
            return False



    #Command 193... something to do with facebook...
    def command193Processor(self, byteArray):
        firstValue = self.utilities.getFourByteInt(0, byteArray)
        facebookValue = self.utilities.getOneByteIntAt15(byteArray)
        print('FirstValue: %s ' % firstValue)
        print('Facebook: %s' % facebookValue)


    #Command 192
    def command192Processor(self, byteArray):
        printerFirmwareVersion = self.utilities.getTwoByteInt(2, byteArray)
        printerHardwareVersion = self.utilities.getTwoByteInt(4, byteArray)
        mysteryUnusedInt = self.utilities.getTwoByteInt(0, byteArray)
        print('Getting Cmd 192 ints..')
        print('Printer Firmware Version: Ver %s' % self.utilities.formatVersionNumber(printerFirmwareVersion))
        print('Printer Hardware Version: Ver %s' % self.utilities.formatVersionNumber(printerHardwareVersion))

    #Command 194
    def command194Processor(self, byteArray):
        printerModel = self.utilities.getPrinterModelString(byteArray)
        print('The Printer Model is: %s' % printerModel)



    #Command 196
    def command196Processor(byteArray):
        print('Getting Cmd 196 ints..')
        print(getTwoByteInt(2, byteArray))


    #Command 79
    def command79Processor(self, byteArray):
        print('Getting Cmd 79 ints..')
        print(self.utilities.getTwoByteInt(0, byteArray))
        print(self.utilities.getTwoByteInt(2, byteArray))
        print(self.utilities.getTwoByteInt(4, byteArray))
        print(self.utilities.getTwoByteInt(6, byteArray))
        print(self.utilities.getTwoByteInt(12, byteArray))
        print(self.utilities.getOneByteInt(14, byteArray))
        print(self.utilities.getFourByteInt(16, byteArray))


    #Command 198
    def command198Processor(byteArray):
        print('Getting Cmd 198 ints..')
        print(getTwoByteInt(0, byteArray))
        print(getOneByteInt(2, byteArray))
        print(getOneByteInt(3, byteArray))
        print(getTwoByteInt(4, byteArray))

    def command81Processor(byteArray):
        print('Getting Cmd 81 ints..')
        print()
