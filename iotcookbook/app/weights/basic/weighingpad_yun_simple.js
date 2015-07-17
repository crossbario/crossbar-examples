
//
// Copyright (C) Tavendo GmbH. Licensed under the MIT license.
//
// This program bridges Arduino Yun to WAMP / Crossbar.io over Firmata (https://github.com/firmata/protocol).
// and sends accelerometer data from a Tinkerkit accelerometer module 
//
// Firmata is a MIDI-based protocol for communication between MCUs and host CPUs over serial connections.
//
// Firmata implementations used in the bridge:
//
//   - Linux-side: https://github.com/shokai/node-arduino-firmata
//   - Arduino-side: https://github.com/firmata/arduino/blob/master/examples/StandardFirmataYun/StandardFirmataYun.ino
//

// configuration:
var router = 'ws://192.168.1.136:8080/ws';
var realm = 'iot_cookbook';
var device_id = '123456';
var device_port = '/dev/ttyATH0';
//var debug = true;
var debug = false;

console.log("Arduino Yun Weighing Pads starting ...");

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
        *   Weighing Pad Control Code   *
        *********************************/

        var config = { 
            id: "yun1", // sent as part of data publish
            pins: [1, 2], // the pins which pads are connected to
            frequency: 20, // the sampling frequency
            publishOnDifference: true, // publish on value change or on each sampling
            difference: 100 // difference between values which triggers publishing
        };
        var lastValues = {};

        // configure pins mode & set up lastValue tracking
        config.pins.forEach(function(pin) {
            console.log("setting mode for pin " + pin);
            set_mode([pin, "in"]);
            if (!lastValues[pin]) {
                lastValues[pin] = 0;
            };
        });


        var get_pad_values = function() {

            var publish = false;
            var dataToPublish = { 
                id: config.id,
                samples: {}
            };
            
            config.pins.forEach(function(pin) {
                
                var value = analog_read([pin]);

                if (config.publishOnDifference === true) {
                    
                    // check whether current value exceeds last value +/- threshold difference
                    if ((value > lastValues[pin] + config.difference) || (value < lastValues[pin] - config.difference) ) {

                        publish = true;
                        dataToPublish.samples[pin] = value;

                        // update only here ensures that slow weight increases (each step below the difference threshold) are caught
                        // if you only want to catch impulses, then move this below the brackets!
                        lastValues[pin] = value; 

                    }; 

                } else {
                    
                    publish = true;
                    dataToPublish.samples[pin] = value;

                }
            });


            if (publish) {
                console.log("publishing: ", dataToPublish);
                session.publish("io.crossbar.examples.yun.weighingpad.on_sample", [dataToPublish]);    
            }            

            setTimeout(get_pad_values, config.frequency);
        };
        get_pad_values();

        
    };

    connection.onclose = function (reason, details) {
        console.log("no connection", reason, details);
    }

    console.log("Connecting to router ...");

    connection.open();
});

// connect to Arduino over serial speaking Firmata
arduino.connect(device_port);
