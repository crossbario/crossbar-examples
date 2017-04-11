//
// Example MQTT client using MQTT.js
//

var mqtt = require('mqtt');
var parser = require('binary-parser');

// hexlify a byte array
function hexlify (arr) {
  return arr.map(function (byte) {
    return ('0' + (byte & 0xFF).toString(16)).slice(-2);
  }).join('');
}

// build a binary parser
var myparser = new parser.Parser()
    .endianess('big')
    .uint16('pid')
    .int32('seq')
    .array('ran', {
        type: 'uint8',
        length: 8,
        formatter: hexlify
    });

// connect to the universal transport we configured in Crossbar.io
var client  = mqtt.connect('mqtt://localhost:8080');

// connect to the dedicated MQTT transport we configured in Crossbar.io
//var client  = mqtt.connect('mqtt://localhost:1883');

client.on('connect', function () {
  client.subscribe('mqtt/test/mytopic1');
  //client.publish('presence', 'Hello mqtt');
});

client.on('message', function (topic, message) {
  // parse message (a binary buffer) into a structured object
  var data = myparser.parse(message);
  console.log('event receivedon topic ' + topic + ': pid=' + data.pid + ', seq=' + data.seq + ', ran=' + data.ran);
  //client.end();
});
