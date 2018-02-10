# Pole software

The pole software is designed to be run on an ESP based board running [Micropython](https://micropython.org/), such as the
[Wemos D1 Mini](https://wiki.wemos.cc/products:d1:d1_mini).

## Requirements

* [six-nibble-name](https://github.com/HowManyOliversAreThere/six-nibble-name) - get the latest version from the repo
* An ESP based board running Micropython
* A way of loading files onto your board, such as [mpfshell](https://github.com/wendlers/mpfshell)

## Usage

1. Modify `secret_config.py` to have your Wireless and MQTT Server details
2. Load `main.py`, `secret_config.py`, and `sixnibblename.py` onto the target device
3. Ensure the Hub is already running, and then reset the device
4. You should see `NAME connected!` on the hub - if so, it's working!

## Known Issues

* The device does not publish its last will when unplugged, leaving the hub still thinking it's connected
