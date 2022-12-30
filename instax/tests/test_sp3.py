"""
Instax SP* Socket Tests

James Sutton 2020
"""
import threading
import unittest

import pytest

from instax.debugServer import DebugServer
from instax.instaxImage import InstaxImage
from instax.sp3 import SP3

test_image = "instax/tests/test_image.png"
server_batt = 2
server_remain = 10
server_total = 20

progress_log = []


def updateProgress(count, total, status=""):
    progress_log.append({"count": count, "total": total, "status": status})


class SP3Tests(unittest.TestCase):
    """
    Tests on the SP2 class
    """

    @pytest.fixture(autouse=True)
    def debug_server(self):
        server = DebugServer(
            host="0.0.0.0", port=0, version=3, battery=server_batt, remaining=server_remain, total=server_total
        )
        self.server_port = server.getPort()
        print(f"SP-2 Server running on port {self.server_port}")

        thread = threading.Thread(target=server.start)
        thread.daemon = True
        thread.start()
        yield server

    def test_get_printer_info(self):
        # Getting Printer Information
        sp2 = SP3(ip="0.0.0.0", port=self.server_port)
        info = sp2.getPrinterInformation()
        # print(info)
        self.assertEqual(info["model"], "SP-3")
        self.assertEqual(info["battery"], 3)  # Something odd here...
        self.assertEqual(info["printCount"], 4)  # Something odd here...
        self.assertEqual(info["count"], server_total)

    def test_print_photo(self):
        sp2 = SP3(ip="0.0.0.0", port=self.server_port)

        instaxImage = InstaxImage(type=3)
        instaxImage.loadImage(test_image)
        instaxImage.convertImage()
        # Save a copy of the converted bitmap
        # instaxImage.saveImage("test.bmp")
        # Preview the image that is about to print
        # instaxImage.previewImage()
        encodedImage = instaxImage.encodeImage()
        sp2.printPhoto(encodedImage, updateProgress)
        # print(progress_log)
        self.assertEqual(progress_log[-1]["count"], 100)
        self.assertTrue("Print is complete!" in progress_log[-1]["status"])


if __name__ == "__main__":

    unittest.main()
