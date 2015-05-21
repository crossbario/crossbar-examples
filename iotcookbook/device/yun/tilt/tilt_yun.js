//
// Copyright (C) Tavendo GmbH. Licensed under the MIT license.
//
// This program bridges Arduino Yun to WAMP / Crossbar.io over Firmata (https://github.com/firmata/protocol).
// and sends the state of a Tinkerit tilt module as a PubSub event
//
// Firmata is a MIDI-based protocol for communication between MCUs and host CPUs over serial connections.
//
// Firmata implementations used in the bridge:
//
//   - Linux-side: https://github.com/shokai/node-arduino-firmata
//   - Arduino-side: https://github.com/firmata/arduino/blob/master/examples/StandardFirmataYun/StandardFirmataYun.ino
//

// configuration:
var router = 'ws://192.168.1.134:8080/ws';
var realm = 'iot_cookbook';
var device_id = '123456';
var device_port = '/dev/ttyATH0';
//var debug = true;
var debug = false;

console.log("Arduino Yun Tilt Sensor starting ...");

var autobahn = require('autobahn');
var firmata = require('arduino-firmata');

var arduino = new firmata();

arduino.on('connect', function () {

    console.log("Arduino connected (over " + arduino.serialport_name + ", board version " + arduino.boardVersion + ")");

    var connection = new autobahn.Connection({url: router, realm: realm});

    connection.onopen = function (session) {

        console.log("Router connected. Session ID:", session.id);

        var monitored_pins = {};

        function set_mode (args) {
            var pin = args[0];
            var mode = args[1];

            if (debug) {
                console.log("set_mode", pin, mode);
            }

            if (mode == "in") {

                arduino.pinMode(pin, firmata.INPUT);
                monitored_pins[pin] = false;

            } else if (mode == "watch") {

                arduino.pinMode(pin, firmata.INPUT);
                monitored_pins[pin] = true;

            } else if (mode == "out") {

                arduino.pinMode(pin, firmata.OUTPUT);
                monitored_pins[pin] = false;

            } else {
                console.log("illegal pin mode", mode);
                throw "illegal pin mode: " + mode;
            }
        }

        function analog_read (args) {
            var pin = args[0];

            if (debug) {
                console.log("analog_read", pin);
            }

            var value;
            try {
                value = arduino.analogRead(pin);
            } catch (e) {
                console.log(e);
                throw e;
            }

            return value;
        }

        /*********************************
        *           Tilt Sensor Code     *
        *********************************/

        var tilt_pin = 0; // change to suit your requirements: 'I0': 0, 'I1': 1, 'I2': 2, 'I3': 3, 'I4': 4, 'I5': 5,

        set_mode([tilt_pin, "watch"]);

        var get_is_tilted = function () {

            set_mode([tilt_pin, "in"]);

            var is_tilted = analog_read([tilt_pin]) < 300 ? true : false;
            
            set_mode([tilt_pin, "watch"]);
            
            return is_tilted;
        };

        var tilt_state = get_is_tilted();
        
        arduino.on('analogChange', function (e) {
            if (tilt_pin === e.pin) {
                if (debug) {
                    console.log("tilt changed", e);
                }

                var is_tilted = e.value < 300 ? true : false;

                if (tilt_state != is_tilted) {
                    session.publish("io.crossbar.examples.yun.tilt.on_tilt", [is_tilted]);
                    tilt_state = is_tilted;
                }
            }
        });

        session.register("io.crossbar.examples.yun.tilt.get_is_tilted", get_is_tilted).then(function() {
            console.log("io.crossbar.examples.yun.tilt.get_is_tilted registered");
        }, 
        function () {
            console.log("io.crossbar.examples.yun.tilt.get_is_tilted - registration error");
        });
    };

    connection.onclose = function (reason, details) {
        console.log("no connection", reason, details);
    }

    console.log("Connecting to router ...");

    connection.open();
});

// connect to Arduino over serial speaking Firmata
arduino.connect(device_port);
