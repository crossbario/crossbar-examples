
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


        // pin 11 = Tinkerkit shield: 'O0'
        // pin 10 = Tinkerkit shield: 'O1'
        // pin 9 = Tinkerkit shield: 'O2'
        // pin 6 = Tinkerkit shield: 'O3'
        // pin 5 = Tinkerkit shield: 'O4'
        // pin 3 = Tinkerkit shield: 'O5'

        // comment out light pins as needed
        var lights = {
            11: false,
            10: false,
            9: false,
            6: false,
            5: false,
            3: false
        };

        // set the correct mode for the light pins
        for (pin in lights) {
            if (lights.hasOwnProperty(pin)) {
                set_mode([pin, "out"]);
            }
        };

        var toggleLight = function (args) {
            var pin = args[0];
            console.log("toggleLights called", pin);
            lights[pin] = !lights[pin];
            digital_write([pin, lights[pin]]);

            return true;
        };
        
        session.register("io.crossbar.examples.yun.lights.toggle_light", toggleLight).then(
            function() {
                console.log("procedure 'io.crossbar.examples.yun.lights.toggle_light' registered");
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
