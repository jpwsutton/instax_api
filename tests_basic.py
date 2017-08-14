"""
Instax SP2 Test File.

@jpwsutton 2016/17
"""
from instax import PacketFactory, Packet, SpecificationsCommand, VersionCommand
import time
import unittest


class PacketTests(unittest.TestCase):
    """
    Instax-SP2 Packet Test Class.

    A series of tests to verify that all commands and responses can be
    correctly encoded and decoded.
    """

    def helper_verify_header(self, header, direction, type, length, time,
                             pin=None):
        """Verify the Header of a packet."""
        self.assertEqual(header['startByte'], direction)
        self.assertEqual(header['cmdByte'], type)
        self.assertEqual(header['packetLength'], length)
        self.assertEqual(header['sessionTime'], time)
        if direction == Packet.MESSAGE_MODE_COMMAND:
            self.assertEqual(header['password'], pin)

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
        resPacket = SpecificationsCommand(Packet.MESSAGE_MODE_RESPONSE,
                                          maxHeight=800,
                                          maxWidth=600,
                                          maxColours=256,
                                          unknown1=10,
                                          maxMsgSize=60000,
                                          unknown2=16,
                                          unknown3=0)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   Packet.RTN_E_RCV_FRAME,
                                                   None)
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedResponse)
        # decodedPacket.printDebug()
        postHeader = decodedPacket.header
        self.helper_verify_header(postHeader,
                                  Packet.MESSAGE_MODE_RESPONSE,
                                  Packet.MESSAGE_TYPE_SPECIFICATIONS,
                                  len(encodedResponse),
                                  resPacket.encodedSessionTime)

        # Verify Payload
        # print(decodedPacket.payload)
        self.assertEqual(decodedPacket.payload['maxHeight'], 800)
        self.assertEqual(decodedPacket.payload['maxWidth'], 600)
        self.assertEqual(decodedPacket.payload['maxColours'], 256)
        self.assertEqual(decodedPacket.payload['unknown1'], 10)
        self.assertEqual(decodedPacket.payload['maxMsgSize'], 60000)
        self.assertEqual(decodedPacket.payload['unknown2'], 16)
        self.assertEqual(decodedPacket.payload['unknown3'], 0)

    def test_premade_resp_specifications(self):
        """Test Decoding a Specifications Response with an existing payload."""
        msg = bytearray.fromhex('2a4f 0030 e759 eede 0000 0000 0000 0027 0258'
                                ' 0320 0100 000a 0000 0000 ea60 1000 0000 0000'
                                ' 0000 0000 0000 0000 fa41 0d0a')
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(msg)
        self.assertEqual(decodedPacket.payload['maxHeight'], 800)
        self.assertEqual(decodedPacket.payload['maxWidth'], 600)
        self.assertEqual(decodedPacket.payload['maxColours'], 256)
        self.assertEqual(decodedPacket.payload['unknown1'], 10)
        self.assertEqual(decodedPacket.payload['maxMsgSize'], 60000)
        self.assertEqual(decodedPacket.payload['unknown2'], 16)
        self.assertEqual(decodedPacket.payload['unknown3'], 0)

    def test_encode_cmd_version(self):
        """Test the process of encoding a spcecifications command."""
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

    def test_premade_resp_version(self):
        """Test Decoding a Version Response with an existing payload."""
        msg = bytearray.fromhex('2ac0 001c e759 eede 0000'
                                ' 0000 0000 0027 0101 0113'
                                ' 0000 0000 fbb0 0d0a')
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(msg)
        self.assertEqual(decodedPacket.payload['unknown1'], 257)
        self.assertEqual(decodedPacket.payload['firmware'], '01.13')
        self.assertEqual(decodedPacket.payload['hardware'], '00.00')


if __name__ == '__main__':

    unittest.main()
