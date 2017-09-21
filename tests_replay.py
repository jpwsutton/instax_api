"""
Instax SP2 Test File.

@jpwsutton 2016/17
"""
from instax import PacketFactory, Packet, SpecificationsCommand,  \
    VersionCommand, PrintCountCommand, ModelNameCommand, PrePrintCommand
import time
import unittest
import json
from pprint import pprint


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

    def test_process_log(self):
        """Import a json log and replay the messages."""
        filename = "priming.json"
        json_data = open(filename)
        data = json.load(json_data)
        json_data.close()
        print()
        decodedPacketList = []
        for packet in data:
            readBytes = bytearray.fromhex(packet['bytes'])
            packetFactory = PacketFactory()
            decodedPacket = packetFactory.decode(readBytes)
            # decodedPacket.printDebug()
            packetObj = decodedPacket.getPacketObject()
            decodedPacketList.append(packetObj)

        pprint(decodedPacketList)
        with open('log2.json', 'w') as outfile:
            json.dump(decodedPacketList, outfile, indent=4)








if __name__ == '__main__':

    unittest.main()
