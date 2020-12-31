"""Fujifilm Instax SP-4 (mini-link) Packet Library.

This packet library can be used to encode and decode packets to be sent to
or recieved from a Fujifilm Instax SP-4 (mini-link) bluetooth device. It is
designed to be used with the instax_api Python Library.
"""
import logging

class PacketFactoryBle(object):
    """Packet Factory BLE.

    Used to generate new packets and to decode existing packets.
    """


    def __init__(self):
        """Init for packet factory."""
        pass