// backend for alarm app with additional speech synthesis output

var autobahn = require('autobahn');

var connection = new autobahn.Connection({
   url: "ws://192.168.1.134:8080/ws", // replace with the url of your crossbar instance
   realm: "iot_cookbook"
});

connection.onopen = function (session, details) {

   console.log("connected!");

   // alarm active state and procedures
   //
   var alarm_active = false;

   function get_alarm_active () {
      return alarm_active;
   }

   session.register("io.crossbar.examples.iotcookbook.alarmapp.get_alarm_active", get_alarm_active).then(
      function () {
         console.log("registered get_alarm_active");
      },
      function (e) {
         console.log(e);
      }
   );

   function set_alarm_active (args) {
      var active = args[0];

      console.log("set_alarm_active", alarm_active, active);

      if (alarm_active != active) {
         alarm_active = active;
         session.publish("io.crossbar.examples.iotcookbook.alarmapp.on_alarm_active", [alarm_active])
      }
      
      // additional part for speech synthesis output begins
      var alertText = "Intruder alert! The police is being alerted!";

      if (alarm_active) {
         console.log("sending speech!", alertText);

         var piSerial = "6ec468fc"; // change to the one on your pi

         var repetitions = 12; // repeat the alertText this many times
         var say = function () {
            
            if (repetitions > 0) {
            
               repetitions -= 1;
            
               session.call("io.crossbar.examples.iotcookbook.alarmapp." + piSerial + ".speechsynth.say", [alertText]).then(function() {
            
                  setTimeout(function() {
                     if (alarm_active) { // check here since we don't want to have a repetition after the alarm has been cancelled
                        say();   
                     }                     
                  }, 3000);
            
               }, function () {
            
                  console.log("speechsynth error", arguments);
            
               });   
            }
            
         }

         // check whether the Pi is busy speaking before sending anything
         var check = function () {

            session.call("io.crossbar.examples.iotcookbook.alarmapp." + piSerial + ".speechsynth.is_busy").then(function (res) {
               if (res) {
                  check(); // next round of checking, until it's ready
               } else {
                  say();
               }
            }, session.log);
            
         }
         check();
      }
      // additional part for speech synthesis output ends

      return alarm_active;
   }

   session.register("io.crossbar.examples.iotcookbook.alarmapp.set_alarm_active", set_alarm_active).then(
      function () {
         console.log("registered set_alarm_active");
      },
      function (e) {
         console.log(e);
      }
   );


   // alarm armed state and procedures
   //
   var alarm_armed = false;

   function get_alarm_armed () {
      return alarm_armed;
   }

   session.register("io.crossbar.examples.iotcookbook.alarmapp.get_alarm_armed", get_alarm_armed).then(
      function () {
         console.log("registered get_alarm_armed");
      },
      function (e) {
         console.log(e);
      }
   );

   var th = 0.1;

   function on_accelerometer (args) {
      var data = args[0];
      console.log(data);

      var trigger =
         (Math.abs(0 - data.x) > th) ||
         (Math.abs(0 - data.y) > th) ||
         (Math.abs(1 - data.z) > th);

      if (trigger) {
         if (alarm_armed && alarm_active === false) {
            set_alarm_active([true]);
         }
      }
   }

   var accel_subscription = null;

   function set_alarm_armed (args) {

      var active = args[0];

      console.log("set_alarm_armed", alarm_armed, active);

      if (alarm_armed != active) {

         alarm_armed = active;

         if (alarm_armed) {

            session.subscribe("io.crossbar.examples.iotcookbook.alarmapp.on_accelerometer_data", on_accelerometer).then(
               function (sub) {
                  console.log("subcribed to on_accelerometer")
                  accel_subscription = sub;
               },
               function (e) {
                  console.log(e);
               }
            );

         } else {

            if (accel_subscription) {
               accel_subscription.unsubscribe().then(
                  function () {
                     console.log("unsubscribed from on_accelerometer")
                  },
                  function (e) {
                     console.log(e);
                  }
               );
            }
         }
         session.publish("io.crossbar.examples.iotcookbook.alarmapp.on_alarm_armed", [alarm_armed])
      }

      return alarm_armed;
   }

   session.register("io.crossbar.examples.iotcookbook.alarmapp.set_alarm_armed", set_alarm_armed).then(
      function () {
         console.log("registered set_alarm_armed");
      },
      function (e) {
         console.log(e);
      }
   );

};

connection.onclose = function (reason, details) {
   console.log("Connection lost: " + reason);
}

connection.open();
