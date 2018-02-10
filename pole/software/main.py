# smart-and-agile pole hardware control

import machine
from machine import Pin
import network
import time
import ubinascii
from umqtt.simple import MQTTClient

import sixnibblename
import secret_config

# CONFIGURE FOR YOUR MQTT SERVER
CLIENT_ID = sixnibblename.get(int.from_bytes(machine.unique_id(), 'little')).encode('ascii')
ADDRESS = secret_config.ADDRESS
PORT = secret_config.PORT
PRESS_TOPIC = b'button'
IN_TOPIC = b'in'
OUT_TOPIC = b'out'

# Connect to the network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect(secret_config.ESSID, secret_config.PASSWORD)
    while not wlan.isconnected():
        pass
    print('Network connected! Config: ', wlan.ifconfig())

# Configure hardware
button = Pin(0, Pin.IN, Pin.PULL_UP) # D0
led = Pin(4, Pin.OUT, value=0) # D3

# Define callback to subscribed channel
def sub_cb(topic, msg):
    print('Message received! Topic: %s, Msg: %s' % (topic, msg))
    if msg == b'go':
        led.on()

# Init MQTT client
c = MQTTClient(CLIENT_ID, ADDRESS, port=PORT)
c.set_callback(sub_cb)
c.set_last_will(OUT_TOPIC, CLIENT_ID)
c.connect()
c.subscribe(CLIENT_ID)
print("Connected to %s:%i, subscribed to %s" % (ADDRESS, PORT, CLIENT_ID))
c.publish(IN_TOPIC, CLIENT_ID)

# Main loop
while True:
    while True:
        c.check_msg()
        if button.value() == 0:
            break
        time.sleep_ms(20)
    print("Button pressed")
    led.off()
    c.publish(PRESS_TOPIC, CLIENT_ID)
    time.sleep_ms(200)

# Something went wrong - bail
c.disconnect()
