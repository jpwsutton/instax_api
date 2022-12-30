#!/usr/bin/env python3
"""Instax SP Print Script.

Author: James Sutton 2017 - jsutton.co.uk

This can be used to print an image to a Fujifilm Instax SP-2 printer.
Parameters:
 - JSON Log File (Default ddmmyy-hhmmss.json)
 - Image to print
 - Port (Default 8080)
 - Host (Default 192.168.0.251)

"""
import argparse
import datetime
import sys

from loguru import logger

from instax.instaxImage import InstaxImage
from instax.sp2 import SP2
from instax.sp3 import SP3


def printPrinterInfo(info):
    """Log Printer information"""
    logger.info("Model: %s" % info["model"])
    logger.info("Firmware: %s" % info["version"]["firmware"])
    logger.info("Battery State: %s" % info["battery"])
    logger.info("Prints Remaining: %d" % info["printCount"])
    logger.info("Total Lifetime Prints: %d" % info["count"])
    logger.info("")


# https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
def printProgress(count, total, status=""):
    # logger.info(status)
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = "=" * filled_len + "-" * (bar_len - filled_len)
    sys.stdout.write("[{}] {}{} ...{}\r".format(bar, percents, "%", status))
    sys.stdout.flush()  # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", default=False, help=argparse.SUPPRESS)
    parser.add_argument("-l", "--log", action="store_true", default=False, help=argparse.SUPPRESS)
    parser.add_argument("-o", "--host", default="192.168.0.251", help=argparse.SUPPRESS)
    parser.add_argument("-p", "--port", type=int, default=8080, help=argparse.SUPPRESS)
    parser.add_argument("-i", "--pin", type=int, default=1111, help="The pin code to use, default: 1111.")
    parser.add_argument(
        "-e",
        "--preview",
        action="store_true",
        default=False,
        help="Show a preview of the image before it is printed, then exit.",
    )
    parser.add_argument("-t", "--timeout", type=int, default=10, help=argparse.SUPPRESS)
    parser.add_argument(
        "-v",
        "--version",
        type=int,
        default=2,
        choices=[1, 2, 3],
        help="The version of Instax Printer to use (1, 2 or 3). Default is 2 (SP-2).",
    )
    parser.add_argument("image", help="The location of the image to print.")
    args = parser.parse_args()

    if not args.debug:
        logger.remove()
        logger.add(sys.stderr, level="INFO")

    # If Not specified, set the log file to a datestamp.
    if args.log:
        logFilename = f"{datetime.datetime.now():%Y-%m-%d.%H-%M-%S.log}"
        logger.add(logFilename)

    logger.info("--- Instax Printer Python Client ---")
    logger.info("")
    myInstax = None

    if args.version == 1:
        logger.info("Attempting to print to an Instax SP-1 printer.")
        # TODO - Need to find an SP-2 to test with.
    elif args.version == 2:
        logger.info("Attempting to print to an Instax SP-2 printer.")
        myInstax = SP2(ip=args.host, port=args.port, pinCode=args.pin, timeout=args.timeout)
    elif args.version == 3:
        logger.info("Attempting to print to an Instax SP-3 printer.")
        # Warning, this does not work in production yet.
        myInstax = SP3(ip=args.host, port=args.port, pinCode=args.pin, timeout=args.timeout)
    else:
        logger.error("Invalid Instax printer version given")
        exit(1)

    if args.preview is True:
        # Going to preview the image as it will be printed
        logger.info(f"Previewing Image: {args.image}")
        instaxImage = InstaxImage(type=args.version)
        instaxImage.loadImage(args.image)
        instaxImage.convertImage()
        instaxImage.previewImage()
        logger.info("Preview complete, exiting.")
        exit(0)
    else:
        # Attempt print
        logger.info("Connecting to Printer.")
        info = myInstax.getPrinterInformation()
        printPrinterInfo(info)

        logger.info("Printing Image: %s" % args.image)
        # Initialize The Instax Image
        instaxImage = InstaxImage(type=args.version)
        instaxImage.loadImage(args.image)
        instaxImage.convertImage()
        # Save a copy of the converted bitmap
        # instaxImage.saveImage("test.bmp")
        # Preview the image that is about to print
        # instaxImage.previewImage()
        encodedImage = instaxImage.encodeImage()
        myInstax.printPhoto(encodedImage, printProgress)
        logger.info("Thank you for using instax-print!")
        logger.info(
            r"""
            \   /\
            )  ( ')
            (  /  )
            \(___)|"""
        )
