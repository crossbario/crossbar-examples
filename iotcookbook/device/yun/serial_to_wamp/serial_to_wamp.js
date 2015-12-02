
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

// our default config which connects to our demo instance
var config = {
    routerUrl: 'wss://demo.crossbar.io/ws',
    realm: 'iot_cookbook',
    deviceId: 'myyun',
    devicePort: '/dev/ttyATH0'
};

//var debug = true;
var debug = false;

// get the config file
var fs = require("fs");

// needs to use the path to the FAT32 partition - FIXME!!!
fs.readFile("config", "utf8", function(err, data) {
    if (err) {

        console.log("Error accessing configuration file. Starting with default config!");
        
    } else {

        cf = data;

        // split by lines - depending on Windows or Unix line endings
        if (cf.indexOf("\r\n")) {
            cf_lines = cf.split("\r\n");    
        } else {
            cf_lines = cf.split("\n");
        }
        
        // iterate over split array an do updates to config
        cf_lines.forEach(function(line) {

            // find out what the type of config setting is
            var configKey = line.split(":")[0];
            
            var configValue = line.slice(line.indexOf(":") + 2); // remove the initial space

            config[configKey] = configValue;

        });

    }

    console.log("config now is", config);    

    startBridge();

})


function make_uri (id) {
    return 'io.crossbar.examples.yun.' + config.deviceId + '.firmata.' + id;
}

function startBridge () {
    
    console.log("Arduino/Firmata-to-WAMP bridge starting ...");

    var autobahn = require('autobahn');
    var firmata = require('arduino-firmata');

    var arduino = new firmata();

    arduino.on('connect', function () {

        console.log("Arduino connected (over " + arduino.serialport_name + ", board version " + arduino.boardVersion + ")");

        // need to add support for WAMP-CRA authentication!! - IMPLEMENT ME

        var connection = new autobahn.Connection({url: config.routerUrl, realm: config.realm});

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

                console.log("digital read", value);

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
                        console.log("Procedure '" + regs[i].procedure + "' has registration ID " + regs[i].id);
                    }
                },
                function (err) {
                    console.log("Could not register procedures", err);
                }
            );
        };

        console.log("Connecting to router ...");

        connection.open();
    });

    // connect to Arduino over serial speaking Firmata
    arduino.connect(config.devicePort);

};


