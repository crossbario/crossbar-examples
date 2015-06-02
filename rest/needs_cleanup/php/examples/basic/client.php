<!DOCTYPE html>
<html>
   <head>
      <link rel="stylesheet" href="styles.css">

      <!-- AutobahnJS client library -->
      <script src="http://autobahn.s3.amazonaws.com/js/autobahn.min.js"></script>

      <script>

         // Tavendo WebMQ WebSocket/WAMP URL
         var wsuri = "<?php echo $_POST['wsuri']; ?>";

         // The topic we use
         var topic = "<?php echo $_POST['topic']; ?>";

         // Authentication key & secret
         var authkey = "<?php echo $_POST['authkey']; ?>";
         var authsecret = null;
         if (authkey == "") {
            authkey = null;            
         } else {
            authsecret = "<?php echo $_POST['authsecret']; ?>";
         }

         // will hold our WebSocket/WAMP client session
         var session = null;

         window.onload = function() {
            
            // connect upon window load
            connect();
         };

         function connect() {

            // connect to WebMQ
            ab.connect(wsuri,

               // called when connection has been established
               function (sess) {
                  log("connected", wsuri);
                  session = sess;

                  // continue with authentication ..
                  if (authkey) {
                     onConnect1();
                  } else {
                     onConnect0();                     
                  }
               },

               // called when connection was lost, failed or on reconnects
               function (code, reason, detail) {
                  log("connection lost", code, reason, detail);
               }
            );
         }

         // authenticate as "anonymous"
         function onConnect0() {
            session.authreq().then(function () {
               session.auth().then(onAuth, log);
            }, log);
         }

         // authentication using auth key/secret
         function onConnect1() {
            session.authreq(authkey).then(function (challenge) {
               var signature = session.authsign(challenge, authsecret);
               session.auth(signature).then(onAuth, log);
            }, log);
         }

         // we are now authenticated
         function onAuth(permissions) {
            log("authenticated", permissions);

            // subscribe to our topic
            session.subscribe(topic, onEvent);
            log("subscribed", topic);
         };

         // we have received an event on our topic
         function onEvent(topic, event) {
            log("event", topic, event);
         };

         function log() {
            var l = document.getElementById("evts")
            for (var i = 0; i < arguments.length; ++i) {
               if (i > 0) {
                  l.innerHTML += ", ";
               }
               l.innerHTML += JSON.stringify(arguments[i]);
            }
            l.innerHTML += "\n";
         };
      </script>
   </head>
   <body>
      <h1 class="title">Tavendo WebMQ - Push from PHP</h1>
      <pre id="evts"></pre>
   </body>
</html>
