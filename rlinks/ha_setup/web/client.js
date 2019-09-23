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


// filled with a WAMP session once connected
var session = null;
var session_url = null;


function rpc1_test () {
    if (!session) {
        console.log("rpc1_test: session not connected");
        return;
    }
    const logname = "browser-client-1";
    const loop = 1;
    const counter = 1;
    const size = 512;
    const payload = autobahn.nacl.randomBytes(size);

    for (var i = 1; i <= 4; ++i) {
        const proc = "node" + i + ".container1.proc1";
        session.call(proc, [logname, session_url, loop, counter, payload]).then(
            function (res) {
                console.log(proc, res);
            },
            function (err) {
                console.log(proc, err);
            }
        )
    }
}


// callback fired upon new WAMP session
connection.onopen = function (new_session, details) {
    console.log("Connected to " + details.transport.url, details);
    console.log("Crossbar.io node (router worker PID):", details.authextra.x_cb_pid);
    session = new_session;
    session_url = details.transport.url;
};


// callback fired upon WAMP session close (or connection failure)
connection.onclose = function (reason, details) {
    console.log("Disconnected:", reason, details);
    session = null;
    session_url = null;
};


// open WAMP session
console.log('Autobahn ' + autobahn.version + ": connecting to " + url + " ..");
connection.open();
