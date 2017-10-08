# instax_api
An Api for the Fujifilm Instax SP-2 printer written in Python

[![Build Status](https://img.shields.io/travis/jpwsutton/instax_api/master.svg)](https://travis-ci.org/jpwsutton/instax_api)
[![Coverage Status](https://img.shields.io/coveralls/jpwsutton/instax_api/master.svg)](https://coveralls.io/github/jpwsutton/instax_api?branch=master)

This is an experimental Python Module to interact and print photos to the Fujifilm Instax SP-2 printer.

Currently there is nothing here yet as I'm still reverse engineering the protocol, so watch this space.

Protocol Information: Check the [Wiki](https://github.com/jpwsutton/instax_api/wiki) for more information about the Instax Protocol.




## Using the Virtualenv environment

* Make sure you have virtualenv installed : `pip install virtualenv`.
* If you haven't created it yet, create the virtual environment: `virtualenv env -p python3`.
* Activate the environment: `source env/bin/activate`.
* Install packages from requirements.txt: `pip install -r requirements.txt --upgrade`.
* When you are finished, just use `deactivate` to end your session.

## Running the Test Server

The Test server was written to allow developers to simulate an Instax SP-2 printer in order to reverse engineer the incoming messages sent by official client applications e.g. the Android App. It is currently capable of listening for incoming connections and receiving images sent by the app. However it is not yet 100% compatible and will crash the app once the image has been sent.

In order to connect the application, the device running the test server will need to be hosting a WiFi network with an SSID starting with `INSTAX-` followed by a number of hex characters (This would usually be the MAC address of the printer). In my case, I used a Raspberry Pi Model 3 to host the wireless network and run the Test Server on.
Once you have set up the pi following these instructions: Tutorial link goes here..., you will need to usually run these three commands :

```
sudo service udhcpd start
sudo hostapd /etc/hostapd/hostapd.conf (This will keep running so do it in another tab or bg)
sudo ifconfig wlan0 192.168.0.251
```

Then run: `python3 testServer.py`

## Running tests
Simply run the command: `python3 tests_basic.py -v`


## Inspecting Packets in Wireshark
* Useful filter: `tcp.port == 8080 && tcp.flags.push == 1`
