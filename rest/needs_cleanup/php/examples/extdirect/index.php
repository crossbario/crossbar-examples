<?php session_start(); ?>
<!DOCTYPE html>
<html>
   <head>
      <link rel="stylesheet" href="styles.css">
      <script>
         window.onload = function () {
            var sessid = document.cookie.match(/PHPSESSID=[^;]+/)[0].substr(10);
            document.getElementById('sessid').innerHTML = "Session Cookie: " + sessid;
         }
      </script>
   </head>
   <body>
      <h1>Ext.Direct RPCs Standard vs Tavendo WebMQ</h1>

      <form action="standard.php" target="_blank" method="post">
         <h1>Ext.Direct RPCs Standard</h1>
         <p>
            <input type="submit" value="Open" />
         </p>
      </form>

      <form action="webmq.php" target="_blank" method="post">
         <h1>Ext.Direct RPCs via Tavendo WebMQ</h1>
         <p>
            WebSocket Service:
            <input type="text" name="wsuri" size="40" value="wss://webmq.tavendo.de/ws" />
         </p>
         <p>
            <input type="submit" value="Open" />
         </p>
         <p>
            Auth Key (optional):
            <input type="text" name="authkey" size="10" value="" />
         </p>
         <p>
            Auth Secret (optional):
            <input type="text" name="authsecret" size="10" value="" />
         </p>
      </form>

      <p id="sessid"></p>
   </body>
</html>
