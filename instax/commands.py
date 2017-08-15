from .utilities  import Utilities
from .response import Response, ResponseCode, PrinterStatus


class Commands:
    """Command Processing Class

    Contains methods to process the command specific output
    from each command.
    """

    def __init__(self):
        self.utilities = Utilities()
        pass


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



    def processResponse(self, byteArray, currentTimeMillis, commandType):
        """ Takes a response byteArray and verifies that it matches
            the correct currentTimeMillis, commandType and has a
            valid checksum. Will return a response Object containing
            the raw payload, and the response codes.
        """

        startByte = (byteArray[0] & 0xFF)
        cmdByte = (byteArray[1] &0xFF)
        packetLength = ((byteArray[2] &0xFF) << 8 | (byteArray[3] &0xFF) << 0)
        responseTime = ((byteArray[4] &0xFF) << 24 | (byteArray[5] &0xFF) << 16 | (byteArray[6] &0xFF) << 8 | (byteArray[7] &0xFF) << 0)
        commandTimePacked = self.getCurrentTimeByteArray(currentTimeMillis)
        commandTime = ((commandTimePacked[0] &0xFF) << 24 | (commandTimePacked[1] &0xFF) << 16 | (commandTimePacked[2] &0xFF) << 8 | (commandTimePacked[3] &0xFF) << 0)
        returnCode = (byteArray[12] & 0xFF)
        if((startByte == 42) and (responseTime == commandTime) and (commandType == cmdByte) and (len(byteArray) == packetLength) and (self.validateEndOfPayload(byteArray, packetLength))):
            # The payload is technically valid, extract the payload appropriately
            if(cmdByte == 79):
                paylaod = self.command79Processor(byteArray)
            elif(cmdByte == 80):
                # No Payload
                payload = {}
            elif(cmdByte == 81):
                payload = self.command81Processor(byteArray)
            elif(cmdByte == 82):
                payload = self.command82Processor(byteArray)
            elif(cmdByte == 176):
                payload = self.command176Processor(byteArray)
            elif(cmdByte == 182):
                payload = self.command182Processor(byteArray)
            elif(cmdByte == 192):
                payload = self.command192Processor(byteArray)
            elif(cmdByte == 193):
                payload = self.command193Processor(byteArray)
            elif(cmdByte == 194):
                payload = self.command194Processor(byteArray)
            elif(cmdByte == 196):
                payload = self.command196Processor(byteArray)
            response = Response(byteArray, payload,ResponseCode.RET_OK, PrinterStatus.IDLE, )
        else:
            response = Response(byteArray, NULL, ResponseCode.E_RCV_FRAME, PrinterStatus.IDLE)

        return response



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


    def command79Processor(self, byteArray):
        """
        Command 79 - Return Printer Specifications
        """
        maxHeight  = self.utilities.getTwoByteInt(0, byteArray)
        maxWidth   = self.utilities.getTwoByteInt(2, byteArray)
        maxColours = self.utilities.getTwoByteInt(4, byteArray)
        unknown1   = self.utilities.getTwoByteInt(6, byteArray)
        maxMsgSize = self.utilities.getTwoByteInt(12, byteArray)
        unknown2   = self.utilities.getOneByteInt(14, byteArray)
        unknown3   = self.utilities.getFourByteInt(16, byteArray)
        payload = {
            'maxHeight' : maxHeight,
            'maxWidth'  : maxWidth,
            'maxColours': maxColours,
            'unknown1'  : unknown1,
            'maxMsgSize': maxMsgSize,
            'unknown2'  : unknown2,
            'unknown3'  : unknown3
        }
        return payload

    def command81Processor(byteArray):
        """
        Command 81 - Prepare for Image
        """
        maxImageSize = self.utilities.getTwoByteInt(2, byteArray)
        payload = {
            'maxImageSize' : maxImageSize
        }
        return payload

    # Command 82 - Send Image
    def command82Processor(byteArray):
        payload = {}
        return payload

    # Command 176 - Lock / Unlock Printer
    def command176Processor(byteArray):
        payload = {}
        return payload

    # Command 182 - Send Image
    def command182Processor(byteArray):
        payload = {}
        return payload

    def command192Processor(self, byteArray):
        """
        Command 192 - Firmware / Hardware Version
        """
        printerFirmwareVersion = self.utilities.getTwoByteInt(2, byteArray)
        printerHardwareVersion = self.utilities.getTwoByteInt(4, byteArray)
        mysteryUnusedInt = self.utilities.getTwoByteInt(0, byteArray)
        payload = {
            'firmwareVer' : self.utilities.formatVersionNumber(printerFirmwareVersion),
            'hardwareVer' : self.utilities.formatVersionNumber(printerHardwareVersion)
        }
        return payload

    def command193Processor(self, byteArray):
        """
        Command 193 - Print Count
        """
        printCount = self.utilities.getFourByteInt(0, byteArray)
        battLevel = self.utilities.getBatteryLevel(byteArray)
        payload = {
            'battLevel' : battLevel,
            'printCount' : printCount
        }
        return payload

    def command194Processor(self, byteArray):
        """
        Command 194 - Model Name
        """
        printerModel = self.utilities.getPrinterModelString(byteArray)
        payload = {
            'modelName' : printerModel
        }
        return payload

    # Command 196 -Unknown
    def command196Processor(byteArray):
        unknown = getTwoByteInt(2, byteArray)
        payload = {
            'unknown' : unknown
        }
        return payload

    # Command 198 - Unknown
    def command198Processor(byteArray):
        unknown1 = getTwoByteInt(0, byteArray)
        unknown2 = getOneByteInt(2, byteArray)
        unknown3 = getOneByteInt(3, byteArray)
        unknown4 = getTwoByteInt(4, byteArray)
        payload = {
            '1' : unknown1,
            '2' : unknown2,
            '3' : unknown3,
            '4' : unknown4,
        }
        return payload
