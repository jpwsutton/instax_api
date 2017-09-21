"""
Instax SP2 Test File.

@jpwsutton 2016/17
"""
from instax import PacketFactory, Packet, SpecificationsCommand,  \
    VersionCommand, PrintCountCommand, ModelNameCommand, PrePrintCommand, \
    PrinterLockCommand, ResetCommand, PrepImageCommand
import time
import unittest


class PacketTests(unittest.TestCase):
    """
    Instax-SP2 Packet Test Class.

    A series of tests to verify that all commands and responses can be
    correctly encoded and decoded.
    """

    def helper_verify_header(self, header, direction, type, length, time,
                             pin=None, returnCode=None, unknown1=None,
                             ejecting=None, battery=None, printCount=None):
        """Verify the Header of a packet."""
        self.assertEqual(header['startByte'], direction)
        self.assertEqual(header['cmdByte'], type)
        self.assertEqual(header['packetLength'], length)
        self.assertEqual(header['sessionTime'], time)
        if direction == Packet.MESSAGE_MODE_COMMAND:
            self.assertEqual(header['password'], pin)
        if direction == Packet.MESSAGE_MODE_RESPONSE:
            self.assertEqual(header['returnCode'], returnCode)
            # self.assertEqual(header['unknown1'], unknown1)
            self.assertEqual(header['ejecting'], ejecting)
            self.assertEqual(header['battery'], battery)
            self.assertEqual(header['printCount'], printCount)

    def test_encode_cmd_specifications(self):
        """Test the process of encoding a spcecifications command."""
        # Create Specifications Command Packet
        sessionTime = int(round(time.time() * 1000))
        pinCode = 1111
        cmdPacket = SpecificationsCommand(Packet.MESSAGE_MODE_COMMAND)
        # Encode the command to raw byte array
        encodedCommand = cmdPacket.encodeCommand(sessionTime, pinCode)
        # Decode the command back into a packet object
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedCommand)
        # decodedPacket.printDebug()
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_COMMAND,
                                  Packet.MESSAGE_TYPE_SPECIFICATIONS,
                                  len(encodedCommand),
                                  cmdPacket.encodedSessionTime,
                                  pinCode)

    def test_encode_resp_specifications(self):
        """Test the process of encoding a specifications response."""
        sessionTime = int(round(time.time() * 1000))
        returnCode = Packet.RTN_E_RCV_FRAME
        ejecting = 0
        battery = 2
        printCount = 7
        resPacket = SpecificationsCommand(Packet.MESSAGE_MODE_RESPONSE,
                                          maxHeight=800,
                                          maxWidth=600,
                                          maxColours=256,
                                          unknown1=10,
                                          maxMsgSize=60000,
                                          unknown2=16,
                                          unknown3=0)
        encodedResponse = resPacket.encodeResponse(sessionTime, returnCode,
                                                   ejecting, battery,
                                                   printCount)
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedResponse)
        # decodedPacket.printDebug()
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_RESPONSE,
                                  Packet.MESSAGE_TYPE_SPECIFICATIONS,
                                  len(encodedResponse),
                                  resPacket.encodedSessionTime,
                                  returnCode=returnCode,
                                  ejecting=ejecting,
                                  battery=battery,
                                  printCount=printCount)

        # Verify Payload
        # print(decodedPacket.payload)
        self.assertEqual(decodedPacket.payload['maxHeight'], 800)
        self.assertEqual(decodedPacket.payload['maxWidth'], 600)
        self.assertEqual(decodedPacket.payload['maxColours'], 256)
        self.assertEqual(decodedPacket.payload['unknown1'], 10)
        self.assertEqual(decodedPacket.payload['maxMsgSize'], 60000)
        self.assertEqual(decodedPacket.payload['unknown2'], 16)
        self.assertEqual(decodedPacket.payload['unknown3'], 0)

    def test_encode_cmd_version(self):
        """Test the process of encoding a version command."""
        # Create Specifications Command Packet
        sessionTime = int(round(time.time() * 1000))
        pinCode = 1111
        cmdPacket = VersionCommand(Packet.MESSAGE_MODE_COMMAND)
        # Encode the command to raw byte array
        encodedCommand = cmdPacket.encodeCommand(sessionTime, pinCode)
        # Decode the command back into a packet object
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedCommand)
        # decodedPacket.printDebug()
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_COMMAND,
                                  Packet.MESSAGE_TYPE_PRINTER_VERSION,
                                  len(encodedCommand),
                                  cmdPacket.encodedSessionTime,
                                  pinCode)

    def test_encode_resp_version(self):
        """Test the process of encoding a version response."""
        sessionTime = int(round(time.time() * 1000))
        returnCode = Packet.RTN_E_RCV_FRAME
        ejecting = 0
        battery = 2
        printCount = 7
        resPacket = VersionCommand(Packet.MESSAGE_MODE_RESPONSE,
                                   unknown1=254,
                                   firmware=275,
                                   hardware=0)
        encodedResponse = resPacket.encodeResponse(sessionTime, returnCode,
                                                   ejecting, battery,
                                                   printCount)
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedResponse)
        # decodedPacket.printDebug()
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_RESPONSE,
                                  Packet.MESSAGE_TYPE_PRINTER_VERSION,
                                  len(encodedResponse),
                                  resPacket.encodedSessionTime,
                                  returnCode=returnCode,
                                  ejecting=ejecting,
                                  battery=battery,
                                  printCount=printCount)

        # Verify Payload
        self.assertEqual(decodedPacket.payload['unknown1'], 254)
        self.assertEqual(decodedPacket.payload['firmware'], '01.13')
        self.assertEqual(decodedPacket.payload['hardware'], '00.00')

    def test_encode_cmd_printCount(self):
        """Test the process of encoding a print count command."""
        # Create Print Count Command Packet
        sessionTime = int(round(time.time() * 1000))
        pinCode = 1111
        cmdPacket = PrintCountCommand(Packet.MESSAGE_MODE_COMMAND)
        # Encode the command to raw byte array
        encodedCommand = cmdPacket.encodeCommand(sessionTime, pinCode)
        # Decode the command back into a packet object
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedCommand)
        # decodedPacket.printDebug()
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_COMMAND,
                                  Packet.MESSAGE_TYPE_PRINT_COUNT,
                                  len(encodedCommand),
                                  cmdPacket.encodedSessionTime,
                                  pinCode)

    def test_encode_resp_printCount(self):
        """Test the process of encoding a print count response."""
        sessionTime = int(round(time.time() * 1000))
        returnCode = Packet.RTN_E_RCV_FRAME
        ejecting = 0
        battery = 2
        printCount = 7
        printHistory = 42
        resPacket = PrintCountCommand(Packet.MESSAGE_MODE_RESPONSE,
                                      printHistory=printHistory)
        encodedResponse = resPacket.encodeResponse(sessionTime, returnCode,
                                                   ejecting, battery,
                                                   printCount)
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedResponse)
        # decodedPacket.printDebug()
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_RESPONSE,
                                  Packet.MESSAGE_TYPE_PRINT_COUNT,
                                  len(encodedResponse),
                                  resPacket.encodedSessionTime,
                                  returnCode=returnCode,
                                  ejecting=ejecting,
                                  battery=battery,
                                  printCount=printCount)

        # Verify Payload
        self.assertEqual(decodedPacket.payload['printHistory'], printHistory)

    def test_encode_cmd_modelName(self):
        """Test the process of encoding a model name command."""
        # Create Model Name Command Packet
        sessionTime = int(round(time.time() * 1000))
        pinCode = 1111
        cmdPacket = ModelNameCommand(Packet.MESSAGE_MODE_COMMAND)
        # Encodde the command to raw byte array
        encodedCommand = cmdPacket.encodeCommand(sessionTime, pinCode)
        # Decode the command back into a packet object
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedCommand)
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_COMMAND,
                                  Packet.MESSAGE_TYPE_MODEL_NAME,
                                  len(encodedCommand),
                                  cmdPacket.encodedSessionTime,
                                  pinCode)

    def test_encode_resp_modelName(self):
        """Test the process of encoding a model name response."""
        sessionTime = int(round(time.time() * 1000))
        returnCode = Packet.RTN_E_RCV_FRAME
        ejecting = 0
        battery = 2
        printCount = 7
        modelName = 'SP-2'
        resPacket = ModelNameCommand(Packet.MESSAGE_MODE_RESPONSE,
                                     modelName=modelName)
        encodedResponse = resPacket.encodeResponse(sessionTime, returnCode,
                                                   ejecting, battery,
                                                   printCount)
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedResponse)
        # decodedPacket.printDebug()
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_RESPONSE,
                                  Packet.MESSAGE_TYPE_MODEL_NAME,
                                  len(encodedResponse),
                                  resPacket.encodedSessionTime,
                                  returnCode=returnCode,
                                  ejecting=ejecting,
                                  battery=battery,
                                  printCount=printCount)

        # Verify Payload
        self.assertEqual(decodedPacket.payload['modelName'], modelName)

    def test_encode_cmd_prePrint(self):
        """Test the process of encoding a prePrint command."""
        # Create Model Name Command Packet
        sessionTime = int(round(time.time() * 1000))
        pinCode = 1111
        cmdNumber = 8
        cmdPacket = PrePrintCommand(Packet.MESSAGE_MODE_COMMAND,
                                    cmdNumber=cmdNumber)
        # Encodde the command to raw byte array
        encodedCommand = cmdPacket.encodeCommand(sessionTime, pinCode)
        # Decodee the command back into a packet object
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedCommand)
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_COMMAND,
                                  Packet.MESSAGE_TYPE_PRE_PRINT,
                                  len(encodedCommand),
                                  cmdPacket.encodedSessionTime,
                                  pinCode)
        # Verify Payload
        self.assertEqual(decodedPacket.payload['cmdNumber'], cmdNumber)

    def test_encode_resp_prePrint(self):
        """Test the process of encoding a pre print response."""
        sessionTime = int(round(time.time() * 1000))
        returnCode = Packet.RTN_E_RCV_FRAME
        ejecting = 0
        battery = 2
        printCount = 7
        cmdNumber = 8
        respNumber = 1
        resPacket = PrePrintCommand(Packet.MESSAGE_MODE_RESPONSE,
                                    cmdNumber=cmdNumber,
                                    respNumber=respNumber)
        encodedResponse = resPacket.encodeResponse(sessionTime, returnCode,
                                                   ejecting, battery,
                                                   printCount)
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedResponse)
        # decodedPacket.printDebug()
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_RESPONSE,
                                  Packet.MESSAGE_TYPE_PRE_PRINT,
                                  len(encodedResponse),
                                  resPacket.encodedSessionTime,
                                  returnCode=returnCode,
                                  ejecting=ejecting,
                                  battery=battery,
                                  printCount=printCount)

        # Verify Payload
        self.assertEqual(decodedPacket.payload['cmdNumber'], cmdNumber)
        self.assertEqual(decodedPacket.payload['respNumber'], respNumber)

    def test_encode_cmd_lock(self):
        """Test encoding a Lock Printer Command."""
        sessionTime = int(round(time.time() * 1000))
        pinCode = 1111
        lockState = 1
        cmdPacket = PrinterLockCommand(Packet.MESSAGE_MODE_COMMAND,
                                       lockState=lockState)
        encodedCommand = cmdPacket.encodeCommand(sessionTime, pinCode)
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedCommand)
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_COMMAND,
                                  Packet.MESSAGE_TYPE_LOCK_DEVICE,
                                  len(encodedCommand),
                                  cmdPacket.encodedSessionTime,
                                  pinCode)
        # Verify Payload
        self.assertEqual(decodedPacket.payload['lockState'], lockState)

    def test_encode_resp_lock(self):
        """Test encoding a Lock Printer Response."""
        sessionTime = int(round(time.time() * 1000))
        returnCode = Packet.RTN_E_RCV_FRAME
        ejecting = 0
        battery = 2
        printCount = 7
        resPacket = PrinterLockCommand(Packet.MESSAGE_MODE_RESPONSE)
        encodedResponse = resPacket.encodeResponse(sessionTime, returnCode,
                                                   ejecting, battery,
                                                   printCount)
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedResponse)
        # decodedPacket.printDebug()
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_RESPONSE,
                                  Packet.MESSAGE_TYPE_LOCK_DEVICE,
                                  len(encodedResponse),
                                  resPacket.encodedSessionTime,
                                  returnCode=returnCode,
                                  ejecting=ejecting,
                                  battery=battery,
                                  printCount=printCount)

    def test_encode_cmd_reset(self):
        """Test encoding a Reset Command."""
        sessionTime = int(round(time.time() * 1000))
        pinCode = 1111
        cmdPacket = ResetCommand(Packet.MESSAGE_MODE_COMMAND)
        encodedCommand = cmdPacket.encodeCommand(sessionTime, pinCode)
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedCommand)
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_COMMAND,
                                  Packet.MESSAGE_TYPE_RESET,
                                  len(encodedCommand),
                                  cmdPacket.encodedSessionTime,
                                  pinCode)

    def test_encode_resp_reset(self):
        """Test encoding a Reset Response."""
        sessionTime = int(round(time.time() * 1000))
        returnCode = Packet.RTN_E_RCV_FRAME
        ejecting = 0
        battery = 2
        printCount = 7
        resPacket = ResetCommand(Packet.MESSAGE_MODE_RESPONSE)
        encodedResponse = resPacket.encodeResponse(sessionTime, returnCode,
                                                   ejecting, battery,
                                                   printCount)
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedResponse)
        # decodedPacket.printDebug()
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_RESPONSE,
                                  Packet.MESSAGE_TYPE_RESET,
                                  len(encodedResponse),
                                  resPacket.encodedSessionTime,
                                  returnCode=returnCode,
                                  ejecting=ejecting,
                                  battery=battery,
                                  printCount=printCount)

    def test_encode_cmd_prep(self):
        """Test encoding a Prep Image Command."""
        sessionTime = int(round(time.time() * 1000))
        pinCode = 1111
        format = 16
        options = 128
        imgLength = 1440000
        cmdPacket = PrepImageCommand(Packet.MESSAGE_MODE_COMMAND,
                                     format=format,
                                     options=options,
                                     imgLength=imgLength)
        encodedCommand = cmdPacket.encodeCommand(sessionTime, pinCode)
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedCommand)
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_COMMAND,
                                  Packet.MESSAGE_TYPE_PREP_IMAGE,
                                  len(encodedCommand),
                                  cmdPacket.encodedSessionTime,
                                  pinCode)
        # Verify Payload
        self.assertEqual(decodedPacket.payload['format'], format)
        self.assertEqual(decodedPacket.payload['options'], options)
        self.assertEqual(decodedPacket.payload['imgLength'], imgLength)

    def test_encode_resp_prep(self):
        """Test encoding a Prep Image Response."""
        sessionTime = int(round(time.time() * 1000))
        returnCode = Packet.RTN_E_RCV_FRAME
        ejecting = 0
        battery = 2
        printCount = 7
        maxLen = 60000
        resPacket = PrepImageCommand(Packet.MESSAGE_MODE_RESPONSE,
                                     maxLen=maxLen)
        encodedResponse = resPacket.encodeResponse(sessionTime, returnCode,
                                                   ejecting, battery,
                                                   printCount)
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedResponse)
        # decodedPacket.printDebug()
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_RESPONSE,
                                  Packet.MESSAGE_TYPE_PREP_IMAGE,
                                  len(encodedResponse),
                                  resPacket.encodedSessionTime,
                                  returnCode=returnCode,
                                  ejecting=ejecting,
                                  battery=battery,
                                  printCount=printCount)

        # Verify Payload
        self.assertEqual(decodedPacket.payload['maxLen'], maxLen)

    def test_encode_cmd_send(self):
        """Test encoding a Send Image Command."""
        pass

    def test_encode_resp_send(self):
        """Test encoding a Send Image Response."""
        pass


if __name__ == '__main__':

    unittest.main()
