
sudo apt-get install -y xboxdrv


sudo xboxdrv --quiet

X1:   622 Y1:  3588  X2:   127 Y2:  3772  du:0 dd:0 dl:0 dr:0  back:1 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0



sudo xboxdrv --quiet | python xbox2wamp.py --router ws://...

Reads Xbox events from stdin, parses and publishes WAMP events

