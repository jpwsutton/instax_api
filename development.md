# Development Guide


## Developing using Poetry

* Install poetry on your development machine: https://python-poetry.org/docs/
* Run `poetry shell` to launch the virtual environment.
* Run `poetry install` to download all main and dev dependencies.
* Run `pre-commit install` and then `pre-commit install --hook-type commit-msg` to set up the pre-commit checks.
* When you are finished, just use `exit` to end your session.

## Running the Test Server

The Test server was written to allow developers to simulate an Instax SP-2 printer in order to test the client.

In order to connect the application, the device running the test server will need to be hosting a WiFi network with an SSID starting with `INSTAX-` followed by a number of hex characters (This would usually be the MAC address of the printer). In my case, I used a Raspberry Pi Model 3 to host the wireless network and run the Test Server on.
Once you have set up the pi following these instructions: Tutorial link goes here..., you will need to usually run these three commands :

```
sudo service udhcpd start
sudo hostapd /etc/hostapd/hostapd.conf (This will keep running so do it in another tab or bg)
sudo ifconfig wlan0 192.168.0.251
```

Then run: `python3 -m instax.debugServer`

## Hidden options in instax-print CLI client
In order to make debugging and using the test server easier, there are some hidden options in the instax-print application that you can use, these include:

```
  -d, --debug           Logs extra debug data to log.
  -l, --log             Log information to log file ddmmyy-hhmmss.log
  -o HOST, --host HOST  The Host IP to connect to the server on.
  -p PORT, --port PORT  The port to connect to the server on.
  -t TIMEOUT, --timeout TIMEOUT
                        The timeout to use when communicating.
```

For example, when using the test server, you can use the following command to print: `python3 -m instax.print myImage.jpg -o localhost -l`

The `-d / --debug` option will print a lot more data to the log file, specifically detailed dumps of every command / response sent or received by the client. This is handy when trying to identify issues in the packet library.

## Running tests
Simply run the command: `python3 -m pytest instax`


## Inspecting Packets in Wireshark
* Useful filter: `tcp.port == 8080 && tcp.flags.push == 1`
