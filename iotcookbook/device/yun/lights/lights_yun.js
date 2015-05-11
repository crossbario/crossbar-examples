
//
// Copyright (C) Tavendo GmbH. Licensed under the MIT license.
//
// This program bridges Arduino Yun to WAMP / Crossbar.io over Firmata (https://github.com/firmata/protocol).
// and allows remote control of up to six Tinkerkit LED modules 
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

console.log("Arduino Yun Lights starting ...");

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

        function digital_write (args) {
            var pin = args[0];
            var value = args[1] == true;
            var sync = args[2];

            if (debug) {
                console.log("digital_write", pin, value, sync);
            }

            try {
                if (sync) {
                    var d = new autobahn.when.defer();
                    arduino.digitalWrite(pin, value, function () { d.resolve(null); });
                    return d.promise;
                } else {
                    arduino.digitalWrite(pin, value);
                }
            } catch (e) {
                console.log(e);
                throw e;
            }
        }


        /*********************************
        *           Lights Code         *
        *********************************/

        set_mode([11, "out"]); // Tinkerkit shield: 'O0'
        set_mode([10, "out"]); // Tinkerkit shield: 'O1'
        set_mode([9, "out"]); // Tinkerkit shield: 'O2'
        set_mode([6, "out"]); // Tinkerkit shield: 'O3'
        set_mode([5, "out"]); // Tinkerkit shield: 'O4'
        set_mode([3, "out"]); // Tinkerkit shield: 'O5'

        var pinMap = {
            O0: 11,
            O1: 10,
            O2: 9,
            O3: 6,
            O4: 5,
            O5: 3
        }

        var pinState = {
            O0: false,
            O1: false,
            O2: false,
            O3: false,
            O4: false,
            O5: false
        }

        var setLightState = function (args) {
            console.log("setLightState called", args);
            var light = args[0];
            // var state = args[1];

            pinState[light] = !pinState[light];
            digital_write([pinMap[light], pinState[light]]);

            return true;
        };

        session.register("io.crossbar.examples.yun.lights.set_light_state", setLightState).then(
            function() {
                console.log("procedure 'io.crossbar.examples.yun.lights.set_light_state' registered");
            },
            session.log
        );


    };

    connection.onclose = function (reason, details) {
        console.log("no connection", reason, details);
    }

    console.log("Connecting to router ...");

    connection.open();
});

// connect to Arduino over serial speaking Firmata
arduino.connect(device_port);
