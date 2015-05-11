var autobahn = require('autobahn');
// var utf8 = require('utf8');
// var wtf8 = require('wtf8');
var fs = require('fs');

var when = autobahn.when; 
var session = null;

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

      function takePhoto (args, kwargs, details) {

         console.log("takePicture called");

         if (details.progress) {
            details.progress(["takePhoto called"]);
         }

         var cameraResult = when.defer();

         var exec = require('child_process').exec;

         
         // exec("fswebcam -d /dev/video0 -r 640x480 --no-banner --save '-'", function(err, stdout, stderr) {
         exec("fswebcam -d /dev/video0 -r 160x120 --no-banner --save '-'", function(err, stdout, stderr) {
            
            if (stdout != "") {
               console.log("picture taken", typeof(stdout), stdout.length);

               if (details.progress) {
                  details.progress(["taken"]);
               }

               // // fails 
               // cameraResult.resolve(stdout);


               // // not a string length issue - below is fine
               // var testString = "";
               // for (var i = 0; i < 116000; i++) {
               //    testString += "0";
               // };
               // cameraResult.resolve(testString);

               // fails
               // var imageUtf8 = utf8.encode(stdout);
               // cameraResult.resolve(imageUtf8);

               // // transmits - but then I really don't want more dependencies
               // var imageWtf8 = wtf8.encode(stdout);
               // cameraResult.resolve(imageWtf8);




               var imageBase64 = new Buffer(stdout).toString('base64');
               cameraResult.resolve(imageBase64);

               var binary = new Buffer(imageBase64).toString('binary');

               fs.writeFile("sample.jpg", stdout, function(err) {
                   if(err) {
                       return console.log(err);
                   }

                   console.log("The file was saved!");
               }); 

               // if (details.progress) {
               //    setTimeout(function () {
               //       details.progress(["transmitting"]);
               //    }, 300); 
               // }
            }
            // console.log("stdout ", stdout);

            if (stderr != "") {
               console.log("stderr ", typeof(stderr), stderr.length);
               // cameraResult.reject(err);   
            }
            
            if (err != null) {
               console.log("exec error: ", err);
               // cameraResult.reject(err);
            };
         })

         // cameraResult.resolve("test");

         return cameraResult.promise; 

         // return "test";

      };

      session.register("io.crossbar.examples.pi.camera.take_photo", takePhoto).then(
         function (registration) {
            console.log("Procedure 'io.crossbar.examples.pi.camera.take_photo' registered:", registration.id);
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

main();

