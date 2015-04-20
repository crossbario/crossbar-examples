# Connecting Xbox gamepads to Crossbar.io on the Pi

Reads Xbox events from stdin, parses and publishes WAMP events.

Install [xboxdrv](https://github.com/xboxdrv/xboxdrv) (a userspace drive for Xbox gamepad controllers):

```console
sudo apt-get install -y xboxdrv
```

Test the driver:

```console
pi@raspberrypi ~/scm/crossbarexamples/device/pi/xboxcontroller $ sudo xboxdrv --quiet --detach-kernel-driver
X1:  1126 Y1:  4564  X2:  1933 Y2:  3268  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
X1:  1126 Y1:  4564  X2:  1933 Y2:  3646  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
X1:  1126 Y1:  4564  X2:  1933 Y2:  4024  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
X1:  1126 Y1:  4564  X2:  1933 Y2:  4402  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
X1:  1126 Y1:  4564  X2:  1546 Y2:  4780  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
X1:  1126 Y1:  4564  X2:  1546 Y2:  5158  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
X1:  1126 Y1:  4564  X2:  1159 Y2:  5914  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
X1:  1126 Y1:  4564  X2:   772 Y2:  5914  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
X1:  1126 Y1:  4564  X2:   772 Y2:  6292  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
X1:  1126 Y1:  4564  X2:   256 Y2:  6292  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
X1:  1126 Y1:  4564  X2:   256 Y2:  6796  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
X1:  1126 Y1:  4564  X2:  -131 Y2:  6796  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
X1:  1126 Y1:  4564  X2:  -131 Y2:  6292  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
X1:  1126 Y1:  4564  X2:  -131 Y2:  5788  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
...
```

Run the Xbox2WAMP bridge:

```console
pi@raspberrypi ~/scm/crossbarexamples/device/pi/xboxcontroller $ make
sudo xboxdrv --quiet --detach-kernel-driver | python xbox2wamp.py --router ws://192.168.1.141:8080/ws
2015-04-20 14:30:00+0000 [-] Log opened.
2015-04-20 14:30:00+0000 [-] Xbox2Wamp bridge starting with ID 6afe83b4 ...
2015-04-20 14:30:05+0000 [-] Running on reactor <twisted.internet.epollreactor.EPollReactor object at 0x3090a30>
2015-04-20 14:30:05+0000 [-] Xboxdrv connected
2015-04-20 14:30:05+0000 [-] Starting factory <autobahn.twisted.websocket.WampWebSocketClientFactory object at 0x30a5370>
2015-04-20 14:30:05+0000 [WampWebSocketClientProtocol,client] Session ready: SessionDetails(realm = realm1, session = 547248756, authid = RnTLg9QMVzcqSsuHalGVE4af, authrole = anonymous, authmethod = anonymous)
2015-04-20 14:30:12+0000 [-] XboxdrvProtocol event published to io.crossbar.xbox.6afe83b4.ondata: {'A': 0, 'dl': 0, 'X1': 622, 'Y': 0, 'start': 0, 'dd': 0, 'LB': 0, 'TR': 0, 'back': 0, 'LT': 0, 'X2': -518, 'TL': 0, 'B': 0, 'RB': 0, 'Y1': 4564, 'X': 0, 'du': 0, 'dr': 0, 'guide': 0, 'Y2': 5788}
2015-04-20 14:30:12+0000 [-] XboxdrvProtocol event published to io.crossbar.xbox.6afe83b4.ondata: {'X1': 118}
2015-04-20 14:30:12+0000 [-] XboxdrvProtocol event published to io.crossbar.xbox.6afe83b4.ondata: {'X1': -260}
2015-04-20 14:30:12+0000 [-] XboxdrvProtocol event published to io.crossbar.xbox.6afe83b4.ondata: {'X1': -638}
2015-04-20 14:30:12+0000 [-] XboxdrvProtocol event published to io.crossbar.xbox.6afe83b4.ondata: {'Y1': 5052}
2015-04-20 14:30:12+0000 [-] XboxdrvProtocol event published to io.crossbar.xbox.6afe83b4.ondata: {'Y1': 5418, 'X1': -1016}
2015-04-20 14:30:12+0000 [-] XboxdrvProtocol event published to io.crossbar.xbox.6afe83b4.ondata: {'Y1': 5784, 'X1': -1520}
2015-04-20 14:30:12+0000 [-] XboxdrvProtocol event published to io.crossbar.xbox.6afe83b4.ondata: {'Y1': 6150}
2015-04-20 14:30:12+0000 [-] XboxdrvProtocol event published to io.crossbar.xbox.6afe83b4.ondata: {'Y1': 5662}
2015-04-20 14:30:12+0000 [-] XboxdrvProtocol event published to io.crossbar.xbox.6afe83b4.ondata: {'Y1': 5174}
2015-04-20 14:30:12+0000 [-] XboxdrvProtocol event published to io.crossbar.xbox.6afe83b4.ondata: {'Y1': 4686}
2015-04-20 14:30:13+0000 [-] XboxdrvProtocol event published to io.crossbar.xbox.6afe83b4.ondata: {'Y1': 4198}
...
```
