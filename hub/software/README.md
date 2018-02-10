# Hub software

The hub software is what controls the poles, and tells them what to do.

## Requirements

* [Python 3.6](https://python.org)
* [paho-mqtt](https://pypi.python.org/pypi/paho-mqtt/1.3.1)

## Usage

1. Modify `secret_config.py` to have your MQTT Server details
2. Run `pole_control.py`

This can be run on the same server as the MQTT Server or a different one - it doesn't matter.

## Future Work

* It would be good to have the hub configurable by a device such as a smartphone
(either through MQTT or an app). This could include:
  * Starting or stopping the poles
  * Configuring delay time
