# instax_api
An Api for the Fujifilm Instax SP-2 printer written in Python

This is an experimental Python Module to interact and print photos to the Fujifilm Instax SP-2 printer.

Currently there is nothing here yet as I'm still reverse engineering the protocol, so watch this space.

Protocol Information: Check the [Wiki](https://github.com/jpwsutton/instax_api/wiki) for more information about the Instax Protocol.




## Using the Virtualenv environment

* Make sure you have virtualenv installed : `pip install virtualenv`.
* If you haven't created it yet, create the virtual environment: `virtualenv env -p python3`.
* Activate the environment: `source env/bin/activate`.
* Install packages from requirements.txt: `pip install -r requirements.txt --upgrade`.
* When you are finished, just use `deactivate` to end your session.


## Inspecting Packets in Wireshark
* Useful filter: `tcp.port == 8080 && tcp.flags.push == 1`
