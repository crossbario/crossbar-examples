console.log("Firmata-WAMP bridge starting ...");

var autobahn = require('autobahn');
var firmata = require('firmata');

var device_id = "123456";

var ledPin = 11;

var board = new firmata.Board("/dev/ttyATH0", function (err) {

    if (err) {
        console.log(err);
        board.reset();
        return;
    } else {
        console.log('Board connected. Firmware: ', board.firmware);        
    }

    var connection = new autobahn.Connection({
             url: 'ws://192.168.43.73:8080/ws',
             realm: 'realm1'
          });

    connection.onopen = function (session) {
        console.log("Router connected. Session ID:", session.id);

        function digital_write (pin, value) {
            if (value) {
                board.digitalWrite(pin, board.HIGH);
            } else {
                board.digitalWrite(pin, board.LOW);                
            }
        }

        session.register('com.example.digital_write', digital_write);

        function set_mode (pin, mode) {
            if (mode == "in") {
                board.pinMode(pin, board.MODES.INPUT);
            } else if (mode == "out") {
                board.pinMode(pin, board.MODES.OUTPUT);
            } else {
                console.log("unknown mode");
            }
        }

        session.register('com.example.set_mode', set_mode);
/*
        board.pinMode(0, board.MODES.INPUT);
        board.analogRead(0, function (value) {
            console.log("pin 0 digital in:", value);
        });

        board.pinMode(1, board.MODES.INPUT);
        board.analogRead(1, function (value) {
            console.log("pin 1 analog in:", value);
        });

        var ledOn = true;
        board.pinMode(ledPin, board.MODES.OUTPUT);

        setInterval(function() {

            if (ledOn) {
                console.log("+");
                board.digitalWrite(ledPin, board.HIGH);
            } else {
                console.log("-");
                board.digitalWrite(ledPin, board.LOW);
            }

            ledOn = !ledOn;
        }, 500);
*/
    };

    console.log("Connecting to router ...");

    connection.open();
});
