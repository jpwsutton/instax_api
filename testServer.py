#!/usr/bin/env python3
"""Instax SP-2 Test Server Wrapper.

Author: James Sutton 2017 - jsutton.co.uk

This wrapper can be used to start a test server implementation.
You can configure a number of useful parameters to use whist the server is
running.
Parameters:
 - Verbose (Default False)
 - JSON Log File (Default ddmmyy-hhmmss.json)
 - Port (Default 8080)
 - Photo Destination Directory: (Default: images)
 - Battery Level: (Default 100%)
 - Prints Remaining: (Default 10)
 - Total Prints in History: (Default 20)

"""
import argparse
import datetime
import logging
import instax


print("---------- Instax SP-2 Test Server ---------- ")


def remaining_type(x):
    """Validate Remaining count is between 0 and 10."""
    x = int(x)
    if x < 10 and x >= 0:
        raise argparse.ArgumentTypeError("Remaining must be between 0 and 10.")
    return x


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true", default=False,
                    help="Print Verbose log messages to console.")
parser.add_argument("-D", "--debug", action="store_true", default=False,
                        help="Logs extra debug data to log.")
parser.add_argument("-l", "--log", action="store_true", default=False,
                        help="Log information to log file ddmmyy-hhmmss-server.log")
parser.add_argument("-o", "--host", default='0.0.0.0',
                    help="The Host IP to expose the server on.")
parser.add_argument("-p", "--port", type=int, default=8080,
                    help="The port to expose the server on.")
parser.add_argument("-d", "--dest", default="images",
                    help="The Directory to save incoming photos,"
                    "default: 'images'")
parser.add_argument("-b", "--battery", type=int, choices=range(0, 4),
                    default=2, help="The Battery level of the printer"
                    " 0-4, default: 2")
parser.add_argument("-r", "--remaining", type=remaining_type, default=10,
                    help="The number of remaining prints 0-10, default: 10")
parser.add_argument("-t", "--total", type=int, default=20,
                    help="The total number of prints in the printers lifetime"
                    ", default 20")
parser.add_argument("-V", "--version", type=int, default=2,
                    help="The Instax SP-* version, 2 or 3, default is 2")
args = parser.parse_args()

logLevel = logging.INFO
if args.debug:
    logLevel = logging.DEBUG

logger = logging.getLogger('instax_server')
logger.setLevel(logLevel)

# Create Log Formatter
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

# Create Console Handler
ch = logging.StreamHandler()
ch.setLevel(logLevel)
ch.setFormatter(formatter)
logger.addHandler(ch)

# If Not specified, set the log file to a datestamp.
if args.log:
    logFilename = '{0:%Y-%m-%d.%H:%M:%S-server.log}'.format(datetime.datetime.now())
    fh = logging.FileHandler(logFilename)
    fh.setLevel(logLevel)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


testServer = instax.DebugServer(host=args.host, 
                               port=args.port, dest=args.dest,
                               battery=args.battery, remaining=args.remaining,
                               total=args.total, version=args.version)
testServer.start()
