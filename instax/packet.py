from .utilities  import Utilities

MESSAGE_MODE_COMMAND            = 36 # Command from Client
MESSAGE_MODE_RESPONSE           = 42  # Response from Server
strings = {
    MESSAGE_MODE_COMMAND : "Command",
    MESSAGE_MODE_RESPONSE: "Response"
}

class PacketFactory(object):
    MESSAGE_TYPE_SPECIFICATIONS     = 79
    MESSAGE_TYPE_RESET              = 80
    MESSAGE_TYPE_PREP_IMAGE         = 81
    MESSAGE_TYPE_SEND_IMAGE         = 82
    MESSAGE_TYPE_SET_LOCK_STATE     = 176
    MESSAGE_TYPE_UNKNOWN_1          = 179
    MESSAGE_TYPE_CHANGE_PASSWORD    = 182
    MESSAGE_TYPE_PRINTER_VERSION    = 192
    MESSAGE_TYPE_PRINT_COUNT        = 193
    MESSAGE_TYPE_MODEL_NAME         = 194
    MESSAGE_TYPE_UNKNOWN_2          = 195
    MESSAGE_TYPE_UNKNOWN_3          = 196

    MESSAGE_MODE_COMMAND            = 36 # Command from Client
    MESSAGE_MODE_RESPONSE           = 42  # Response from Server

    strings = {
        MESSAGE_MODE_COMMAND : "Command",
        MESSAGE_MODE_RESPONSE: "Response"
    }

    def printByteArray(self, byteArray):
        hexString = ''.join('%02x'%i for i in byteArray)
        data = ' '.join(hexString[i:i+4] for i in range(0, len(hexString), 4))
        info = (data[:80] + '..') if len(data) > 80 else data
        return(info)

    def __init__(self):
        pass

    def getPacket(self, byteArray):
        """Decode a byte array into an instax Packet
        """


        # Get first two bytes as they will help identify the type of packet
        pMode = byteArray[0]
        pType = byteArray[1]


        # Identify the type of packet and hand over to that packets specific class
        if pType == self.MESSAGE_TYPE_SPECIFICATIONS:
            return(SpecificationsCommand(mode=pMode, byteArray=byteArray))
        elif pType == self.MESSAGE_TYPE_RESET:
            return(ResetCommand(mode=pMode, byteArray=byteArray))
        elif pType == self.MESSAGE_TYPE_PREP_IMAGE:
            return(PrepImageCommand(mode=pMode, byteArray=byteArray))
        elif pType == self.MESSAGE_TYPE_SEND_IMAGE:
            return(SendImageCommand(mode=pMode, byteArray=byteArray))
        else:
            print("Unknown Packet Type: " + str(pType))




class Packet(object):
    'Packet Utilities class'
    utilities = Utilities()

    def __init__(self, mode):
        self.mode = mode
        self.bob = "foo"
        pass

    def printByteArray(self, byteArray):
        hexString = ''.join('%02x'%i for i in byteArray)
        data = ' '.join(hexString[i:i+4] for i in range(0, len(hexString), 4))
        info = (data[:80] + '..') if len(data) > 80 else data
        return(info)

    def printDebug(self, byteArray, mode, name, header, payload):
        print("-------------------------------------------------------------")
        print("Bytes: %s" % (self.printByteArray(byteArray)))
        print("Mode:  %s" % (strings[mode]))
        print("Type:  %s" % (name))
        print("Valid: %s" % (self.valid))
        print("Header:")
        print('    Start Byte:', header['startByte'])
        print('    Command:', header['cmdByte'])
        print('    Packet Length:', header['packetLength'])
        print('    Session Time:', header['sessionTime'])
        if(mode == MESSAGE_MODE_COMMAND):
            print('    Password:', header['password'])
        elif(mode == MESSAGE_MODE_RESPONSE):
            print('    Return Code:', header['returnCode'])
            print('    Unknown 1:', header['unknown1'])
            print('    Ejecting:', header['ejecting'])
            print('    Unkown 2:', header['unknown2'])

        if len(payload) == 0:
            print("Payload: None")
        else :
            print("Payload:")
            for key in payload:
                if(key == 'payloadBytes'):
                    print('    ', key, ': (length: ' + str(len(payload[key])) + ') : ' + self.printByteArray(payload[key]));
                else:
                    print('    ', key , ':', payload[key])
        print("-------------------------------------------------------------")
        print()





    def decodeHeader(self, mode, byteArray):
        startByte = self.utilities.getOneByteInt(0, byteArray)
        cmdByte = self.utilities.getOneByteInt(1, byteArray)
        packetLength = self.utilities.getTwoByteInt(2, byteArray)
        responseTime = self.utilities.getFourByteInt(4, byteArray)
        header = {
            'startByte' : startByte,
            'cmdByte' : cmdByte,
            'packetLength' : packetLength,
            'sessionTime': responseTime
        }

        if(mode == MESSAGE_MODE_COMMAND):
            # Command Specific Header Fields
            header['password'] = self.utilities.getTwoByteInt(8, byteArray)
        elif(mode == MESSAGE_MODE_RESPONSE):
            # Payload Specific Header Fields
            header['returnCode'] = self.utilities.getOneByteInt(12, byteArray)
            header['unknown1'] = self.utilities.getOneByteInt(13, byteArray)
            header['ejecting'] = self.utilities.getEjecting(14, byteArray)
            header['unknown2'] = self.utilities.getOneByteInt(15, byteArray)

        self.header = header

        return header



    def validatePacket(self, byteArray, packetLength):
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


class SpecificationsCommand(Packet):
    NAME = "Specifications"


    def __init__(self, mode, byteArray=None, height=800, width=600, colours=None, unknown1=None, maxSize=None, unknown2=None, unknown3=None):
        #super(SubClass,self).__init__( x )
        super(SpecificationsCommand, self).__init__(mode)


        if (byteArray is not None):
            self.header = super(SpecificationsCommand, self).decodeHeader(mode,byteArray)
            self.valid = self.validatePacket(byteArray, self.header['packetLength'])
            if(mode == MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeCommand(byteArray)
            elif(mode == MESSAGE_MODE_RESPONSE):
                self.decodedCommandPayload = self.decodeResponse(byteArray)
            super(SpecificationsCommand, self).printDebug(byteArray, mode, self.NAME, self.header,self.decodedCommandPayload)
        else:
            print("Building new specifications command")


    def decodeCommand(self, byteArray):
        # This command does not have a payload
        return {}

    def decodeResponse(self, byteArray):
        self.maxHeight  = self.utilities.getTwoByteInt(16, byteArray)
        self.maxWidth   = self.utilities.getTwoByteInt(18, byteArray)
        self.maxColours = self.utilities.getTwoByteInt(20, byteArray)
        self.unknown1   = self.utilities.getTwoByteInt(22, byteArray)
        self.maxMsgSize = self.utilities.getTwoByteInt(28, byteArray)
        self.unknown2   = self.utilities.getOneByteInt(30, byteArray)
        self.unknown3   = self.utilities.getFourByteInt(32, byteArray)
        self.payload = {
            'maxHeight' : self.maxHeight,
            'maxWidth'  : self.maxWidth,
            'maxColours': self.maxColours,
            'unknown1'  : self.unknown1,
            'maxMsgSize': self.maxMsgSize,
            'unknown2'  : self.unknown2,
            'unknown3'  : self.unknown3
        }
        return self.payload


class ResetCommand(Packet):
    NAME = "Reset"

    def __init__(self, mode, byteArray=None, returnCode=None, unknown1=None, ejecting=None, unknown2=None):
        super(ResetCommand, self).__init__(mode)
        if (byteArray is not None):
            self.header = super(ResetCommand, self).decodeHeader(mode, byteArray)
            self.valid = self.validatePacket(byteArray, self.header['packetLength'])
            if(mode == MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeCommand(byteArray)
            elif(mode == MESSAGE_MODE_RESPONSE):
                self.decodedCommandPayload = self.decodeResponse(byteArray)
            super(ResetCommand, self).printDebug(byteArray, mode, self.NAME, self.header, self.decodedCommandPayload)
        else:
            print("Building new Reset Command")


    def decodeCommand(self, byteArray):
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
            if(mode == MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeCommand(byteArray)
            elif(mode == MESSAGE_MODE_RESPONSE):
                self.decodedCommandPayload = self.decodeResponse(byteArray)
            super(PrepImageCommand, self).printDebug(byteArray, mode, self.NAME, self.header, self.decodedCommandPayload)
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

    def __init__(self, mode, byteArray=None, sequenceNumber=None, payloadBytes=None, unknown1=None):
        super(SendImageCommand, self).__init__(mode)
        if(byteArray is not None):
            self.header = super(SendImageCommand, self).decodeHeader(mode, byteArray)
            self.valid = self.validatePacket(byteArray, self.header['packetLength'])
            if(mode == MESSAGE_MODE_COMMAND):
                self.decodedCommandPayload = self.decodeCommand(byteArray)
            elif(mode == MESSAGE_MODE_RESPONSE):
                self.decodedCommandPayload = self.decodeResponse(byteArray)
            super(SendImageCommand, self).printDebug(byteArray, mode, self.NAME, self.header, self.decodedCommandPayload)
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
