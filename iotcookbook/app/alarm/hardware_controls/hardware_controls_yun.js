
//
// Copyright (C) Tavendo GmbH. Licensed under the MIT license.
//
// This program bridges Arduino Yun to WAMP / Crossbar.io over Firmata (https://github.com/firmata/protocol).
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

console.log("Alarm App - Arduino Yun Hardware Controls starting ...");

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

        /****************************************
        *   Alarm App Hardware Control Code     *
        ****************************************/

        // alarm LED
        set_mode([10, "out"]);
        // armed LED
        set_mode([11, "out"]);

        var armed = false;
        var active = false;

        var setArmed = function (isArmed) {
            digital_write([11, isArmed]);
            armed = isArmed;
        };

        var setActive = function (isActive) {
            digital_write([10, isActive]);
            active = isActive;
        };

        // get initial states
        session.call("io.crossbar.examples.iotcookbook.alarmapp.get_alarm_armed").then(
            function(res) {
                setArmed(res);         
            },
            function(err) {
                console.log("get_alarm_armed error", err);
            }
        );

        session.call("io.crossbar.examples.iotcookbook.alarmapp.get_alarm_active").then(
            function(res) {
                setActive(res);        
            },
            function(err) {
                console.log("get_alarm_active error", err);
            }
        );

        // subscribe to state updates
        session.subscribe("io.crossbar.examples.iotcookbook.alarmapp.on_alarm_armed", function(args) {
            setArmed(args[0]);           
        });

        session.subscribe("io.crossbar.examples.iotcookbook.alarmapp.on_alarm_active", function(args) {
            setActive(args[0]);           
        });   

               
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

        var buttons = [
            {
                id: "armButton",
                pin: 0,
                mode: "in",
                action: function () {
                    session.call("io.crossbar.examples.iotcookbook.alarmapp.set_alarm_armed", [!armed]);
                },
                pressed: false,
                debounce: false
            },
            {
                id: "alarmButton",
                pin: 1,
                mode: "in",
                action: function () {
                    session.call("io.crossbar.examples.iotcookbook.alarmapp.set_alarm_active", [!active]); 
                },
                pressed: false,
                debounce: false
            },
        ];

        buttons.forEach(function(button) {
            console.log("button",  button.id, button.pin, button.mode);
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
