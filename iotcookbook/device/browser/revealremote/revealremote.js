// connect to a WAMP router
var session = null;

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


// replace with a name or other identifier for your presentation
// if several presentations are to be controlled in the same realm
var presentation_name = "standard"; 

// fired when connection is established and session attached
//
connection.onopen = function (sess, details) {
   console.log("connected");
   session = sess;

   session.prefix('control', 'io.crossbar.revealremote.' + presentation_name);


   // subscriptions to control events
   // (subscriptions are used since this enables controlling multiple presentations
   // simultaneously)
   session.subscribe('control:navigate', navigate);
   session.subscribe('control:autoplay', autoplay);
   
};

// fired when connection was lost (or could not be established)
//
connection.onclose = function (reason, details) {
   console.log("Connection lost: " + reason);
}

// now actually open the connection
//
connection.open();


var navigate = function (args, kwargs, details) {
   var action = args[0];

   switch (action) {
      case "next":
         Reveal.next();
         break;
      case "prev":
         Reveal.prev();
         break;         
      case "right":
         Reveal.right();
         break;
      case "left":
         Reveal.left();
         break;
      case "up":
         Reveal.up();
         break;
      case "down":
         Reveal.down();
         break;
      case "first_slide":
         Reveal.slide(0);
         break;
      case "pause":
         Reveal.togglePause();
         break;
      default:
         console.log("received unknown navigation command ", action);
         break;
   };
};

var autoplay = function (args, kwargs, details) {

      var delay = args[0];
      var loop = args[1];
      console.log("autoplay changed", delay, loop);

      Reveal.configure({ autoSlide: delay });   
      Reveal.configure({ loop: loop });
};
