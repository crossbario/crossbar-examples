//
// Example MQTT client using MQTT.js
//

var mqtt = require('mqtt');
var parser = require('binary-parser');
var crypto = require('crypto');


// topic we publish and subscribe to
var topic = 'mqtt/test/mytopic1';


// hexlify a byte array
function hexlify (arr) {
  return arr.map(function (byte) {
    return ('0' + (byte & 0xFF).toString(16)).slice(-2);
  }).join('');
}


// payload decoder for receiving
var decoder = new parser.Parser()
    .endianess('big')
    .uint16('pid')
    .int32('seq')
    .array('ran', {
        type: 'uint8',
        length: 8,
        formatter: hexlify
    });


// payload encoder for sending
function encoder (pid, seq) {
    var buf = new Buffer(14);
    buf.writeUInt16BE(pid, 0);
    buf.writeInt32BE(seq, 2);
    crypto.randomBytes(8).copy(buf, 6);
    return buf;
}

// connect to the universal transport we configured in Crossbar.io
var client  = mqtt.connect('mqtt://localhost:8080');

// connect to the dedicated MQTT transport we configured in Crossbar.io
//var client  = mqtt.connect('mqtt://localhost:1883');

// called when the client has connected to the MQTT broker (or when the client reconnects
// upon a lost connection)
client.on('connect', function () {
    var pid = process.pid;
    var seq = 1;

    console.log('connect: pid=' + pid);

    client.subscribe(topic);

    function publish () {
        var payload = encoder(pid, seq);
        client.publish(topic, payload);
        seq += 1;
    }

    setInterval(publish, 1000);
});


// called when a message has been received on a topic that the client subscribes to.
client.on('message', function (topic, message) {
  // parse message (a binary buffer) into a structured object
  var data = decoder.parse(message);
  console.log('event received topic ' + topic + ': pid=' + data.pid + ', seq=' + data.seq + ', ran=' + data.ran);
  //client.end();
});
