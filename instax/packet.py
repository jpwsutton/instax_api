"""Fujifilm Instax SP-2 Packet Library.

This packet library can be used to encode and decode packets to be sent to
or recieved from a Fujifilm Instax SP-2. It is designed to be used with the
instax_api Python Library.
"""


class PacketFactory(object):
    """Packet Factory.

    Used to generate new pakcets and to decode existing packets.
    """

    MESSAGE_TYPE_SPECIFICATIONS = 79
    MESSAGE_TYPE_RESET = 80
    MESSAGE_TYPE_PREP_IMAGE = 81
    MESSAGE_TYPE_SEND_IMAGE = 82
    MESSAGE_TYPE_83 = 83
    MESSAGE_TYPE_SET_LOCK_STATE = 176
    MESSAGE_TYPE_LOCK_DEVICE = 179
    MESSAGE_TYPE_CHANGE_PASSWORD = 182
    MESSAGE_TYPE_PRINTER_VERSION = 192
    MESSAGE_TYPE_PRINT_COUNT = 193
    MESSAGE_TYPE_MODEL_NAME = 194
    MESSAGE_TYPE_195 = 195
    MESSAGE_TYPE_PRE_PRINT = 196

    MESSAGE_MODE_COMMAND = 36  # Command from Client
    MESSAGE_MODE_RESPONSE = 42  # Response from Server

    def __init__(self):
        """Init for Packet Factory."""
        pass

    def printRawByteArray(self, byteArray):
        """Print a byte array fully."""
        hexString = ''.join('%02x' % i for i in byteArray)
        return(' '.join(hexString[i:i + 4] for i in range(
            0, len(hexString), 4)))

    def decode(self, byteArray):
        """Decode a byte array into an instax Packet."""
        self.byteArray = byteArray
        # Get first two bytes as they will help identify the type of packet
        self.mode = byteArray[0]
        pType = byteArray[1]

        # Identify the type of packet and hand over to that packets class
        if pType == self.MESSAGE_TYPE_SPECIFICATIONS:
            return(SpecificationsCommand(mode=self.mode, byteArray=byteArray))
        elif pType == self.MESSAGE_TYPE_PRINTER_VERSION:
            return(VersionCommand(mode=self.mode, byteArray=byteArray))
        elif pType == self.MESSAGE_TYPE_PRINT_COUNT:
            return(PrintCountCommand(mode=self.mode, byteArray=byteArray))
        elif pType == self.MESSAGE_TYPE_RESET:
            return(ResetCommand(mode=self.mode, byteArray=byteArray))
        elif pType == self.MESSAGE_TYPE_PREP_IMAGE:
            return(PrepImageCommand(mode=self.mode, byteArray=byteArray))
        elif pType == self.MESSAGE_TYPE_SEND_IMAGE:
            return(SendImageCommand(mode=self.mode, byteArray=byteArray))
        elif pType == self.MESSAGE_TYPE_MODEL_NAME:
            return(ModelNameCommand(mode=self.mode, byteArray=byteArray))
        elif pType == self.MESSAGE_TYPE_PRE_PRINT:
            return(PrePrintCommand(mode=self.mode, byteArray=byteArray))
        elif pType == self.MESSAGE_TYPE_LOCK_DEVICE:
            return(PrinterLockCommand(mode=self.mode, byteArray=byteArray))
        elif pType == self.MESSAGE_TYPE_83:
            return(Type83Command(mode=self.mode, byteArray=byteArray))
        elif pType == self.MESSAGE_TYPE_195:
            return(Type195Command(mode=self.mode, byteArray=byteArray))
        elif pType == self.MESSAGE_TYPE_SET_LOCK_STATE:
            return(LockStateCommand(mode=self.mode, byteArray=byteArray))
        else:
            print("Unknown Packet Type: " + str(pType))
            print("Packet Bytes: [" + self.printRawByteArray(byteArray) + "]")


class Packet(object):
    """Base Packet Class."""

    MESSAGE_TYPE_SPECIFICATIONS = 79
    MESSAGE_TYPE_RESET = 80
    MESSAGE_TYPE_PREP_IMAGE = 81
    MESSAGE_TYPE_SEND_IMAGE = 82
    MESSAGE_TYPE_83 = 83
    MESSAGE_TYPE_SET_LOCK_STATE = 176
    MESSAGE_TYPE_LOCK_DEVICE = 179
    MESSAGE_TYPE_CHANGE_PASSWORD = 182
    MESSAGE_TYPE_PRINTER_VERSION = 192
    MESSAGE_TYPE_PRINT_COUNT = 193
    MESSAGE_TYPE_MODEL_NAME = 194
    MESSAGE_TYPE_195 = 195
    MESSAGE_TYPE_PRE_PRINT = 196

    MESSAGE_MODE_COMMAND = 36  # Command from Client
    MESSAGE_MODE_RESPONSE = 42  # Response from Server

    RTN_E_RCV_FRAME = 0
    RTN_E_PI_SENSOR = 248
    RTN_E_UNMATCH_PASS = 247
    RTN_E_MOTOR = 246
    RTN_E_CAM_POINT = 245
    RTN_E_FILM_EMPTY = 244
    RTN_E_RCV_FRAME_1 = 243
    RTN_E_RCV_FRAME_2 = 242
    RTN_E_RCV_FRAME_3 = 241
    RTN_E_RCV_FRAME_4 = 240
    RTN_E_CONNECT = 224
    RTN_E_CHARGE = 180
    RTN_E_TESTING = 165
    RTN_E_EJECTING = 164
    RTN_E_PRINTING = 163  # ST_PRINT
    RTN_E_BATTERY_EMPTY = 162
    RTN_E_NOT_IMAGE_DATA = 161
    RTN_E_OTHER_USED = 160
    RTN_ST_UPDATE = 127  # RET_HOLD

    strings = {
        MESSAGE_MODE_COMMAND: "Command",
        MESSAGE_MODE_RESPONSE: "Response"
    }

    def __init__(self, mode=None):
        """Init for Packet."""
        pass

    def printByteArray(self, byteArray):
        """Print a Byte Array.

        Prints a Byte array in the following format: b1b2 b3b4...
        """
        hexString = ''.join('%02x' % i for i in byteArray)
        data = ' '.join(hexString[i:i + 4]
                        for i in range(0, len(hexString), 4))
        info = (data[:80] + '..') if len(data) > 80 else data
        return(info)

    def printRawByteArray(self, byteArray):
        """Print a byte array fully."""
        hexString = ''.join('%02x' % i for i in byteArray)
        return(' '.join(hexString[i:i + 4] for i in range(
            0, len(hexString), 4)))

    def printDebug(self):
        """Print Debug information about packet."""
        print("-------------------------------------------------------------")
        print("Bytes: %s" % (self.printByteArray(self.byteArray)))
        print("Mode:  %s" % (self.strings[self.mode]))
        print("Type:  %s" % (self.NAME))
        print("Valid: %s" % (self.valid))
        print("Header:")
        print("    Start Byte: %s" % (self.header['startByte']))
        print("    Command: %s" % (self.header['cmdByte']))
        print("    Packet Length: %s" % (self.header['packetLength']))
        print("    Session Time: %s" % (self.header['sessionTime']))
        if(self.mode == self.MESSAGE_MODE_COMMAND):
            print("    Password: %s" % (self.header['password']))
        elif(self.mode == self.MESSAGE_MODE_RESPONSE):
            print("    Return Code: %s" % (self.header['returnCode']))
            print("    Unknown 1: %s" % (self.header['unknown1']))
            print("    Ejecting: %s" % (self.header['ejecting']))
            print("    Battery: %s" % (self.header['battery']))
            print("    Prints Left: %s" % (self.header['printCount']))

        if len(self.payload) == 0:
            print("Payload: None")
        else:
            print("Payload:")
            for key in self.payload:
                if(key == 'payloadBytes'):
                    print("    payloadBytes: (length: %s) : [%s]" %
                          (str(len(self.payload[key])),
                           self.printByteArray(self.payload[key])))
                else:
                    print("    %s : %s" % (key, self.payload[key]))
        print("-------------------------------------------------------------")
        print()

    def getPacketObject(self):
        """Return a simple object containing all packet details."""
        packetObj = {}
        packetObj['bytes'] = self.printByteArray(self.byteArray)
        packetObj['header'] = self.header
        packetPayload = {}
        for key in self.payload:
            if(key == 'payloadBytes'):
                packetPayload['payloadBytes'] = self.printByteArray(
                    self.payload[key])
            else:
                packetPayload[key] = self.payload[key]
        packetObj['payload'] = packetPayload
        return packetObj

    def decodeHeader(self, mode, byteArray):
        """Decode packet header."""
        startByte = self.getOneByteInt(0, byteArray)
        cmdByte = self.getOneByteInt(1, byteArray)
        packetLength = self.getTwoByteInt(2, byteArray)
        responseTime = self.getFourByteInt(4, byteArray)
        header = {
            'startByte': startByte,
            'cmdByte': cmdByte,
            'packetLength': packetLength,
            'sessionTime': responseTime
        }

        if(mode == self.MESSAGE_MODE_COMMAND):
            # Command Specific Header Fields
            header['password'] = self.getTwoByteInt(8, byteArray)
        elif(mode == self.MESSAGE_MODE_RESPONSE):
            # Payload Specific Header Fields
            header['returnCode'] = self.getOneByteInt(12, byteArray)
            header['unknown1'] = self.getOneByteInt(13, byteArray)
            header['ejecting'] = self.getEjecting(14, byteArray)
            header['battery'] = self.getBatteryLevel(byteArray)
            header['printCount'] = self.getPrintCount(byteArray)

        self.header = header

        return header

    def validatePacket(self, byteArray, packetLength):
        """
        Validate that a payload ends correctly.

        This is done by checking the end bytes and the checksum.
        """
        try:
            checkSumIndex = 0
            checkSum = 0
            while(checkSumIndex < (packetLength - 4)):
                checkSum += (byteArray[checkSumIndex] & 0xFF)
                checkSumIndex += 1
            if ((byteArray[checkSumIndex + 2] == 13) and
                    (byteArray[checkSumIndex + 3] == 10)):
                expectedCB = (checkSum +
                              (((byteArray[checkSumIndex] & 0xFF) << 8)
                               | ((byteArray[checkSumIndex + 1] & 0xFF) << 0)))
                if (expectedCB & 65535) == 65535:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as ex:
            print("Unexpected Error validating packet: " + str(type(ex)))
            print(ex.args)
            print(ex)
            print("Expected:      %s" % (packetLength))
            print("Actual:        %s" % (str(len(byteArray))))
            print("Final 4 bytes: %s" % (self.printByteArray(byteArray[-4:])))

    def generateCommand(self, mode, cmdType, sessionTime, payload, pinCode):
        """Generate a command.

        Takes Command arguments and packs them into a byteArray to be
        sent to the Instax SP-2.
        """
        self.encodedSessionTime = self.getFourByteInt(
            0,
            self.encodeFourByteInt(sessionTime))
        commandPayloadLength = 16 + len(payload)
        commandPayload = bytearray()
        commandPayload.append(mode & 0xFF)  # Start of payload is 36
        commandPayload.append(cmdType & 0xFF)  # The Command bytes
        commandPayload = commandPayload + \
            self.encodeTwoByteInt(commandPayloadLength)
        commandPayload = commandPayload + self.encodeFourByteInt(sessionTime)
        commandPayload = commandPayload + self.encodeTwoByteInt(pinCode)
        commandPayload.append(0)  # Nothing
        commandPayload.append(0)  # Nothing
        if(len(payload) > 0):
            commandPayload = commandPayload + payload
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

    def generateResponse(self, mode, cmdType, sessionTime, payload, returnCode,
                         ejectState, battery, printCount):
        """Generate a response Byte Array.

        Takes Response arguments and packs them into a byteArray to be
        sent to the Instax-SP2.
        """
        self.encodedSessionTime = self.getFourByteInt(
            0, self.encodeFourByteInt(sessionTime))
        responsePayloadLength = 20 + len(payload)
        responsePayload = bytearray()
        responsePayload.append(mode & 0xFF)  # Start of payload is 42
        responsePayload.append(cmdType & 0xFF)  # The Response type bytes
        responsePayload = responsePayload + self.encodeTwoByteInt(
            responsePayloadLength)
        responsePayload = responsePayload + self.encodeFourByteInt(sessionTime)
        responsePayload = responsePayload + bytearray(4)
        responsePayload = responsePayload + self.encodeOneByteInt(returnCode)
        responsePayload.append(0)  # Nothing
        responsePayload = responsePayload + self.encodeEjecting(0)
        responsePayload = responsePayload + self.encodeBatteryAndPrintCount(
            battery, printCount)

        if(len(payload) > 0):
            responsePayload = responsePayload + payload
        # Generating the Checksum & End of payload
        checkSumIndex = 0
        checkSum = 0
        while(checkSumIndex < (responsePayloadLength - 4)):
            checkSum += (responsePayload[checkSumIndex] & 0xFF)
            checkSumIndex += 1
        responsePayload.append(((checkSum ^ -1) >> 8) & 0xFF)
        responsePayload.append(((checkSum ^ -1) >> 0) & 0xFF)
        responsePayload.append(13)
        responsePayload.append(10)
        return responsePayload

    def encodeCommand(self, sessionTime, pinCode):
        """Encode a command packet into a byteArray."""
        payload = self.encodeComPayload()
        encodedPacket = self.generateCommand(self.mode, self.TYPE,
                                             sessionTime, payload, pinCode)
        return encodedPacket

    def encodeResponse(self, sessionTime, returnCode, ejectState, battery,
                       printCount):
        """Encode a response packet into a byteArray."""
        payload = self.encodeRespPayload()
        encodedPacket = self.generateResponse(self.mode, self.TYPE,
                                              sessionTime, payload,
                                              returnCode, ejectState,
                                              battery, printCount)
        return encodedPacket

    def getFourByteInt(self, offset, byteArray):
        """Decode a Four Byte Integer."""
        if(len(byteArray) < (offset + 4)):
            return 0
        else:
            return (((byteArray[offset] & 0xFF) << 24) | (
                    (byteArray[(offset) + 1] & 0xFF) << 16) | (
                    (byteArray[(offset) + 2] & 0xFF) << 8) | (
                    (byteArray[(offset) + 3] & 0xFF) << 0))

    def encodeFourByteInt(self, numberToEncode):
        """Encode a Four Byte Integer."""
        fourByteInt = bytearray()
        fourByteInt.append((numberToEncode >> 24) & 0xFF)  # B1
        fourByteInt.append((numberToEncode >> 16) & 0xFF)  # B2
        fourByteInt.append((numberToEncode >> 8) & 0xFF)  # B3
        fourByteInt.append((numberToEncode >> 0) & 0xFF)  # B4
        return fourByteInt

    def getTwoByteInt(self, offset, byteArray):
        """Decode a Two Byte Integer."""
        if(len(byteArray) < (offset + 2)):
            return 0
        else:
            return (((byteArray[offset] & 0xFF) << 8) | (
                (byteArray[(offset) + 1] & 0xFF) << 0))

    def encodeTwoByteInt(self, numberToEncode):
        """Encode a Two Byte Integer."""
        twoByteInt = bytearray()
        twoByteInt.append((numberToEncode >> 8) & 0xFF)  # B1
        twoByteInt.append((numberToEncode >> 0) & 0xFF)  # B2
        return twoByteInt

    def getOneByteInt(self, offset, byteArray):
        """Decode a One Byte Integer."""
        if(len(byteArray) < (offset + 1)):
            return 0
        else:
            return (byteArray[offset] & 0xFF)

    def encodeOneByteInt(self, numberToEncode):
        """Encode a One Byte Integer."""
        oneByteInt = bytearray()
        oneByteInt.append((numberToEncode >> 0) & 0xFF)
        return oneByteInt

    def getEjecting(self, offset, byteArray):
        """Decode the Ejecting State."""
        if(len(byteArray) < (offset + 1)):
            return 0
        else:
            return ((byteArray[offset] >> 2) & 0xFF)

    def encodeEjecting(self, eject):
        """Encode the Ejecting State."""
        ejectState = bytearray()
        ejectState.append((eject >> 2) & 0xFF)
        return ejectState

    def getBatteryLevel(self, byteArray):
        """Decode the Battery Level."""
        if(len(byteArray) < 16):
            return -1
        else:
            return ((byteArray[15] >> 4) & 7)

    def getPrintCount(self, byteArray):
        """Decode the Print Count."""
        if(len(byteArray) < 16):
            return -1
        else:
            return ((byteArray[15] >> 0) & 15)

    def encodeBatteryAndPrintCount(self, battery, printCount):
        """Encode Battery Level and Print Count."""
        oneByteInt = bytearray()
        oneByteInt.append((battery << 4) | printCount << 0)
        return oneByteInt

    def formatVersionNumber(self, version):
        """Encode a Version Number."""
        part2 = version & 0xFF
        part1 = ((65280 & version) >> 8)
        return('%s.%s' % ("%0.2X" % part1, "%0.2X" % part2))

    def encodeModelString(self, model):
        """Encode a Model String."""
        return bytes(model, encoding="UTF-8")

    def getPrinterModelString(self, offset, byteArray):
        """Decode a Model String."""
        if(len(byteArray) < (offset + 4)):
            return ''
        else:
            return str(byteArray[offset: offset + 4], 'ascii')

    def getPayloadBytes(self, offset, length, byteArray):
        """Return Payload Bytes."""
        return byteArray[offset:offset + length]


class SpecificationsCommand(Packet):
    """Specifications Command and Response."""

    NAME = "Specifications"
    TYPE = Packet.MESSAGE_TYPE_SPECIFICATIONS

    def __init__(self, mode, byteArray=None, maxHeight=800, maxWidth=600,
                 maxColours=256, unknown1=None, maxMsgSize=None, unknown2=None,
                 unknown3=None):
        """Initialise the Packet."""
        super(SpecificationsCommand, self).__init__(mode)
        self.payload = {}
        self.mode = mode

        if (byteArray is not None):
            self.byteArray = byteArray
            self.header = super(SpecificationsCommand,
                                self).decodeHeader(mode, byteArray)
            self.valid = self.validatePacket(byteArray,
                                             self.header['packetLength'])
            if(mode == self.MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeComPayload(byteArray)
            elif(mode == self.MESSAGE_MODE_RESPONSE):
                self.payload = self.decodeRespPayload(byteArray)
        else:
            self.mode = mode
            self.maxHeight = maxHeight
            self.maxWidth = maxWidth
            self.maxColours = maxColours
            self.unknown1 = unknown1
            self.unknown2 = unknown2
            self.unknown3 = unknown3
            self.maxMsgSize = maxMsgSize

    def encodeComPayload(self):
        """Encode Command payload.

        This command does not have a payload, pass.
        """
        return {}

    def decodeComPayload(self, byteArray):
        """Decode Command payload.

        This command does not have a payload, pass.
        """
        return {}

    def encodeRespPayload(self):
        """Encode Response payload."""
        payload = bytearray()
        payload = payload + self.encodeTwoByteInt(self.maxWidth)
        payload = payload + self.encodeTwoByteInt(self.maxHeight)
        payload = payload + self.encodeTwoByteInt(self.maxColours)
        payload = payload + self.encodeTwoByteInt(self.unknown1)
        payload = payload + bytearray(4)  # Nothing
        payload = payload + self.encodeTwoByteInt(self.maxMsgSize)
        payload = payload + self.encodeOneByteInt(self.unknown2)
        payload.append(0)  # Nothing
        payload = payload + self.encodeFourByteInt(self.unknown3)
        payload = payload + bytearray(8)  # Nothing
        return payload

    def decodeRespPayload(self, byteArray):
        """Decode Response payload."""
        self.maxWidth = self.getTwoByteInt(16, byteArray)
        self.maxHeight = self.getTwoByteInt(18, byteArray)
        self.maxColours = self.getTwoByteInt(20, byteArray)
        self.unknown1 = self.getTwoByteInt(22, byteArray)
        self.maxMsgSize = self.getTwoByteInt(28, byteArray)
        self.unknown2 = self.getOneByteInt(30, byteArray)
        self.unknown3 = self.getFourByteInt(32, byteArray)
        self.payload = {
            'maxHeight': self.maxHeight,
            'maxWidth': self.maxWidth,
            'maxColours': self.maxColours,
            'unknown1': self.unknown1,
            'maxMsgSize': self.maxMsgSize,
            'unknown2': self.unknown2,
            'unknown3': self.unknown3
        }
        return self.payload


class VersionCommand(Packet):
    """Version Command."""

    NAME = "Version"
    TYPE = Packet.MESSAGE_TYPE_PRINTER_VERSION

    def __init__(self, mode, byteArray=None, unknown1=None, firmware=None,
                 hardware=None):
        """Initialise the packet."""
        super(VersionCommand, self).__init__(mode)
        self.payload = {}
        self.mode = mode

        if (byteArray is not None):
            self.byteArray = byteArray
            self.header = super(VersionCommand,
                                self).decodeHeader(mode, byteArray)
            self.valid = self.validatePacket(byteArray,
                                             self.header['packetLength'])
            if(mode == self.MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeComPayload(byteArray)
            elif(mode == self.MESSAGE_MODE_RESPONSE):
                self.payload = self.decodeRespPayload(byteArray)
        else:
            self.mode = mode
            self.unknown1 = unknown1
            self.firmware = firmware
            self.hardware = hardware

    def encodeComPayload(self):
        """Encode Command payload.

        This command does not have a payload, pass.
        """
        return {}

    def decodeComPayload(self, byteArray):
        """Decode Command payload.

        This command does not have a payload, pass.
        """
        return {}

    def encodeRespPayload(self):
        """Encode Response payload."""
        payload = bytearray()
        payload = payload + self.encodeTwoByteInt(self.unknown1)
        payload = payload + self.encodeTwoByteInt(self.firmware)
        payload = payload + self.encodeTwoByteInt(self.hardware)
        payload = payload + bytearray(2)  # Nothing
        return payload

    def decodeRespPayload(self, byteArray):
        """Decode Response payload."""
        self.unknown1 = self.getTwoByteInt(16, byteArray)
        self.firmware = self.formatVersionNumber(
            self.getTwoByteInt(18, byteArray))
        self.hardware = self.formatVersionNumber(
            self.getTwoByteInt(20, byteArray))
        self.payload = {
            'unknown1': self.unknown1,
            'firmware': self.firmware,
            'hardware': self.hardware
        }
        return self.payload


class PrintCountCommand(Packet):
    """Print Count Command."""

    NAME = "Print Count"
    TYPE = Packet.MESSAGE_TYPE_PRINT_COUNT

    def __init__(self, mode, byteArray=None, printHistory=None):
        """Initialise the packet."""
        super(PrintCountCommand, self).__init__(mode)
        self.payload = {}
        self.mode = mode

        if (byteArray is not None):
            self.byteArray = byteArray
            self.header = super(PrintCountCommand,
                                self).decodeHeader(mode, byteArray)
            self.valid = self.validatePacket(byteArray,
                                             self.header['packetLength'])
            if(mode == self.MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeComPayload(byteArray)
            elif(mode == self.MESSAGE_MODE_RESPONSE):
                self.payload = self.decodeRespPayload(byteArray)
        else:
            self.mode = mode
            self.printHistory = printHistory

    def encodeComPayload(self):
        """Encode Command payload.

        This command does not have a payload, pass.
        """
        return {}

    def decodeComPayload(self, byteArray):
        """Decode Command payload.

        This command does not have a payload, pass.
        """
        return {}

    def encodeRespPayload(self):
        """Encode Response payload."""
        payload = bytearray()
        payload = payload + self.encodeFourByteInt(self.printHistory)
        payload = payload + bytearray(12)
        return payload

    def decodeRespPayload(self, byteArray):
        """Decode Response payload."""
        self.printHistory = self.getFourByteInt(16, byteArray)
        self.payload = {
            'printHistory': self.printHistory
        }
        return self.payload


class ModelNameCommand(Packet):
    """Model Name Command."""

    NAME = "Model Name"
    TYPE = Packet.MESSAGE_TYPE_MODEL_NAME

    def __init__(self, mode, byteArray=None, modelName=None):
        """Initialise the packet."""
        super(ModelNameCommand, self).__init__(mode)
        self.payload = {}
        self.mode = mode

        if (byteArray is not None):
            self.byteArray = byteArray
            self.header = super(ModelNameCommand,
                                self).decodeHeader(mode, byteArray)
            self.valid = self.validatePacket(byteArray,
                                             self.header['packetLength'])
            if(mode == self.MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeComPayload(byteArray)
            elif(mode == self.MESSAGE_MODE_RESPONSE):
                self.payload = self.decodeRespPayload(byteArray)
        else:
            self.mode = mode
            self.modelName = modelName

    def encodeComPayload(self):
        """Encode Command payload.

        This command does not have a payload, pass.
        """
        return {}

    def decodeComPayload(self, byteArray):
        """Decode Command payload.

        This command does not have a payload, pass.
        """
        return {}

    def encodeRespPayload(self):
        """Encode Response payload."""
        payload = bytearray()
        payload = payload + self.encodeModelString(self.modelName)
        return payload

    def decodeRespPayload(self, byteArray):
        """Decode Response payload."""
        self.modelName = self.getPrinterModelString(16, byteArray)
        self.payload = {
            'modelName': self.modelName
        }
        return self.payload


class PrePrintCommand(Packet):
    """Pre Print Command."""

    NAME = "Pre Print"
    TYPE = Packet.MESSAGE_TYPE_PRE_PRINT

    def __init__(self, mode, byteArray=None, cmdNumber=None, respNumber=None):
        """Initialise the packet."""
        super(PrePrintCommand, self).__init__(mode)
        self.payload = {}
        self.mode = mode

        if(byteArray is not None):
            self.byteArray = byteArray
            self.header = super(PrePrintCommand,
                                self).decodeHeader(mode, byteArray)
            self.valid = self.validatePacket(byteArray,
                                             self.header['packetLength'])
            if(mode == self.MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeComPayload(byteArray)
            elif(mode == self.MESSAGE_MODE_RESPONSE):
                self.payload = self.decodeRespPayload(byteArray)
        else:
            self.mode = mode
            self.cmdNumber = cmdNumber
            self.respNumber = respNumber

    def encodeComPayload(self):
        """Encode Command Payload."""
        payload = bytearray()
        payload = payload + bytearray(2)
        payload = payload + self.encodeTwoByteInt(self.cmdNumber)
        return payload

    def decodeComPayload(self, byteArray):
        """Decode the Command Payload."""
        self.cmdNumber = self.getTwoByteInt(14, byteArray)
        self.payload = {
            'cmdNumber': self.cmdNumber
        }
        return self.payload

    def encodeRespPayload(self):
        """Encode Response Payload."""
        payload = bytearray()
        payload = payload + self.encodeTwoByteInt(self.cmdNumber)
        payload = payload + self.encodeTwoByteInt(self.respNumber)
        return payload

    def decodeRespPayload(self, byteArray):
        """Decode Response Payload."""
        self.cmdNumber = self.getTwoByteInt(16, byteArray)
        self.respNumber = self.getTwoByteInt(18, byteArray)
        self.payload = {
            'cmdNumber': self.cmdNumber,
            'respNumber': self.respNumber
        }
        return self.payload


class PrinterLockCommand(Packet):
    """Printer Lock Command."""

    NAME = "LockPrinter"
    TYPE = Packet.MESSAGE_TYPE_LOCK_DEVICE

    def __init__(self, mode, lockState=None, byteArray=None):
        """Initialise Lock Printer Packet."""
        super(PrinterLockCommand, self).__init__(mode)
        self.payload = {}
        self.mode = mode
        if (byteArray is not None):
            self.byteArray = byteArray
            self.header = super(PrinterLockCommand,
                                self).decodeHeader(mode, byteArray)
            self.valid = self.validatePacket(byteArray,
                                             self.header['packetLength'])
            if(mode == self.MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeComPayload(byteArray)
            elif(mode == self.MESSAGE_MODE_RESPONSE):
                self.decodedCommandPayload = self.decodeRespPayload(byteArray)
        else:
            self.mode = mode
            self.lockState = lockState

    def encodeComPayload(self):
        """Encode Command Payload."""
        payload = bytearray()
        payload = payload + self.encodeOneByteInt(self.lockState)
        payload = payload + self.encodeOneByteInt(0)
        payload = payload + self.encodeTwoByteInt(0)
        return payload

    def decodeComPayload(self, byteArray):
        """Decode the Command Payload."""
        self.lockState = self.getOneByteInt(12, byteArray)
        self.payload = {
            'lockState': self.lockState
        }
        return self.payload

    def encodeRespPayload(self):
        """Encode Response Payload."""
        return bytearray()

    def decodeRespPayload(self, byteArray):
        """Decode Response Payload."""
        return {}


class ResetCommand(Packet):
    """Reset Command."""

    NAME = "Reset"
    TYPE = Packet.MESSAGE_TYPE_RESET

    def __init__(self, mode, byteArray=None):
        """Initialise Reset Command Packet."""
        super(ResetCommand, self).__init__(mode)
        self.payload = {}
        self.mode = mode
        if (byteArray is not None):
            self.byteArray = byteArray
            self.header = super(ResetCommand,
                                self).decodeHeader(mode, byteArray)
            self.valid = self.validatePacket(byteArray,
                                             self.header['packetLength'])
            if(mode == self.MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeComPayload(byteArray)
            elif(mode == self.MESSAGE_MODE_RESPONSE):
                self.decodedCommandPayload = self.decodeRespPayload(byteArray)
        else:
            self.mode = mode

    def encodeComPayload(self):
        """Encode Command Payload."""
        return bytearray()

    def decodeComPayload(self, byteArray):
        """Decode the Command Payload."""
        return {}

    def encodeRespPayload(self):
        """Encode Response Payload."""
        return bytearray()

    def decodeRespPayload(self, byteArray):
        """Decode Response Payload."""
        return {}


class PrepImageCommand(Packet):
    """Prep Image Command."""

    NAME = "PrepImage"
    TYPE = Packet.MESSAGE_TYPE_PREP_IMAGE

    def __init__(self, mode, byteArray=None, format=None, options=None,
                 imgLength=None, maxLen=None):
        """Initialise Prep Image Command Packet."""
        super(PrepImageCommand, self).__init__(mode)
        self.payload = {}
        self.mode = mode
        if (byteArray is not None):
            self.byteArray = byteArray
            self.header = super(PrepImageCommand,
                                self).decodeHeader(mode, byteArray)
            self.valid = self.validatePacket(byteArray,
                                             self.header['packetLength'])
            if(mode == self.MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeComPayload(byteArray)
            elif(mode == self.MESSAGE_MODE_RESPONSE):
                self.decodedCommandPayload = self.decodeRespPayload(byteArray)
        else:
            self.mode = mode
            self.format = format
            self.options = options
            self.imgLength = imgLength
            self.maxLen = maxLen

    def encodeComPayload(self):
        """Encode Command Payload."""
        payload = bytearray()
        payload = payload + self.encodeOneByteInt(self.format)
        payload = payload + self.encodeOneByteInt(self.options)
        payload = payload + self.encodeFourByteInt(self.imgLength)
        payload = payload + self.encodeTwoByteInt(0)
        payload = payload + self.encodeTwoByteInt(0)
        payload = payload + self.encodeTwoByteInt(0)
        return payload

    def decodeComPayload(self, byteArray):
        """Decode the Command Payload."""
        self.format = self.getOneByteInt(12, byteArray)
        self.options = self.getOneByteInt(13, byteArray)
        self.imgLength = self.getFourByteInt(14, byteArray)

        self.payload = {
            'format': self.format,
            'options': self.options,
            'imgLength': self.imgLength
        }
        return self.payload

    def encodeRespPayload(self):
        """Encode Response Payload."""
        payload = bytearray(2)
        payload = payload + self.encodeTwoByteInt(self.maxLen)
        return payload

    def decodeRespPayload(self, byteArray):
        """Decode Response Payload."""
        self.maxLen = self.getTwoByteInt(18, byteArray)
        self.payload = {
            'maxLen': self.maxLen
        }
        return self.payload


class SendImageCommand(Packet):
    """Send Image Command."""

    NAME = "Send Image"
    TYPE = Packet.MESSAGE_TYPE_SEND_IMAGE

    def __init__(self, mode, byteArray=None, sequenceNumber=None,
                 payloadBytes=None):
        """Initialise Send Image Command Packet."""
        super(SendImageCommand, self).__init__(mode)
        self.payload = {}
        self.mode = mode
        if(byteArray is not None):
            self.byteArray = byteArray
            self.header = super(SendImageCommand, self).decodeHeader(mode,
                                                                     byteArray)
            self.valid = self.validatePacket(byteArray,
                                             self.header['packetLength'])
            if(mode == self.MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeComPayload(byteArray)
            elif(mode == self.MESSAGE_MODE_RESPONSE):
                self.decodedCommandPayload = self.decodeRespPayload(byteArray)
        else:
            self.mode = mode
            self.sequenceNumber = sequenceNumber
            self.payloadBytes = payloadBytes

    def encodeComPayload(self):
        """Encode Command Payload."""
        payload = bytearray(0)
        payload = payload + self.encodeFourByteInt(self.sequenceNumber)
        payload = payload + self.payloadBytes
        return payload

    def decodeComPayload(self, byteArray):
        """Decode the Command Payload."""
        self.sequenceNumber = self.getFourByteInt(12, byteArray)
        payloadBytesLength = self.header['packetLength'] - 20
        self.payloadBytes = self.getPayloadBytes(16, payloadBytesLength,
                                                 byteArray)
        self.payload = {
            'sequenceNumber': self.sequenceNumber,
            'payloadBytes': self.payloadBytes
        }
        return self.payload

    def encodeRespPayload(self):
        """Encode Response Payload."""
        payload = bytearray(3)
        payload = payload + self.encodeOneByteInt(self.sequenceNumber)
        return payload

    def decodeRespPayload(self, byteArray):
        """Decode Response Payload."""
        self.sequenceNumber = self.getOneByteInt(19, byteArray)
        self.payload = {
            'sequenceNumber': self.sequenceNumber
            }
        return self.payload


class Type83Command(Packet):
    """Type 83 Command."""

    NAME = "Type 83"
    TYPE = Packet.MESSAGE_TYPE_83

    def __init__(self, mode, byteArray=None):
        """Initialise Type 83 Command Packet."""
        super(Type83Command, self).__init__(mode)
        self.payload = {}
        self.mode = mode
        if(byteArray is not None):
            self.byteArray = byteArray
            self.header = super(Type83Command, self).decodeHeader(mode,
                                                                  byteArray)
            self.valid = self.validatePacket(byteArray,
                                             self.header['packetLength'])
            if(mode == self.MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeComPayload(byteArray)
            elif(mode == self.MESSAGE_MODE_RESPONSE):
                self.decodedCommandPayload = self.decodeRespPayload(byteArray)
        else:
            self.mode = mode

    def encodeComPayload(self):
        """Encode Command Payload."""
        return bytearray()

    def decodeComPayload(self, byteArray):
        """Decode the Command Payload."""
        return {}

    def encodeRespPayload(self):
        """Encode Response Payload."""
        return bytearray()

    def decodeRespPayload(self, byteArray):
        """Decode Response Payload."""
        return {}


class Type195Command(Packet):
    """Type 195 Command."""

    NAME = "Type 195"
    TYPE = Packet.MESSAGE_TYPE_195

    def __init__(self, mode, byteArray=None):
        """Initialise Type 195 Command Packet."""
        super(Type195Command, self).__init__(mode)
        self.payload = {}
        self.mode = mode
        if(byteArray is not None):
            self.byteArray = byteArray
            self.header = super(Type195Command, self).decodeHeader(mode,
                                                                   byteArray)
            self.valid = self.validatePacket(byteArray,
                                             self.header['packetLength'])
            if(mode == self.MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeComPayload(byteArray)
            elif(mode == self.MESSAGE_MODE_RESPONSE):
                self.decodedCommandPayload = self.decodeRespPayload(byteArray)
        else:
            self.mode = mode

    def encodeComPayload(self):
        """Encode Command Payload."""
        return bytearray()

    def decodeComPayload(self, byteArray):
        """Decode the Command Payload."""
        return {}

    def encodeRespPayload(self):
        """Encode Response Payload."""
        return bytearray()

    def decodeRespPayload(self, byteArray):
        """Decode Response Payload."""
        return {}


class LockStateCommand(Packet):
    """LockState Command."""

    NAME = "Lock State"
    TYPE = Packet.MESSAGE_TYPE_SET_LOCK_STATE

    def __init__(self, mode, byteArray=None, unknownFourByteInt=None):
        """Initialise Lock State Command Packet."""
        super(LockStateCommand, self).__init__(mode)
        self.payload = {}
        self.mode = mode
        if(byteArray is not None):
            self.byteArray = byteArray
            self.header = super(LockStateCommand, self).decodeHeader(mode,
                                                                     byteArray)
            self.valid = self.validatePacket(byteArray,
                                             self.header['packetLength'])
            if(mode == self.MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeComPayload(byteArray)
            elif(mode == self.MESSAGE_MODE_RESPONSE):
                self.decodedCommandPayload = self.decodeRespPayload(byteArray)
        else:
            self.mode = mode
            self.unknownFourByteInt = unknownFourByteInt

    def encodeComPayload(self):
        """Encode Command Payload."""
        return bytearray()

    def decodeComPayload(self, byteArray):
        """Decode the Command Payload."""
        return {}

    def encodeRespPayload(self):
        """Encode Response Payload."""
        payload = bytearray(0)
        payload = payload + self.encodeFourByteInt(self.unknownFourByteInt)
        return payload

    def decodeRespPayload(self, byteArray):
        """Decode Response Payload."""
        self.unknownFourByteInt = self.getFourByteInt(16, byteArray)
        self.payload = {
            'unknownFourByteInt': self.unknownFourByteInt
        }
        return self.payload
