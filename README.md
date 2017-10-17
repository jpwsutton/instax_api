# instax_api
An Api for the Fujifilm Instax SP-2 printer written in Python

[![Build Status](https://img.shields.io/travis/jpwsutton/instax_api/master.svg)](https://travis-ci.org/jpwsutton/instax_api)
[![Coverage Status](https://img.shields.io/coveralls/jpwsutton/instax_api/master.svg)](https://coveralls.io/github/jpwsutton/instax_api?branch=master)

This is an experimental Python Module to interact and print photos to the Fujifilm Instax SP-2 printer.


## Setup

```
git clone https://github.com/jpwsutton/instax_api.git
cd instax_api
python setup.py install
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

## Developing using the Virtualenv environment

* Make sure you have virtualenv installed : `pip install virtualenv`.
* If you haven't created it yet, create the virtual environment: `virtualenv env -p python3`.
* Activate the environment: `source env/bin/activate`.
* Install packages from requirements.txt: `pip install -r requirements.txt --upgrade`.
* When you are finished, just use `deactivate` to end your session.

## Running the Test Server

The Test server was written to allow developers to simulate an Instax SP-2 printer in order to test the client.

In order to connect the application, the device running the test server will need to be hosting a WiFi network with an SSID starting with `INSTAX-` followed by a number of hex characters (This would usually be the MAC address of the printer). In my case, I used a Raspberry Pi Model 3 to host the wireless network and run the Test Server on.
Once you have set up the pi following these instructions: Tutorial link goes here..., you will need to usually run these three commands :

```
sudo service udhcpd start
sudo hostapd /etc/hostapd/hostapd.conf (This will keep running so do it in another tab or bg)
sudo ifconfig wlan0 192.168.0.251
```

Then run: `./bin/testServer.py`

## Running tests
Simply run the command: `py.test instax/tests/*.py`


## Inspecting Packets in Wireshark
* Useful filter: `tcp.port == 8080 && tcp.flags.push == 1`
