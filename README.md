# instax_api

[![Build Status](https://img.shields.io/travis/jpwsutton/instax_api/master.svg)](https://travis-ci.org/jpwsutton/instax_api)
[![Coverage Status](https://img.shields.io/coveralls/jpwsutton/instax_api/master.svg)](https://coveralls.io/github/jpwsutton/instax_api?branch=master)

This is a Python Module to interact and print photos to the Fujifilm Instax SP-2 and SP-3 printers.


## Install this library

In order to use this library, you will need to be using Python 3

```
pip3 install instax-api
```

## Usage

```
$ instax-print --help
usage: instax-print [-h] [-i PIN] [-v {1,2,3}] image

positional arguments:
  image                 The location of the image to print.

optional arguments:
  -h, --help            show this help message and exit
  -i PIN, --pin PIN     The pin code to use, default: 1111.
  -v {1,2,3}, --version {1,2,3}
                        The version of Instax Printer to use (1, 2 or 3).
                        Default is 2 (SP-2).                       
```

### Examples:

 - Printing a Photo to an SP-2 printer: `instax-print myPhoto.jpg`
 - Printing a Photo to an SP-3 printer: `instax-print myPhoto.jpg -v 3`
 - Printing a Photo to a printer with a pin that is not the default (1111) `instax-print myPhoto.jpg -i 1234`

### Hints and tips:
 - Make sure you are connected to the correct wifi network, once the printer is turned on, there will be an SSID / WiFi network available that starts with `INSTAX-` followed by 8 numbers. You'll need to connect to this.
 - If you have a static IP address set up on your computer, you'll need to turn on DHCP before attempting to print, the Instax printer will automatically assign you a new address once you connect.
- Some Unix based operating systems may require you to use sudo in order to access the network.
- The printer will automatically turn itself off after roughly 10 minutes of innactivity.
- The instax-print utility will attempt to automatically rotate the image so that it either is correctly printed in portrait, or landscape with the thick bottom edge of the print on the left. If you wish to print your photos in a specific orientation that differs from this, then it's reccomended that you orient your photo in a tool like GIMP first, then strip out the rotation metadata. Once the rotation metadata has been stripped, the photo will need to be in a portrait orientation relative to the finished print (e.g. thick edge at the bottom). 

## Install Manually

```
git clone https://github.com/jpwsutton/instax_api.git
cd instax_api
python3 setup.py install
```
