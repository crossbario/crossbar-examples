var SerialPort = require("serialport").SerialPort
// var list = require("serialport");

// adjust the port & baudrate for your setup

// Serial port to use (e.g. 2 (the integer) for a COM port ('COM3' here) on Windows,
// /dev/ttyATH0 for Arduino Yun or /dev/ttyACM0 for Serial-over-USB from Linux

var port = "/dev/ttyATH0"
// var port = "/dev/ttyACM0"
// var port = 2

var serialPort = new SerialPort("/dev/ttyATH0", {
    baudrate: 115200
});


serialPort.on("open", function () {
    console.log("open");
  
    serialPort.on("data", function(data) {
        
        var values = data.toString("ascii");

        try {

            var button = parseInt(values.split(",")[0]);
            var poti = parseInt(values.split(",")[1]);

        } catch (e) {
            console.log("could not process line", values);
        }
        
        if (button || poti > 400) {
            serialPort.write("1\n");
        } else {
            serialPort.write("0\n");
        }
    });
  
});

