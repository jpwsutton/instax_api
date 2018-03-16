# Development Guide


## Developing using the Virtualenv environment

* Make sure you have virtualenv installed : `pip3 install virtualenv`.
* If you haven't created it yet, create the virtual environment: `virtualenv env -p python3`.
* Activate the environment: `source env/bin/activate`.
* Install packages from requirements.txt: `pip3 install -r requirements.txt --upgrade`.
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
