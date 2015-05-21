//
// Copyright (C) Tavendo GmbH. Licensed under the MIT license.
//
// This program bridges Arduino Yun to WAMP / Crossbar.io over Firmata (https://github.com/firmata/protocol).
// and sends the state of a Tinkerit LDR module as a PubSub event
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
var debug = false;
// var debug = true;


console.log("Arduino Yun Ambientlight Sensor starting ...");

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

        /******************************************
        *     Ambient Light (LDR) Sensor Code     *
        ******************************************/

        var ldr_pin = 0; // change to suit your requirements: 'I0': 0, 'I1': 1, 'I2': 2, 'I3': 3, 'I4': 4, 'I5': 5,
        var threshold = 0; // threshold value for sending events, '0' = send any changes
        var ldr_min = 9; // minimum value the sensor produces at full dark
        var ldr_max = 880; // max value the sensor produces
        var ldr_last = 0;
        var ldr_smoothe = 1; // offset below which no value changes are sent

        set_mode([ldr_pin, "watch"]);

        var get_light_level = function () {

            set_mode([ldr_pin, "in"]);

            var normValue = normalizeValue(analog_read([ldr_pin]));
            
            set_mode([ldr_pin, "watch"]);

            ldr_last = normValue;
            
            return normValue;
        };

        var normalizeValue = function (rawValue) {
            return parseInt(((rawValue - ldr_min) / (ldr_max - ldr_min)) * 100);
        };

        arduino.on('analogChange', function (e) {
            if (ldr_pin === e.pin) {

                normValue = normalizeValue(e.value);

                if (debug) {
                    console.log("light level changed", e.value, normValue, ldr_last);
                }

                // constant value wanted, differs from previous value by more than smoothe value
                if (threshold === 0 && (normValue > ldr_last + ldr_smoothe || normValue < ldr_last - ldr_smoothe)) {
                    ldr_last = normValue;
                    session.publish("io.crossbar.examples.yun.ambientlight.on_light_level_change", [normValue]);    
                // is at other side of threshold value (with smoothe area around that value)
                } else if (normValue > threshold + ldr_smoothe && ldr_last < threshold - ldr_smoothe) {
                    ldr_last = normValue;
                    session.publish("io.crossbar.examples.yun.ambientlight.on_threshold_passed", [true]);
                } else if (normValue < threshold - ldr_smoothe && ldr_last > threshold + ldr_smoothe) {
                    ldr_last = normValue;
                    session.publish("io.crossbar.examples.yun.ambientlight.on_threshold_passed", [false]);
                }               
            }
        });

        session.register("io.crossbar.examples.yun.ambientlight.get_light_level", get_light_level).then(function() {
            console.log("io.crossbar.examples.yun.ambientlight.get_light_level registered");
        }, 
        function () {
            console.log("io.crossbar.examples.yun.ambientlight.get_light_level - registration error");
        });


        session.register("io.crossbar.examples.yun.ambientlight.set_threshold", function(args) {
            threshold = args[0];
        }).then(function() {
            console.log("io.crossbar.examples.yun.ambientlight.set_threshold registered");
        }, 
        function () {
            console.log("io.crossbar.examples.yun.ambientlight.set_threshold - registration error");
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
