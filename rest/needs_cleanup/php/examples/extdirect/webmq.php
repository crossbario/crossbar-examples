<!DOCTYPE html>
<html>
   <head>
      <link rel="stylesheet" href="styles.css">

      <!-- include AutobahnJS .. that's all you need -->
      <script src="http://autobahn.s3.amazonaws.com/js/autobahn.min.js"></script>

      <script>

         // Tavendo WebMQ WebSocket/WAMP URL
         var wsuri = "<?php echo $_POST['wsuri']; ?>";

         // Authentication key & secret
         var authkey = "<?php echo $_POST['authkey']; ?>";
         var authsecret = null;
         if (authkey == "") {
            authkey = null;
         } else {
            authsecret = "<?php echo $_POST['authsecret']; ?>";
         }

         // WAMP session object
         var sess = null;

         var startTime;

         function log(event, method) {
            var now = (new Date).getTime();
            var ms = now - startTime;
            var tms = ("      " + ms).slice(-6);
            console.log(tms, ("       " + event).slice(-7), method);
         }

         window.onload = function() {

            // connect to WAMP server
            ab.connect(wsuri,

               // WAMP session was established
               function (session) {

                  sess = session;

                  console.log("Connected to " + wsuri);

                  onConnect();
               },

               // WAMP session is gone
               function (code, reason) {

                  sess = null;

                  if (code == ab.CONNECTION_UNSUPPORTED) {
                     window.location = "http://autobahn.ws/unsupportedbrowser";
                  } else {
                     console.log(reason);
                  }
               }
            );
         };

         // authenticate as "anonymous"
         function onConnect() {
            var extra = null;
/*
            if (document.cookie != "") {
               extra = {cookies: {}};
               //extra.cookies[document.domain] = document.cookie;
               extra.cookies["demo.record-evolution.com"] = "__utma=231747228.1060551579.1338469050.1339924283.1342708058.4; __utmz=231747228.1338469050.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHPSESSID=sj83dpbh2vrgcso7bg1ad8hhu0";
            }
*/
            var extra = {cookies: {}};
            extra.cookies["record-evolution.com"] = "__utma=231747228.1060551579.1338469050.1339924283.1342708058.4; __utmz=231747228.1338469050.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHPSESSID=sj83dpbh2vrgcso7bg1ad8hhu0";

            sess.authreq(null, extra).then(function () {
               sess.auth().then(onAuth, ab.log);
            }, ab.log);
         }

         // we are now authenticated
         function onAuth(permissions) {
            ab.log("authenticated", permissions);

            sess.prefix("TestAction", "http://example.com/TestAction#");
         };

         function test() {

            var n = parseInt(document.getElementById('concurrency').value);

            console.log("Starting with concurrency " + n);
            startTime = (new Date).getTime();

            log("calling", "TestAction.square");
            sess.call("TestAction:square", 7).then(function (result) {
               log("result", "TestAction.square", result);
            }, ab.log);

            for (var i = 0; i < n; ++i) {
               log("calling", "TestAction.doEchoSlow");
               sess.call("TestAction:doEchoSlow", "Hello Slow Echo").then(function (result) {
                  log("result", "TestAction.doEchoSlow", result);
               });
            }

            log("calling", "TestAction.doEcho");
            sess.call("TestAction:doEcho", "Hello Echo").then(function (result) {
               log("result", "TestAction.doEcho", result);
            });

            log("calling", "TestAction.add");
            sess.call("TestAction:add", 23, 7).then(function (result) {
               log("result", "TestAction.add", result);
            });
         };
      </script>
   </head>
   <body>
      <h1>Ext.Direct RPCs - Tavendo WebMQ (via WebSocket/WAMP)</h1>
      <noscript>
         <span style="color: #f00; font-weight: bold;">
            You need to turn on JavaScript.
         </span>
      </noscript>
      <p>
         Open development console (press F12) to watch. Then press "Start".
      </p>
      <form>
         Concurrency: <input type="number" id="concurrency" value="8" min="1" max="100">
      </form>
      <button onclick="test();">Start</button>
   </body>
 </html>
