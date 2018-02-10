# A hub controller for smart-and-agile poles

import paho.mqtt.client as mqtt
from random import randrange
from time import sleep
import threading

import secret_config

# CONFIGURE FOR YOUR MQTT SERVER
ADDRESS = secret_config.ADDRESS
PORT = secret_config.PORT

# Configure for your setup
MIN_POLES = 1
MAX_POLES = 4
DELAY_SECS = 3

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")
    client.subscribe('button')
    client.subscribe('in')
    client.subscribe('out')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def button_pressed(client, userdata, msg):
    global cur_pole, poles
    if cur_pole != -2:
        if poles[cur_pole] == str(msg.payload):
            print('Correct button pressed!')
            cur_pole = -2
        else:
            print('Wrong button m8')

def pole_connected(client, userdata, msg):
    le_nom = str(msg.payload)
    if le_nom not in poles:
        print(le_nom+' connected!')
        poles.append(le_nom)
    else:
        print('Imposter %s on the loose' % le_nom)

def pole_disconnected(client, userdata, msg):
    global cur_pole, poles
    le_nom = str(msg.payload)
    try:
        i = poles.index(le_nom)
        if cur_pole == i:
            # The pole that was active is gone, we'll have
            # to get a new one
            cur_pole = -2
        poles.remove(le_nom)
        print('%s left :(' % le_nom)
    except ValueError:
        print('How can he be gone if he never existed? We won\'t miss you, %s' % le_nom)

def timeout_set():
    global timeout
    timeout = True

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.message_callback_add('button', button_pressed)
client.message_callback_add('in', pole_connected)
client.message_callback_add('out', pole_disconnected)

client.connect(ADDRESS, PORT, 60)
client.loop_start()
print('Running!')
poles = []
timeout = False
cur_pole = -2 # Used to represent invalid selection
# Main loop
while True:
    # Hang out until it's go time
    while len(poles) < MIN_POLES:
        pass
    
    # Go time
    cur_pole = randrange(len(poles))
    client.publish(poles[cur_pole], payload='go')
    print('Time for %s to go!' % poles[cur_pole])
    
    # Hang out until either the button is pressed or the pole disconnected
    while cur_pole != -2:
        pass
    
    # Give some time to get back to centre, and then start again
    timeout = False
    timer = threading.Timer(DELAY_SECS, timeout_set)
    timer.start()
    # Hang out until non-blocking delay finishes
    while not timeout:
        pass

# Something went wrong - time to bail
client.loop_stop(force=False)
