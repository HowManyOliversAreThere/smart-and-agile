# smart-and-agile

A smart system for agile people.

This design consists of two different module types: hubs and poles.

* Poles are the individual units that light up and have their buttons pressed.
* Hubs are the controllers that tell poles when to light up, and organise synchronisation and algorithm management.

The pole and hub systems can be found in their respective folders in the repository.

## MQTT Server

The smart-and-agile system is designed around MQTT communication between the poles and their respective hub.
As such, an MQTT Server is necessary to facilitate this communication.

This code has been tested with [Mosquitto](https://mosquitto.org/), which is widely recognised as an
easy and straight forward way to implement an MQTT Server.

You will need to configure both the poles and hubs with the MQTT server details in order for them to connect.
