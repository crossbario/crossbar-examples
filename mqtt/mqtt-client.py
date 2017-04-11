#
# Example MQTT client using paho-mqtt
#

import os
import time
import struct

import paho.mqtt.client as paho

# binary payload format we use in this example (unsigned short + signed int, big endian)
FORMAT = '<Hl'

# topic we publish and subscribe to
TOPIC = u'mqtt/test/mytopic1'

pid = os.getpid()
print('MQTT client starting with PID {}..'.format(pid))

client = paho.Client()

# Called when a message has been received on a topic that the client subscribes to.
def on_connect(client, userdata, flags, rc):
    print('on_connect({}, {}, {}, {})'.format(client, userdata, flags, rc))

def on_message(client, userdata, msg):
    pid, seq = struct.unpack(FORMAT, msg.payload)
    print('event received on topic {}: pid={}, seq={}'.format(msg.topic, pid, seq))

client.on_connect = on_connect
client.on_message = on_message

# connect to the universal transport we configured in Crossbar.io
client.connect('localhost', port=8080)

# connect to the dedicated MQTT transport we configured in Crossbar.io
# client.connect('localhost', port=1883)

# subscribe to a topic, this will fire on_message() upon receiving events
client.subscribe(TOPIC, qos=0)

# start the network loop in a background thread
# see: https://pypi.python.org/pypi/paho-mqtt#network-loop
client.loop_start()

# publish once a second forever ..
seq = 1
while True:
    payload = struct.pack(FORMAT, pid, seq)
    client.publish(TOPIC, payload, qos=0, retain=False)
    seq += 1
    time.sleep(1)
