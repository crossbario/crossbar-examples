var autobahn = require('wamp-tessel');
var tessel = require('tessel');
var camera = require('camera-vc0706').use(tessel.port['A']);

var when = autobahn.when; 
var session = null;

var notificationLED = tessel.led[3]; // Set up an LED to notify when we're taking a picture
var cameraReady = false;

camera.on('ready', function() {
   
   console.log("camera ready");

   // camera.setResolution("vga");
   // camera.setResolution("qvga");
   camera.setResolution("qqvga"); // gives you the (relatively) quickest response

   main();

});

camera.on('error', function(err) {
   console.error("camera error", err);
   // add a publication of camera error - IMPLEMENT ME!!!
});

function main () {

   console.log("main called");

   // the WAMP connection to the Router
   //
   var connection = new autobahn.Connection({
      url: "ws://192.168.1.134:8080/ws", // replace with the url of your crossbar instance
      realm: "iot_cookbook"
   });

   // fired when connection is established and session attached
   //
   connection.onopen = function (sess, details) {

      console.log("connected");

      session = sess;

      // send publishes to keep wifi alive (testing)
      setInterval(function() {
         session.publish("io.crossbar.examples.tessel.keepalive");
      }, 1000);

      function takePhoto (args, kwargs, details) {

         console.log("takePicture called");

         if (details.progress) {
            details.progress(["takePhoto called", 0]);
         }

         var cameraResult = when.defer();

         camera.takePicture(function (err, image) {

            console.log("picture taken", Date.now() - t0);

            if (details.progress) {
               details.progress(["taken", Date.now() - t0]);
            }
            
            // notification LED on for two seconds
            notificationLED.high();
            setTimeout(function() {
               notificationLED.low();
            }, 2000);

            if (err) {

               console.log('error taking image', err);
               cameraResult.reject(err);

            } else {

               // need to encode image before sending
               try {

                  if (details.progress) {
                     details.progress(["encoding", Date.now() - t0]);
                  }

                  var encodedImage = image.toString("hex");

                  if (details.progress) {
                     details.progress(["transmitting", Date.now() - t0]);
                  }

                  cameraResult.resolve(encodedImage);
               } catch (e) {
                  console.log("error,", e);
               }
              
            }
         });

         return cameraResult.promise; 

      };

      session.register("io.crossbar.examples.tessel.camera.take_photo", takePhoto).then(
         function (registration) {
            console.log("Procedure 'io.crossbar.examples.tessel.camera.take_photo' registered:", registration.id);
         },
         function (error) {
            console.log("Registration failed:", error);
         }
      );

   };
      

   // fired when connection was lost (or could not be established)
   //
   connection.onclose = function (reason, details) {
      console.log("Connection lost: " + reason);
   }

   // now actually open the connection
   //
   connection.open();

}


