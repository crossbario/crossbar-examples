<!DOCTYPE html>
<html>
   <head>
      <link rel="stylesheet" href="styles.css">
   </head>
   <body>
      <h1 class="title">Tavendo WebMQ - Push from PHP</h1>

      <form action="client.php" target="_blank" method="post">
         <h1>Real-time Client</h1>
         <p>
            WebSocket Service:
            <input type="text" name="wsuri" size="40" value="wss://webmq.tavendo.de/ws" />
         </p>
         <p>
            Topic:
            <input type="text" name="topic" size="60" value="http://autobahn.tavendo.de/public/demo/topic1" />
         </p>
         <p>
            Auth Key (optional):
            <input type="text" name="authkey" size="10" value="" />
         </p>
         <p>
            Auth Secret (optional):
            <input type="text" name="authsecret" size="10" value="" />
         </p>
         <p>
            <input type="submit" value="Open" />
         </p>
      </form>

      <form action="form.php" target="_blank" method="post">
         <h1>User Form</h1>
         <p>
            Push Service:
            <input type="text" name="pushendpoint" size="40" value="http://webmq.tavendo.de:8080" />
         </p>
         <p>
            Topic:
            <input type="text" name="topic" size="60" value="http://autobahn.tavendo.de/public/demo/topic1" />
         </p>
         <p>
            Auth Key (optional):
            <input type="text" name="authkey" size="10" value="" />
         </p>
         <p>
            Auth Secret (optional):
            <input type="text" name="authsecret" size="10" value="" />
         </p>
         <p>
            <input type="submit" value="Open" />
         </p>
      </form>

   </body>
</html>
