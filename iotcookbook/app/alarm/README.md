# Alarmapp for Tessel

Alarm triggered via accelerometer (Tessel 1) causes a photo to be taken (Tessel 2). Alarm + photo are displayed in a HTML5 client, which also allows arming, disarming and canceling the alarm.

Put together during the Microsoft IoT Hackaton in Berlin; 13.11.2014.

[Video](http://www.youtube.com/watch?v=WY7KzrRm8XY) of this in action (with some Crossbar.io/WAMP background) (2 minutes 50 seconds).

Note: 
   * Taking the picture on the Tessel takes about 2.4s at a very low resolution.
   * Encoding this for sending over WAMP is another ~1.3s.
   * The Tessel's wi-fi is also slow.
   * So don't expect a snappy response with the image. (Any hints about optimization are highly welcome!)

## Hardware requirements

Two Tessels, one with an accelerometer module, one with a camera module.

## Running the demo

The demo backend runs on Node.js, and the Tessel uses the node package manager `npm` - so you need to have both installed.

To install the required Node packages, you initially need to do

```
npm install 
```

in the demo directory.

Then start Crossbar.io from the demo directory by doing 

```
crossbar start
``` 

Crossbar also serves the HTML5 frontend under `http://localhost:8080`.


For the two Tessel scripts, you need to replace the IP in `url: "ws://192.168.1.134:8080/ws"` with the IP under which the Tessels can reach the computer running Crossbar.io.


Connect the **Tessel with the accelerometer** and  do

```
tessel push tessel/accelerometer.js
```

the disconnect and restart.

For the **Tessel with the camera** do

```
tessel push tessel/camera.js
```



## Note on Crossbar.io configuration

Since the Tessel WS/WAMP libraries do not send the proper WebSocket subprotocol parameters, in the Crossbar configuration ignoring this needs to be set:

```
"type": "websocket",
"options": {
   "require_websocket_subprotocol": false   
} 
```

Since the Tessel has problems with WebSocket pings, do not set `auto_ping_interval` to anything but the default `0`.

## Note on hacking the Tessel code

As a consequence of not having the pings, Crossbar.io will most likely not detect the loss of connection when redeploying code on the Tessel. It is easiest to handle this by restarting Crossbar.io before each code redeployment.

## Note on progressive results

When called from the frontend, the remote procedure for taking pictures on the Tessel provides progressive results. This is an easy method to allow feedback about long-running operations.