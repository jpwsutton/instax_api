# instax_api

[![Build Status](https://img.shields.io/travis/jpwsutton/instax_api/master.svg)](https://travis-ci.org/jpwsutton/instax_api)
[![Coverage Status](https://img.shields.io/coveralls/jpwsutton/instax_api/master.svg)](https://coveralls.io/github/jpwsutton/instax_api?branch=master)

This is an experimental Python Module to interact and print photos to the Fujifilm Instax SP-2 printer.


## Install this library

In order to use this library, you will need to be using Python 3

```
pip3 install instax-api
```

## Usage

This library is still in a developmental state and so your mileage may vary.

```
$ instax-print --help
usage: instax-print [-h] [-v] [-l LOG] [-o HOST] [-p PORT] [-i PIN]
                    [-t TIMEOUT]
                    image

positional arguments:
  image                 The location of the image to print.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Print Verbose log messages to console.
  -l LOG, --log LOG     The location to store the JSON log,by default: ddmmyy-
                        hhmmss-log.json
  -o HOST, --host HOST  The Host IP to connect to the server on.
  -p PORT, --port PORT  The port to connect to the server on.
  -i PIN, --pin PIN     The pin code to use, default: 1111.
  -t TIMEOUT, --timeout TIMEOUT
                        The timeout to use when communicating.
```

## Install Manually

```
git clone https://github.com/jpwsutton/instax_api.git
cd instax_api
python3 setup.py install
```
