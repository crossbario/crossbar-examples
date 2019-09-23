// WAMP router URL to use
var url;
if (document.location.origin == "file://") {
    url = "ws://localhost:8080/ws";

} else {
    url = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" + document.location.host + "/ws";
}


// WAMP connection configuration
var connection = new autobahn.Connection({
    realm: "realm1",
    transports: [
        {
            url: url,
            type: 'websocket',
            serializers: [ new autobahn.serializer.MsgpackSerializer() ]
        }
    ],
    initial_retry_delay: 0.01
});


// callback fired upon new WAMP session
connection.onopen = function (session, details) {
    console.log("Connected:", details);
    console.log("Crossbar.io node (router worker PID):", details.authextra.x_cb_pid);
};


connection.onclose = function (reason, details) {
    console.log("Disconnected:", reason, details);
};


// open WAMP session
console.log('Autobahn ' + autobahn.version + ": connecting to " + url + " ..");
connection.open();
