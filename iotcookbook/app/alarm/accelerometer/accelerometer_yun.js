
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

function make_uri (id) {
    return 'io.crossbar.examples.iot.devices.arduino.' + device_id + '.firmata.' + id;
}

console.log("Arduino/Firmata-to-WAMP bridge starting ...");

var autobahn = require('autobahn');
var firmata = require('arduino-firmata');

var arduino = new firmata();

arduino.on('connect', function () {

    console.log("Arduino connected (over " + arduino.serialport_name + ", board version " + arduino.boardVersion + ")");

    var connection = new autobahn.Connection({url: router, realm: realm});

    connection.onopen = function (session) {

        console.log("Router connected. Session ID:", session.id);

        var reg_requests = [];

        var monitored_pins = {};

        arduino.on('analogChange', function (e) {
            if (monitored_pins[e.pin]) {
                if (debug) {
                    console.log("analogChange", e);
                }
                session.publish(make_uri("on_analog_changed"), [e.pin, e.old_value, e.value]);
            }
        });
/*
        arduino.on('digitalChange', function (e) {
            if (monitored_pins[e.pin]) {
                if (debug) {
                    console.log("digitalChange", e);
                }
                session.publish(make_uri("on_digital_changed"), [e.pin, e.old_value, e.value]);
            }
        });
*/
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
        reg_requests.push(session.register(make_uri('set_mode'), set_mode));

        function digital_read (args) {
            var pin = args[0];

            if (debug) {
                console.log("digital_read", pin);
            }

            var value;
            try {
                value = arduino.digitalRead(pin);
            } catch (e) {
                console.log(e);
                throw e;
            }

            return value;
        }
        reg_requests.push(session.register(make_uri('digital_read'), digital_read));

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
        reg_requests.push(session.register(make_uri('digital_write'), digital_write));

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
        reg_requests.push(session.register(make_uri('analog_read'), analog_read));

        function analog_write (args) {
            var pin = args[0];
            var value = args[1];
            var sync = args[2];

            if (debug) {
                console.log("analog_write", pin, value, sync);
            }

            try {
                if (sync) {
                    var d = new autobahn.when.defer();
                    arduino.analogWrite(pin, value, function () { d.resolve(null); });
                    return d.promise;
                } else {
                    arduino.analogWrite(pin, value);
                }
            } catch (e) {
                console.log(e);
                throw e;
            }
        }
        reg_requests.push(session.register(make_uri('analog_write'), analog_write));

        function servo_write (args) {
            var pin = args[0];
            var value = args[1];
            var sync = args[2];

            if (debug) {
                console.log("servo_write", pin, value, sync);
            }

            try {
                if (sync) {
                    var d = new autobahn.when.defer();
                    arduino.servoWrite(pin, value, function () { d.resolve(null); });
                    return d.promise;
                } else {
                    arduino.servoWrite(pin, value);
                }
            } catch (e) {
                console.log(e);
                throw e;
            }
        }
        reg_requests.push(session.register(make_uri('servo_write'), servo_write));

        function reset(args) {
            var sync = args[0];

            if (debug) {
                console.log("reset", sync);
            }

            if (sync) {
                var d = new autobahn.when.defer();
                arduino.reset(function () {
                    d.resolve(null);
                });
                return d.promise;
            } else {
                arduino.reset();
            }
        }
        reg_requests.push(session.register(make_uri('reset'), reset));

        autobahn.when.all(reg_requests).then(
            function (regs) {
                console.log("All procedures (" + regs.length + " in total) registered.");
                for (var i = 0; i < regs.length; ++i) {
                    console.log("Procedure '" + regs[i].procedure + "'' has registration ID " + regs[i].id);
                }
            },
            function (err) {
                console.log("Could not register procedures", err);
            }
        );

        // alarm LED
        set_mode([11, "out"]);
        // armed LED
        set_mode([10, "out"]);

        var armed = false;

        // get initial states
        session.call("io.crossbar.examples.iotcookbook.alarmapp.get_alarm_armed").then(
            function(res) {
                if (res === true) {
                    digital_write([10, true]);
                    armed = true;                
                } else {
                    digital_write([10, false]);
                    armed = false;
                }         
            },
            function(err) {
                console.log("get_alarm_armed error", err);
            }
        );


        session.call("io.crossbar.examples.iotcookbook.alarmapp.get_alarm_active").then(
            function(res) {
                if (res === true) {
                    digital_write([11, true]);
                    active = true;                
                } else {
                    digital_write([11, false]);
                    active = false;
                }         
            },
            function(err) {
                console.log("get_alarm_active error", err);
            }
        );

        // subscribe to state updates
        session.subscribe("io.crossbar.examples.iotcookbook.alarmapp.on_alarm_active", function(args) {
            console.log("received on_alarm_active event", args[0]);
            if (args[0] === true) {
                // console.log("should turn on alarm LED");
                digital_write([11, true]);
                active = true;    
            } else {
                // console.log("should turn off alarm LED");
                digital_write([11, false]);
                active = false;
            }            
        });        

        session.subscribe("io.crossbar.examples.iotcookbook.alarmapp.on_alarm_armed", function(args) {
            console.log("received on_alarm_armed event", args[0]);
            if (args[0] === true) {
                // console.log("should turn on armed LED");
                digital_write([10, true]);
                armed = true;    
            } else {
                // console.log("should turn off armed LED");
                digital_write([10, false]);
                armed = false;
            }            
        });

        // arm/disarm button
        set_mode([0, "in"]);

        // values above 500 should be considered as 'pressed' 
        // (precise value seems to depend on the lenght of the connecting wire)
        // 
        var pressed = false;
        var debounce = false;
                
        var get_button_value = function() {
            // console.log("button value: ", analog_read([0]));
            if (analog_read([0]) > 500 && !pressed && !debounce) {
                
                pressed = true;
                debounce = true;
                console.log("button pressed!", armed);

                if (armed) {
                    session.call("io.crossbar.examples.iotcookbook.alarmapp.set_alarm_armed", [false]).then(session.log, session.log);
                } else {
                    session.call("io.crossbar.examples.iotcookbook.alarmapp.set_alarm_armed", [true]).then(session.log, session.log);
                }
                

                // reset after a timeout for de-bouncing
                setTimeout(function() {
                    // shouldn't reset if button still being pressed
                    if (analog_read([0]) < 500) {
                        pressed = false;
                    };
                    debounce = false;
                }, 100)
            } else if (analog_read([0]) < 500 && debounce === false) {
                pressed = false;
            }

            setTimeout(get_button_value, 10);
        };
        get_button_value();

         // trigger/cancel alarm
        set_mode([1, "in"]);

        // values above 500 should be considered as 'pressed' 
        // (precise value seems to depend on the lenght of the connecting wire)
        // 
        var pressed2 = false;
        var debounce2 = false;
                
        var get_button_value2 = function() {
            // console.log("button value: ", analog_read([0]));
            if (analog_read([1]) > 500 && !pressed2 && !debounce2) {
                
                pressed2 = true;
                debounce2 = true;
                console.log("button pressed!", active);

                if (active) {
                    session.call("io.crossbar.examples.iotcookbook.alarmapp.set_alarm_active", [false]).then(session.log, session.log);
                } else {
                    session.call("io.crossbar.examples.iotcookbook.alarmapp.set_alarm_active", [true]).then(session.log, session.log);
                }
                

                // reset after a timeout for de-bouncing
                setTimeout(function() {
                    // shouldn't reset if button still being pressed
                    if (analog_read([1]) < 500) {
                        pressed2 = false;
                    };
                    debounce2 = false;
                }, 100)
            } else if (analog_read([1]) < 500 && debounce2 === false) {
                pressed2 = false;
            }

            setTimeout(get_button_value2, 10);
        };
        get_button_value2();





    };

    console.log("Connecting to router ...");

    connection.open();
});

// connect to Arduino over serial speaking Firmata
arduino.connect(device_port);
