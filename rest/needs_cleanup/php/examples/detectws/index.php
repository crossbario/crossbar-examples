<!DOCTYPE html>
<html>
   <body>
   <?php
      require('../../webmqconnect/webmqconnect.php');
      $wssupport = lookupWsSupport();
   ?>

   <h1>Detecting WebSocket Support with WebMQ Connect for PHP</h1>

   <h2>WebSocket Support Detection Results</h2>
   <table>
      <tr>
         <td>User Agent</td>
         <td><?php echo $wssupport['user_agent']; ?></td>
      </tr>
      <tr>
         <td>Detected?</td>
         <td><?php if ($wssupport['detected']) echo 'Yes'; else echo 'No'; ?></td>
      </tr>
      <tr>
         <td>Detected Browser</td>
         <td><?php echo $wssupport['browser']; ?></td>
      </tr>
      <tr>
         <td>WebSocket Supported?</td>
         <td><?php if ($wssupport['ws_supported']) echo 'Yes'; else echo 'No'; ?></td>
      </tr>
      <tr>
         <td>Needs Hixie-76?</td>
         <td><?php if ($wssupport['needs_hixie76']) echo 'Yes'; else echo 'No'; ?></td>
      </tr>
      <tr>
         <td>Needs Flash Polyfill?</td>
         <td><?php if ($wssupport['needs_flash']) echo 'Yes'; else echo 'No'; ?></td>
      </tr>
   </table>

   <h2>Needs Hixie-76</h2>
   <p>
      If you want to support browsers for which Hixie-76 support is required,
      you will need to make sure Hixie-76 support is enabled in your
      Tavendo WebMQ appliance.
   </p>

   <h2>Needs Flash Polyfill</h2>
   <p>
      When the browser has been detected to need the Flash WebSocket polyfill,
      include the following in the generated HTML's head:
   </p>

   <pre>
&lt;script type="text/javascript"&gt;
  WEB_SOCKET_SWF_LOCATION = "web-socket-js/WebSocketMain.swf";
  WEB_SOCKET_DEBUG = false;
  WEB_SOCKET_FORCE_FLASH = true;
&lt;/script&gt;
&lt;script type="text/javascript" src="web-socket-js/swfobject.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="web-socket-js/web_socket.js"&gt;&lt;/script&gt;
   </pre>

   <p>
      You can find all 3 files required <a href="https://github.com/gimite/web-socket-js/">here</a>.
   </p>
   </body>
</html>
