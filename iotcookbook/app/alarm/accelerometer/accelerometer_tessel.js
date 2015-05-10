var tessel = require('tessel');
var accel = require('accel-mma84').use(tessel.port['A']);
var autobahn = require('wamp-tessel');

accel.on('ready', function () {
   var rates = accel.availableOutputRates();
   console.log("accelerometer initialized (output rates: " + rates + ")");
   accel.setOutputRate(12.5, function rateSet () {
      main();
   });
});

accel.on('error', function (err) {
   console.log('Error:', err);
});

function main () {

   var connection = new autobahn.Connection({
      url: "ws://192.168.1.134:8080/ws", // replace with the url of your crossbar instance
      realm: "iot_cookbook"
   });

   connection.onopen = function (session, details) {

      console.log("connected!");

      // send publishes to keep wifi alive
      setInterval(function() {
         session.publish("io.crossbar.examples.tessel.keepalive");
      }, 1000);

      accel.on('data', function (xyz) {
         var data = {
            x: xyz[0].toFixed(2),
            y: xyz[1].toFixed(2),
            z: xyz[2].toFixed(2)
         };
         console.log("sending accel data");
         session.publish("io.crossbar.examples.iotcookbook.alarmapp.on_accelerometer_data", ["tessel", data]);
      });

   };

   connection.onclose = function (reason, details) {
      console.log("Connection lost: " + reason, details);
   };

   connection.open();
}
