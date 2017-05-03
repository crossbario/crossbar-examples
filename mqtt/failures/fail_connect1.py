#
# failing connect because clean_session==False
#

import paho.mqtt.client as paho


client = paho.Client(client_id="someone", clean_session=False)

def on_connect(client, userdata, flags, rc):
    print('on_connect(client={}, userdata={}, flags={}, rc={})'.format(client, userdata, flags, rc))
    client.disconnect()

def on_disconnect(client, userdata, rc):
    print('on_disconnect(client={}, userdata={}, rc={})'.format(client, userdata, rc))
    client.disconnect()

client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect('localhost', port=8080)

client.loop_forever()
