// the URL of the WAMP Router (Crossbar.io)
//
var wsuri;
if (document.location.origin == "file://") {
   wsuri = "ws://127.0.0.1:8080";

} else {
   wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws";
}

var httpUri;

if (document.location.origin == "file://") {
   httpUri = "http://127.0.0.1:8080/lp";

} else {
   httpUri = (document.location.protocol === "http:" ? "http:" : "https:") + "//" +
               document.location.host + "/lp";
}

var updateStatusline = function (status) {
   document.getElementsByClassName("statusline")[0].innerHTML = status;
}


// the WAMP connection to the Router
//
var connection = new autobahn.Connection({
   // url: wsuri,
   transports: [
      {
         'type': 'websocket',
         'url': wsuri
      },
      {
         'type': 'longpoll',
         'url': httpUri
      }
   ],
   realm: "crossbardemo"
});


// fired when connection is established and session attached
//
connection.onopen = function (session, details) {

   if (details.x_cb_node_id) {
      updateStatusline("Connected to node <strong>" + details.x_cb_node_id + "</strong> at " + wsuri);
   } else {
      updateStatusline("Connected to " + wsuri);
   }

   main(session);


};

function main (session) {
   // subscribe to future vote event
   session.subscribe("io.crossbar.demo.vote.onvote",
      function(args) {
         var event = args[0];
         document.getElementById("votes" + event.subject).value =
            event.votes;
      });

   // get the current vote count
   session.call("io.crossbar.demo.vote.get").then(
      function(res){
         for(var i = 0; i < res.length; i++) {
            document.getElementById("votes" + res[i].subject).value =
               res[i].votes;
         }
   }, session.log);

   // wire up vote buttons
   var voteButtons = document.getElementById("voteContainer").
                              getElementsByTagName("button");
   for (var i = 0; i < voteButtons.length; i++) {
      voteButtons[i].onclick = function(evt) {
         session.call("io.crossbar.demo.vote.vote",
            [evt.target.id]).then(session.log, session.log);
      };
   }

   // subscribe to vote reset event
   session.subscribe("io.crossbar.demo.vote.onreset", function() {
         var voteCounters = document.getElementById("voteContainer").
                                     getElementsByTagName("input");
         for(var i = 0; i < voteCounters.length; i++) {
            voteCounters[i].value = 0;
         }
      });

   // wire up reset button
   document.getElementById("resetVotes").onclick = function() {
      session.call("io.crossbar.demo.vote.reset").
         then(session.log, session.log);
   };
}


// fired when connection was lost (or could not be established)
//
connection.onclose = function(reason, details) {
   console.log("connection closed ", reason, details);

   if (details.will_retry) {
      updateStatusline("Trying to reconnect in " + parseInt(details.retry_delay) + " s.");
   } else {
      updateStatusline("Disconnected");   
   }
}


// now actually open the connection
//
connection.open();

