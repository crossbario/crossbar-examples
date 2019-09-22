const when = autobahn.when;

var http_get_json = function (url, timeout) {

    var d = when.defer();
    var req = new XMLHttpRequest();
    req.withCredentials = true; // pass along cookies
    req.onreadystatechange = function () {

       if (req.readyState === 4) {

          // Normalize IE's response to HTTP 204 when Win error 1223.
          // http://stackoverflow.com/a/10047236/884770
          //
          var status = (req.status === 1223) ? 204 : req.status;

          if (status === 200) {

             // parse response
             var data = JSON.parse(req.responseText);

             // response with content
             //
             d.resolve(data);

          } if (status === 204) {

             // empty response
             //
             d.resolve();

          } else {

             // anything else is a fail
             //
             var statusText = null;
             try {
                statusText = req.statusText;
             } catch (e) {
                // IE8 fucks up on this
             }
             d.reject({code: status, text: statusText});
          }
       }
    }

    req.open("GET", url, true);
    req.setRequestHeader("Content-type", "application/json; charset=utf-8");

    if (timeout > 0) {
       req.timeout = timeout; // request timeout in ms

       req.ontimeout = function () {
          d.reject({code: 501, text: "request timeout"});
       }
    }

    req.send();

    if (d.promise.then) {
       // whenjs has the actual user promise in an attribute
       return d.promise;
    } else {
       return d;
    }
 };


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


http_get_json("/config").then(
    function (config) {
        console.log(config);
    },
    function (err) {
        console.log(err);
    }
);
