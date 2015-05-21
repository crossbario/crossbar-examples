
//
// Copyright (C) Tavendo GmbH. Licensed under the MIT license.
//
// This program bridges Arduino Yun to WAMP / Crossbar.io over Firmata (https://github.com/firmata/protocol).
// and sends button presses from up to six Tinkerkit button modules 
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

console.log("Arduino Yun Buttons starting ...");

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
        *           Buttons Code         *
        *********************************/

        var get_button_value = function (button) {

            // button is currently pressed and we need to create an event
            if (analog_read([button.pin]) > 500 && !button.pressed && !button.debounce) {
                
                button.pressed = true;
                button.debounce = true;

                button.action();

                // timeout for de-bouncing
                setTimeout(function() {
                    button.debounce = false;
                }, 100)
            // button not pressed and we're outside of the debounce timeout
            } else if (analog_read([button.pin]) < 500 && button.debounce === false) {
                button.pressed = false;
            }

            setTimeout(function () {
                get_button_value(button);
            }, 5);
        };

        // When we listen to all pins and there are less buttons connected, then events for unconnected
        // buttons can be triggered.
        // E.g. with two buttons like this XX0000, when the second button (X) is pressed, 
        // events will be triggered for the four unconnected buttons (0000).
        // So please comment in the precise buttons you need below!
        var buttons = [
            {
                pin: 0,
                mode: "in",
                action: function () {
                    session.publish("io.crossbar.examples.yun.buttons.button_pressed", [0]);
                },
                pressed: false,
                debounce: false
            },
            // {
            //     pin: 1,
            //     mode: "in",
            //     action: function () {
            //         session.publish("io.crossbar.examples.yun.buttons.button_pressed", [1]);
            //     },
            //     pressed: false,
            //     debounce: false
            // },
            // {
            //     pin: 2,
            //     mode: "in",
            //     action: function () {
            //         session.publish("io.crossbar.examples.yun.buttons.button_pressed", [2]);
            //     },
            //     pressed: false,
            //     debounce: false
            // },
            // {
            //     pin: 3,
            //     mode: "in",
            //     action: function () {
            //         session.publish("io.crossbar.examples.yun.buttons.button_pressed", [3]);
            //     },
            //     pressed: false,
            //     debounce: false
            // },
            // {
            //     pin: 4,
            //     mode: "in",
            //     action: function () {
            //         session.publish("io.crossbar.examples.yun.buttons.button_pressed", [4]);
            //     },
            //     pressed: false,
            //     debounce: false
            // },
            // {
            //     pin: 5,
            //     mode: "in",
            //     action: function () {
            //         session.publish("io.crossbar.examples.yun.buttons.button_pressed", [5]);
            //     },
            //     pressed: false,
            //     debounce: false
            // }
        ];

        buttons.forEach(function(button) {
            console.log("button",  button.pin, button.mode);
            set_mode([button.pin, button.mode]);
            get_button_value(button);
        })


    };

    connection.onclose = function (reason, details) {
        console.log("no connection", reason, details);
    }

    console.log("Connecting to router ...");

    connection.open();
});

// connect to Arduino over serial speaking Firmata
arduino.connect(device_port);
