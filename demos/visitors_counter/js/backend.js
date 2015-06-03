try {
   var autobahn = require('autobahn');
} catch (e) {
   // when running in browser, AutobahnJS will
   // be included without a module system
}

var connectionCount = 0;

// the WAMP connection to the Router
//
var connection = new autobahn.Connection({
   url: "ws://127.0.0.1:8080/ws",
   realm: "crossbardemo"
});

// fired when connection is established and session attached
//
connection.onopen = function (session, details) {

   console.log("connected");

   // return the current connection count
   function getCurrentVisitorCount () {
      console.log("current visitor count requested", connectionCount)
      return connectionCount;
   }
   session.register("io.crossbar.demo.crossbardemo.get-current-visitor-count", getCurrentVisitorCount).then(function() {
      console.log("procedure 'io.crossbar.demo.crossbardemo.get-current-visitor-count' registered");
   }, session.log);

   // subscribe to and handle connection established metaevent
   session.subscribe("wamp.session.on_join", function() {
      connectionCount += 1;
      session.publish("io.crossbar.demo.crossbardemo.on-visitor-count-update", [connectionCount]);

      console.log("visitor joined", connectionCount);
   })

   // subscribe to and handle connection closed metaevent
   session.subscribe("wamp.session.on_leave", function() {

      connectionCount -= 1;
      if (connectionCount < 0) {
         connectionCount = 0;
      }

      session.publish("io.crossbar.demo.crossbardemo.on-visitor-count-update", [connectionCount]);

      console.log("visitor left", connectionCount);

   })

};

// fired when connection was lost (or could not be established)
//
connection.onclose = function (reason, details) {

   console.log("Connection lost: " + reason);

};


// now actually open the connection
//
connection.open();
