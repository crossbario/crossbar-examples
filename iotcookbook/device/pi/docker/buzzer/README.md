# Crossbar.io IoT Starterkit - Buzzer

This component exposes the piezo buzzer built into the Crossbar.io IoT Starterkit in a WAMP component.

The component registers a single procedure to trigger a beeping sound sequence:

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.beep(count=1, on=30, off=80)`

Here, `serial` is the serial number of the Pi inside the starterkit, eg `1106555643`. The parameters are:

* `count`: Number of beeps.
* `on`: ON duration in ms.
* `off`: OFF duration in ms.
