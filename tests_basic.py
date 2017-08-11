"""
Instax SP2 Test File.

@jpwsutton 2016/17
"""
from instax import PacketFactory, Packet, SpecificationsCommand
import time
import unittest


class PacketTests(unittest.TestCase):
    """
    Instax-SP2 Packet Test Class.

    A series of tests to verify that all commands and responses can be
    correctly encoded and decoded.
    """

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
        self.assertEqual(postHeader['startByte'], 36)
        self.assertEqual(postHeader['cmdByte'],
                         Packet.MESSAGE_TYPE_SPECIFICATIONS)
        self.assertEqual(postHeader['packetLength'], len(encodedCommand))
        self.assertEqual(postHeader['sessionTime'],
                         cmdPacket.encodedSessionTime)
        self.assertEqual(postHeader['password'], pinCode)

    def test_encode_resp_specifications(self):
        """Test the process of encoding a specifications response."""
        sessionTime = int(round(time.time() * 1000))
        resPacket = SpecificationsCommand(Packet.MESSAGE_MODE_RESPONSE,
                                          height=800,
                                          width=600,
                                          colours=256,
                                          unknown1=10,
                                          maxSize=60000,
                                          unknown2=16,
                                          unknown3=0)
        encodedResponse = resPacket.encodeResponse(sessionTime,
                                                   Packet.RTN_E_RCV_FRAME,
                                                   None)
        packetFactory = PacketFactory()
        decodedPacket = packetFactory.decode(encodedResponse)
        # decodedPacket.printDebug()


if __name__ == '__main__':

    unittest.main()
