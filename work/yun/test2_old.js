console.log("Arduino/Firmata-to-WAMP bridge starting ...");

/*
#define O0 11
#define O1 10
#define O2 9
#define O3 6
#define O4 5
#define O5 3
#define I0 A0
#define I1 A1
#define I2 A2
#define I3 A3
#define I4 A4
#define I5 A5
*/

// configuration:
var router = 'ws://192.168.1.136:8080/ws';
var realm = 'realm1';
var device_id = '123456';
var device_port = '/dev/ttyATH0';


var autobahn = require('autobahn');
var firmata = require('arduino-firmata');

var arduino = new firmata();

arduino.on('connect', function () {

    console.log("Arduino connected (over " + arduino.serialport_name + ", board version " + arduino.boardVersion + ")");

    var connection = new autobahn.Connection({url: router, realm: realm});

    connection.onopen = function (session) {
        console.log("Router connected. Session ID:", session.id);

        var regs = [];

        function set_mode (pin, mode) {
            if (mode == "in") {
                arduino.pinMode(pin, firmata.INPUT);
            } else if (mode == "out") {
                arduino.pinMode(pin, firmata.OUTPUT);
            } else {
                console.log("unknown mode");
            }
        }

        regs.push(session.register('com.example.set_mode', set_mode));

        function digital_read (pin) {
            return arduino.digitalRead(pin);
        }

        regs.push(session.register('com.example.digital_read', digital_read));

        function digital_write (pin, value) {
            if (value) {
                arduino.digitalWrite(pin, True);
            } else {
                arduino.digitalWrite(pin, False);
            }
        }

        regs.push(session.register('com.example.digital_write', digital_write));

        autobahn.when.all(regs).then(
            function () {
                console.log("All procedures registered.");
            },
            function (err) {
                console.log("Could not register procedures", err);
            }
        );

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


  arduino.pinMode(11, firmata.OUTPUT);
  arduino.pinMode(10, firmata.OUTPUT);

  arduino.on('analogChange', function(e){
    if(e.pin != 1) return;
    console.log("pin" + e.pin + " : " + e.old_value + " -> " + e.value);
  });

  arduino.pinMode(0, firmata.INPUT);

  var stat = true
  var cnt = 0;
  setInterval(function(){
//    console.log(stat);
    arduino.digitalWrite(11, stat);
    arduino.digitalWrite(10, !stat);
    stat = !stat;

    var pin_stat = arduino.digitalRead(0);
    console.log(pin_stat);
    /*    
    cnt += 1;
    if (cnt % 5 == 0) {
        console.log("resetting ..");
        arduino.reset(function () {
            console.log("on-reset");
        });
    }
*/
  }, 1000);
});

// connect to Arduino over serial speaking Firmata
arduino.connect(device_port);
