//
// Example MQTT client using MQTT.js
//

var mqtt = require('mqtt');
var cbor = require('cbor');
var crypto = require('crypto');


// topic we publish and subscribe to
var topic = 'mqtt/test/mytopic1';


// payload decoder for receiving
function decode (payload) {
    //var obj = cbor.decodeFirstSync(payload);
    var obj = cbor.decodeAllSync(payload)[0];
    return obj;
}


// payload encoder for sending
function encode (pid, seq) {
    var obj = {
        args: [pid, seq, crypto.randomBytes(8)]
    };
    var payload = cbor.encode(obj);
    return payload;
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
        var payload = encode(pid, seq);
        client.publish(topic, payload);
        seq += 1;
    }

    setInterval(publish, 1000);
});


// called when a message has been received on a topic that the client subscribes to.
client.on('message', function (topic, payload) {
    // parse payload (a binary buffer) into a structured object
    var obj = decode(payload);
    console.log(obj);
    var pid = obj.args[0];
    var seq = obj.args[1];
    var ran = obj.args[2];
    console.log('event received topic ' + topic + ': pid=' + pid + ', seq=' + seq + ', ran=' + ran.toString('hex'));
    //client.end();
});
