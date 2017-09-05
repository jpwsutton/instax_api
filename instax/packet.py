from .utilities import Utilities


class PacketFactory(object):
    'Packet Factory'
    MESSAGE_TYPE_SPECIFICATIONS = 79
    MESSAGE_TYPE_RESET = 80
    MESSAGE_TYPE_PREP_IMAGE = 81
    MESSAGE_TYPE_SEND_IMAGE = 82
    MESSAGE_TYPE_SET_LOCK_STATE = 176
    MESSAGE_TYPE_UNKNOWN_1 = 179
    MESSAGE_TYPE_CHANGE_PASSWORD = 182
    MESSAGE_TYPE_PRINTER_VERSION = 192
    MESSAGE_TYPE_PRINT_COUNT = 193
    MESSAGE_TYPE_MODEL_NAME = 194
    MESSAGE_TYPE_UNKNOWN_2 = 195
    MESSAGE_TYPE_PRE_PRINT = 196

    MESSAGE_MODE_COMMAND = 36  # Command from Client
    MESSAGE_MODE_RESPONSE = 42  # Response from Server

    def __init__(self):
        pass

    def decode(self, byteArray):
        """Decode a byte array into an instax Packet
        """
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
        else:
            print("Unknown Packet Type: " + str(pType))


class Packet(object):
    'Packet Utilities class'
    MESSAGE_TYPE_SPECIFICATIONS = 79
    MESSAGE_TYPE_RESET = 80
    MESSAGE_TYPE_PREP_IMAGE = 81
    MESSAGE_TYPE_SEND_IMAGE = 82
    MESSAGE_TYPE_SET_LOCK_STATE = 176
    MESSAGE_TYPE_UNKNOWN_1 = 179
    MESSAGE_TYPE_CHANGE_PASSWORD = 182
    MESSAGE_TYPE_PRINTER_VERSION = 192
    MESSAGE_TYPE_PRINT_COUNT = 193
    MESSAGE_TYPE_MODEL_NAME = 194
    MESSAGE_TYPE_UNKNOWN_2 = 195
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

    utilities = Utilities()

    def __init__(self, mode=None):
        pass

    def printByteArray(self, byteArray):
        hexString = ''.join('%02x' % i for i in byteArray)
        data = ' '.join(hexString[i:i+4] for i in range(0, len(hexString), 4))
        info = (data[:80] + '..') if len(data) > 80 else data
        return(info)

    def printDebug(self):
        """Print Debug information about packet."""
        print("-------------------------------------------------------------")
        print("Bytes: %s" % (self.printByteArray(self.byteArray)))
        print("Mode:  %s" % (self.strings[self.mode]))
        print("Type:  %s" % (self.NAME))
        print("Valid: %s" % (self.valid))
        print("Header:")
        print('    Start Byte:', self.header['startByte'])
        print('    Command:', self.header['cmdByte'])
        print('    Packet Length:', self.header['packetLength'])
        print('    Session Time:', self.header['sessionTime'])
        if(self.mode == self.MESSAGE_MODE_COMMAND):
            print('    Password:', self.header['password'])
        elif(self.mode == self.MESSAGE_MODE_RESPONSE):
            print('    Return Code:', self.header['returnCode'])
            print('    Unknown 1:', self.header['unknown1'])
            print('    Ejecting:', self.header['ejecting'])
            print('    Battery:', self.header['battery'])
            print('    Prints Left:', self.header['printCount'])

        if len(self.payload) == 0:
            print("Payload: None")
        else:
            print("Payload:")
            for key in self.payload:
                if(key == 'payloadBytes'):
                    print('    ',
                          key,
                          ': (length: ' + str(len(self.payload[key])) + ') : ',
                          self.printByteArray(self.payload[key]))
                else:
                    print('    ', key, ':', self.payload[key])
        print("-------------------------------------------------------------")
        print()

    def decodeHeader(self, mode, byteArray):
        """Decode packet header."""
        startByte = self.utilities.getOneByteInt(0, byteArray)
        cmdByte = self.utilities.getOneByteInt(1, byteArray)
        packetLength = self.utilities.getTwoByteInt(2, byteArray)
        responseTime = self.utilities.getFourByteInt(4, byteArray)
        header = {
            'startByte': startByte,
            'cmdByte': cmdByte,
            'packetLength': packetLength,
            'sessionTime': responseTime
        }

        if(mode == self.MESSAGE_MODE_COMMAND):
            # Command Specific Header Fields
            header['password'] = self.utilities.getTwoByteInt(8, byteArray)
        elif(mode == self.MESSAGE_MODE_RESPONSE):
            # Payload Specific Header Fields
            header['returnCode'] = self.utilities.getOneByteInt(12, byteArray)
            header['unknown1'] = self.utilities.getOneByteInt(13, byteArray)
            header['ejecting'] = self.utilities.getEjecting(14, byteArray)
            header['battery'] = self.utilities.getBatteryLevel(byteArray)
            header['printCount'] = self.utilities.getPrintCount(byteArray)

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
                               | ((byteArray[checkSumIndex+1] & 0xFF) << 0)))
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
        """ Takes Command arguments and packs them into a byteArray to be
            sent to the Instax SP-2.
        """
        self.encodedSessionTime = self.utilities.getFourByteInt(0,self.utilities.encodeFourByteInt(sessionTime))
        commandPayloadLength = 16 + len(payload)
        commandPayload = bytearray()
        commandPayload.append(mode & 0xFF)  # Start of payload is 36
        commandPayload.append(cmdType & 0xFF)  # The Command bytes
        commandPayload = commandPayload + self.utilities.encodeTwoByteInt(commandPayloadLength)
        commandPayload = commandPayload + self.utilities.encodeFourByteInt(sessionTime)
        commandPayload = commandPayload + self.utilities.encodeTwoByteInt(pinCode)
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
        """ Takes Response arguments and packs them into a byteArray to be
            sent to the Instax-SP2
        """
        self.encodedSessionTime = self.utilities.getFourByteInt(0, self.utilities.encodeFourByteInt(sessionTime))
        responsePayloadLength = 20 + len(payload)
        responsePayload = bytearray()
        responsePayload.append(mode & 0xFF)  # Start of payload is 42
        responsePayload.append(cmdType & 0xFF)  # The Response type bytes
        responsePayload = responsePayload + self.utilities.encodeTwoByteInt(responsePayloadLength)
        responsePayload = responsePayload + self.utilities.encodeFourByteInt(sessionTime)
        responsePayload.append(0)  # Nothing
        responsePayload.append(0)  # Nothing
        responsePayload.append(0)  # Nothing
        responsePayload.append(0)  # Nothing
        responsePayload = responsePayload + self.utilities.encodeOneByteInt(returnCode)
        responsePayload.append(0)  # Nothing
        responsePayload = responsePayload + self.utilities.encodeEjecting(0)
        responsePayload = responsePayload + self.utilities.encodeBatteryAndPrintCount(battery, printCount)

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
        payload = payload + self.utilities.encodeTwoByteInt(self.maxWidth)
        payload = payload + self.utilities.encodeTwoByteInt(self.maxHeight)
        payload = payload + self.utilities.encodeTwoByteInt(self.maxColours)
        payload = payload + self.utilities.encodeTwoByteInt(self.unknown1)
        payload.append(0)  # Nothing
        payload.append(0)  # Nothing
        payload.append(0)  # Nothing
        payload.append(0)  # Nothing
        payload = payload + self.utilities.encodeTwoByteInt(self.maxMsgSize)
        payload = payload + self.utilities.encodeOneByteInt(self.unknown2)
        payload.append(0)  # Nothing
        payload = payload + self.utilities.encodeFourByteInt(self.unknown3)
        payload.append(0)  # Nothing
        payload.append(0)  # Nothing
        payload.append(0)  # Nothing
        payload.append(0)  # Nothing
        payload.append(0)  # Nothing
        payload.append(0)  # Nothing
        payload.append(0)  # Nothing
        payload.append(0)  # Nothing
        return payload

    def decodeRespPayload(self, byteArray):
        """Decode Response payload."""
        self.maxWidth = self.utilities.getTwoByteInt(16, byteArray)
        self.maxHeight = self.utilities.getTwoByteInt(18, byteArray)
        self.maxColours = self.utilities.getTwoByteInt(20, byteArray)
        self.unknown1 = self.utilities.getTwoByteInt(22, byteArray)
        self.maxMsgSize = self.utilities.getTwoByteInt(28, byteArray)
        self.unknown2 = self.utilities.getOneByteInt(30, byteArray)
        self.unknown3 = self.utilities.getFourByteInt(32, byteArray)
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
        payload = payload + self.utilities.encodeTwoByteInt(self.unknown1)
        payload = payload + self.utilities.encodeTwoByteInt(self.firmware)
        payload = payload + self.utilities.encodeTwoByteInt(self.hardware)
        payload.append(0)  # Nothing
        payload.append(0)  # Nothing
        return payload

    def decodeRespPayload(self, byteArray):
        """Decode Response payload."""
        self.unknown1 = self.utilities.getTwoByteInt(16, byteArray)
        self.firmware = self.utilities.formatVersionNumber(
                            self.utilities.getTwoByteInt(18, byteArray))
        self.hardware = self.utilities.formatVersionNumber(
                            self.utilities.getTwoByteInt(20, byteArray))
        self.payload = {
            'unknown1': self.unknown1,
            'firmware': self.firmware,
            'hardware': self.hardware
        }
        return self.payload


class PrintCountCommand(Packet):
    """Print Count Command"""

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
        payload = payload + self.utilities.encodeFourByteInt(self.printHistory)
        payload = payload + bytearray(12)
        return payload

    def decodeRespPayload(self, byteArray):
        """Decode Response payload."""
        self.printHistory = self.utilities.getFourByteInt(16, byteArray)
        self.payload = {
            'printHistory': self.printHistory
        }
        return self.payload


class ModelNameCommand(Packet):
    """Model Name Command"""

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
        payload = payload + self.utilities.encodeModelString(self.modelName)
        return payload

    def decodeRespPayload(self, byteArray):
        """Decode Response payload."""
        self.modelName = self.utilities.getPrinterModelString(16, byteArray)
        self.payload = {
            'modelName': self.modelName
        }
        return self.payload


class PrePrintCommand(Packet):
    """Pre Print Command"""
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
            self.respNumber = respNumber

    def encodeComPayload(self):
        """Encode Command Payload."""
        payload = bytearray()
        payload = payload + bytearray(2)
        payload = payload + self.utilities.encodeTwoByteInt(self.cmdNumber)
        return payload

    def decodeComPayload(self, byteArray):
        """Decode the Command Payload."""
        self.cmdNumber = self.utilities.getTwoByteInt(14, byteArray)
        self.payload = {
            'cmdNumber': self.cmdNumber
        }
        return self.payload

    def encodeRespPayload(self):
        """Encode Response Payload."""
        payload = bytearray()
        return payload

    def decodeRespPayload(self, byteArray):
        """Decode Response Payload."""
        return {}



class ResetCommand(Packet):
    """Reset Command."""

    NAME = "Reset"
    TYPE = Packet.MESSAGE_TYPE_RESET

    def __init__(self, mode, byteArray=None, returnCode=None, unknown1=None,
                 ejecting=None, unknown2=None):
        """Initialise Reset Command Packet."""
        super(ResetCommand, self).__init__(mode)
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


    def decodeComPayload(self, byteArray):
        # This command does not have a payload
        return {}

    def decodeResponse(self, byteArray):
        # This response does not have a payload
        return {}

class PrepImageCommand(Packet):
    NAME = "Image Prepare"

    def __init__(self, mode, byteArray=None, format=None, options=None, length=None, unknown1=None):
        super(PrepImageCommand, self).__init__(mode)
        if (byteArray is not None):
            self.header = super(PrepImageCommand, self).decodeHeader(mode, byteArray)
            self.valid = self.validatePacket(byteArray, self.header['packetLength'])
            if(mode == self.MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeCommand(byteArray)
            elif(mode ==self.MESSAGE_MODE_RESPONSE):
                self.decodedCommandPayload = self.decodeResponse(byteArray)
            #super(PrepImageCommand, self).printDebug(byteArray, mode, self.NAME, self.header, self.decodedCommandPayload)
        else:
            print("Building new Image Prepare Command")


    def decodeCommand(self, byteArray):
        self.format  = self.utilities.getOneByteInt(12, byteArray)
        self.options = self.utilities.getOneByteInt(13, byteArray)
        self.length  = self.utilities.getFourByteInt(14, byteArray)
        self.payload = {
            'format' : self.format,
            'options'  : self.options,
            'length': self.length
        }
        return self.payload

    def decodeResponse(self, byteArray):
        self.unkown1  = self.utilities.getTwoByteInt(18, byteArray)
        self.payload = {
            'unkown1' : self.unkown1
        }
        return self.payload


class SendImageCommand(Packet):
    NAME = "Send Image"

    def __init__(self, byteArray=None, sequenceNumber=None, payloadBytes=None, unknown1=None):
        super(SendImageCommand, self).__init__(mode)
        if(byteArray is not None):
            self.header = super(SendImageCommand, self).decodeHeader(mode, byteArray)
            self.valid = self.validatePacket(byteArray, self.header['packetLength'])
            if(self.mode == self.MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeCommand(byteArray)
            elif(self.mode ==self.MESSAGE_MODE_RESPONSE):
                self.decodedCommandPayload = self.decodeResponse(byteArray)
            #super(SendImageCommand, self).printDebug(byteArray, mode, self.NAME, self.header, self.decodedCommandPayload)
        else:
            print("Building new Image Send Command")

    def decodeCommand(self, byteArray):
        self.sequenceNumber = self.utilities.getFourByteInt(12, byteArray)
        payloadBytesLength = self.header['packetLength'] - 20
        #print("Payload Bytes length: " + str(payloadBytesLength))
        #print("byteArray len" + str(len(byteArray)))
        self.payloadBytes = self.utilities.getPayloadBytes(16, payloadBytesLength + 2, byteArray)
        self.payload = {
            'sequenceNumber' : self.sequenceNumber,
            'payloadBytes'  : self.payloadBytes
        }
        return self.payload

    def decodeResponse(self, byteArray):
        self.unknown1 = self.utilities.getOneByteInt(16, byteArray)
        self.unknown2 = self.utilities.getOneByteInt(17, byteArray)
        self.unknown3 = self.utilities.getOneByteInt(18, byteArray)
        self.unknown4 = self.utilities.getOneByteInt(19, byteArray)
        self.payload = {
            'unknown1' : self.unknown1,
            'unknown2' : self.unknown2,
            'unknown3' : self.unknown3,
            'unknown4' : self.unknown4
        }
        return self.payload
