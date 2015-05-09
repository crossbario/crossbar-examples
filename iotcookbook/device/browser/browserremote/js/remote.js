// the URL of the WAMP Router (Crossbar.io)
//
var wsuri;
if (document.location.origin == "file://") {
   wsuri = "ws://127.0.0.1:8080/ws";
} else {
   wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws";
}

// the WAMP connection to the Router
//
var connection = new autobahn.Connection({
   url: wsuri, // replace with URL of WAMP router if this doesn't serve the file!
   realm: "iot_cookbook"
});

var externalUrlWindow = null;


// fired when connection is established and session attached
//
connection.onopen = function (session, details) {

   console.log("connected");

   session.subscribe("io.crossbar.examples.remotecontrol.on_navigate", function(args) {
      var newUrl = args[0];
      window.location.assign(newUrl);
   }).then(session.log, session.log);
   
   session.subscribe("io.crossbar.examples.remotecontrol.on_reload", function() {
      window.location.reload(true);
   }).then(session.log, session.log);
   
   // for this to work, you probably need to allow pop-ups from the domain this page is served from
   // permanently
   session.subscribe("io.crossbar.examples.remotecontrol.on_navigate_external", function(args) {
      console.log("on_navigate_external called", args);
      
      var externalUrl = args[0];
      
      externalUrlWindow = window.open(externalUrl, "externalWindow"); // opens a new window on first call, 
      // else changes the location of the previously created window        
      
   }).then(session.log, session.log);

   session.subscribe("io.crossbar.examples.remotecontrol.on_close_external", function(args) {
      console.log("on_close_external called", args);
      externalUrlWindow.close();
   }).then(session.log, session.log);

};

// fired when connection was lost (or could not be established)
//
connection.onclose = function (reason, details) {
   console.log("Connection lost: " + reason);
}

// now actually open the connection
//
connection.open();

