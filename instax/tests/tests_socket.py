"""
Instax SP* Socket Tests

James Sutton 2020
"""
from instax import DebugServer, SP2
import time
import unittest
import threading
import pytest


class SocketTests(unittest.TestCase):
    """
    Very basic first pass socket test to make sure a simple command works
    """

    @pytest.fixture(autouse=True)
    def test_server(self):
        server = DebugServer(host='0.0.0.0', port=0)
        self.server_port = server.getPort()
        print(f"Server running on port {self.server_port}")
       
        thread = threading.Thread(target=server.start)
        thread.daemon = True
        thread.start()
        yield server

    def test_send_recieve_command(self):
        sp2 = SP2(ip="0.0.0.0", port=self.server_port)
        sp2.connect()
        model_name = sp2.getPrinterModelName().payload['modelName']
        print(f"Model name returned was: {model_name}")
        sp2.close()
        self.assertEqual('SP-2', model_name)

if __name__ == '__main__':

    unittest.main()
