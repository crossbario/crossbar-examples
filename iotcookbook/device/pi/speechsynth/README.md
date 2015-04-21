# A remote controlled robot voice for the Pi

## Description

How about a robot voice, text-to-speech engine that can be remotely controlled from any other WAMP component. Wnat your alarm system talk to the intruder? Sure.

The example uses the [flite](http://www.festvox.org/flite/) text-to-speech engine to convert english sentances to voice which is then output via the Pi's audio output.

The code for the example consists of a adapter written in Python and AutobahnPython using Twisted. The adapter runs on the Pi and connects to Crossbar.io running on a network accessible from the Pi.

The adapter exposes these procedures

* `io.crossbar.examples.iot.devices.pi.<DEVICE ID>.speechsynth.say`
* `io.crossbar.examples.iot.devices.pi.<DEVICE ID>.speechsynth.is_busy`

and publishes event on these topics

* `io.crossbar.examples.iot.devices.pi.<DEVICE ID>.speechsynth.on_ready`
* `io.crossbar.examples.iot.devices.pi.<DEVICE ID>.speechsynth.on_speech_start`
* `io.crossbar.examples.iot.devices.pi.<DEVICE ID>.speechsynth.on_speech_end`

Included with a frontend running in browsers. The frontend is written in JavaScript using AutobahnJS and connects to the same Crossbar.io router instance as the adapter connects to. Consequently, the frontend is able to invoke the procedures exposed on the Pi and subscribe to events generated from there.


## How to run

[Enable audio](https://www.raspberrypi.org/documentation/configuration/audio-config.md) output on the 3.5mm plug:

```console
sudo amixer cset numid=3 1
```

Install the [flite](http://www.festvox.org/flite/) text-to-speech processor:

```console
sudo apt-get install -y flite
```

Test the text-to-speech engine:

```console
flite -voice slt -t "Hi, my name is Susan. How can I help you?"
```

