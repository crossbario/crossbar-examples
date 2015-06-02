<!DOCTYPE html>
<html>
   <head>
      <script type="text/javascript" src="../extjs/ext-all.js"></script>
      <script type="text/javascript" src="php/api.php"></script>
      <script>
         Ext.require([
            'Ext.direct.*',
         ]);

         var startTime;

         function log(event, method) {
            var now = (new Date).getTime();
            var ms = now - startTime;
            var tms = ("      " + ms).slice(-6);
            console.log(tms, ("       " + event).slice(-7), method);
         }

         Ext.onReady(function(){

            // http://www.browserscope.org/?category=network
            Ext.app.REMOTING_API.enableBuffer = false
            Ext.direct.Manager.addProvider(Ext.app.REMOTING_API);

            console.log("Ext.Direct initialized.");
         });

         function test() {

            var n = parseInt(document.getElementById('concurrency').value);

            console.log("Starting with concurrency " + n);
            startTime = (new Date).getTime();

            log("calling", "TestAction.square");
            TestAction.square(7, function(result, event){
               log("result", "TestAction.square", result);
            });

            for (var i = 0; i < n; ++i) {
               log("calling", "TestAction.doEchoSlow");
               TestAction.doEchoSlow("Hello Slow Echo", function(result, event){
                  log("result", "TestAction.doEchoSlow", result);
               });
            }

            log("calling", "TestAction.doEcho");
            TestAction.doEcho("Hello Echo", function(result, event){
               log("result", "TestAction.doEcho", result);
            });

            log("calling", "TestAction.add");
            TestAction.add(23, 7, function(result, event){
               log("result", "TestAction.add", result);
            });
         };
      </script>
   </head>
   <body>
      <h1>Ext.Direct RPCs - Standard (via HTTP/Ajax)</h1>
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
