<!DOCTYPE html>
<html>
   <head>
      <link rel="stylesheet" href="styles.css">
   </head>
   <body>
      <h1 class="title">Tavendo WebMQ - Push from PHP</h1>
      <p>
         <?php
            require('../../webmqconnect/webmqconnect.php');
            
            $server = $_POST['pushendpoint'];
            $authkey = trim($_POST['authkey']);
            $authsecret = trim($_POST['authsecret']);
            
            $client = new WebMQConnectClient($server, $authkey, $authsecret);

            $topic = $_POST['topic'];
            
            for ($i = 1; $i <= $_POST['cnt']; $i++) {
               $data = array("name" => $_POST['name'], "age" => $_POST['age'], "no" => $i);
               $result = $client->push($topic, $data);
               if ($result !== null)
               {
                  echo "Push failed: " . $result;
               }
               else
               {
                  echo "Data pushed to <b>" . $server . "</b> on topic <b>" . $topic . "</b>";
               }
            }
         ?>
      </p>
   </body>
</html>
