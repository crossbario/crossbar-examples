//
// Copyright (C) Tavendo GmbH. Licensed under the MIT license.
//
// This program bridges Arduino Yun to WAMP / Crossbar.io over Firmata (https://github.com/firmata/protocol).
// and sends the state of a Tinkerit Potentiometer module as a PubSub event
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


console.log("Arduino Yun Potentiometer starting ...");

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

        /*****************************
        *     Potentiometer Code     *
        *****************************/



        // 'I0': 0, 'I1': 1, 'I2': 2, 'I3': 3, 'I4': 4, 'I5': 5,
        var pot_min = 13; // minimum value the potentiometer produces
        var pot_max = 868; // max value the potentiomenter produces
        var pot_smoothe = 1; // offset below which no value changes are sent

        // add entries as needed: key is the pin the potentiometer is connected to
        //  'source' = key
        var potentiometers = {
            0: {
                type: "publish",
                url: "io.crossbar.examples.yun.potentiometer.on_value_change",
                source: 0,
                lastValue: null
            },
            // 1: {
            //     type: "publish",
            //     url: "io.crossbar.examples.yun.potentiometer.on_value_change",
            //     source: 1,
            //     lastValue: null
            // }
        };

        // initialize the potentiometers for watching
        for (pin in potentiometers) {
            if (potentiometers.hasOwnProperty(pin)) {
                set_mode([pin, "watch"]);
            }
        }

        var normalizeValue = function (rawValue) {
            return parseInt(((rawValue - pot_min) / (pot_max - pot_min)) * 100);
        };

        var get_potentiometer_value = function (pin) {

            set_mode([pin, "in"]);

            var normValue = normalizeValue(analog_read([pin]));
            
            set_mode([pin, "watch"]);

            potentiometers[pin].lastValue = normValue;
            
            return normValue;
        };

        session.register("io.crossbar.examples.yun.potentiometer.get_potentiometer_value", get_potentiometer_value).then(function() {
            console.log("io.crossbar.examples.yun.potentiometer.get_potentiometer_value registered");
        }, 
        function () {
            console.log("io.crossbar.examples.yun.potentiometer.get_potentiometer_value - registration error");
        });
        
        arduino.on('analogChange', function (e) {
            if (e.pin in potentiometers) {

                normValue = normalizeValue(e.value);
                var lastValue = potentiometers[e.pin].lastValue;

                if (debug) {
                    console.log("light level changed", e.pin, normValue);
                }

                // constant value wanted, differs from previous value by more than smoothe value
                if (normValue > lastValue + pot_smoothe || normValue < lastValue - pot_smoothe) {
                    potentiometers[e.pin].lastValue = normValue; // can't use 'lastValue' since this is not a reference
                    session.publish("io.crossbar.examples.yun.potentiometer.on_value_change", [e.pin, normValue]);    
                }              
            }
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
