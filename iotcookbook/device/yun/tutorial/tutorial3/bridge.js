var SerialPort = require("serialport").SerialPort;
var autobahn = require("autobahn");

var config = {
    routerUrl: 'http://192.168.1.136:8080/ws',
    realm: 'realm1',
    deviceId: 'myyun',
    devicePort: '/dev/ttyATH0'
};

var lastData = null;
var ledState = false;

var connection = new autobahn.Connection({url: config.routerUrl, realm: config.realm});

connection.onopen = function (session) {

    console.log("Router connected. Session ID:", session.id);

    var serialPort = new SerialPort("/dev/ttyATH0", {
        baudrate: 115200
    });


    session.register("io.crossbar.demo.yun.tutorial3.get_sensors", function () {
        return lastData;
    });

    session.register("io.crossbar.demo.yun.tutorial3.set_led", function (args) {
        var targetState = args[0];
        
        if (ledState != targetState) {

            var writeBit = targetState === true ? "1" : "0";

            serialPort.write(writeBit + "\n");
            ledState = targetState;
            session.publish("io.crossbar.demo.yun.tutorial3.on_led", [ledState]);
            return true;

        } else {
            return false;
        }

    });

    serialPort.on("open", function () {
        console.log("open");
      
        serialPort.on("data", function(data) {
            
            var values = data.toString("ascii");

            try {

                var button = parseInt(values.split(",")[0]);
                var poti = parseInt(values.split(",")[1]);

                lastData = [button, poti];

                console.log("lastData", lastData);

                session.publish("io.crossbar.demo.yun.tutorial3.on_sensors", [lastData]);

            } catch (e) {
                console.log("could not process line", values);
            }        

        });
      
    });


};

connection.open();
