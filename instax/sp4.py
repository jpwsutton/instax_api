"""Main SP4 / mini-link Interface class."""


import time
import queue
import sys
import logging

class SP4:
    """SP4 Client Interface."""

    def __init__(self, port='/dev/rfcomm0', timeout=10):
        """Initialise the client."""
        self.port = port
        self.timeout = timeout
        #self.packetFactory = PacketFactory()