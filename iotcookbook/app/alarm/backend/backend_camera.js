//  backend for alarm app with camera component (Tessel or Pi)
//  only handles a single camera component!

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

         // camera component specific code
         if (alarm_active) {
            session.call("io.crossbar.examples.iot_cookbook.alarmapp.take_photo", [], {}, {receive_progress: true}).then(
               function (res) {
                  console.log("received image, publishing");
                  session.publish("io.crossbar.examples.iotcookbook.alarmapp.on_photo_taken", res);
               }, 
               function (err) {
                  console.log("requestImage failed", err);
               },
               // only called from Tessel camera - it's slow, so with this you know it 
               // didn't just crash!
               function (progress) {
                  session.publish("io.crossbar.examples.iotcookbook.alarmapp.on_photo_progress", progress);
               }
            );
         }        
         // camera component specific code end

      }
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

   var th_tessel = 0.1; // threshold for tessel
   var th_yun = 80; // threshold for yun

   function on_accelerometer (args) {

      var device = args[0];
      var data = args[1];
      var trigger = null;

      if (device === "tessel") {

         trigger =
            (Math.abs(0 - data.x) > th_tessel) ||
            (Math.abs(0 - data.y) > th_tessel) ||
            (Math.abs(1 - data.z) > th_tessel);
      
      } else if (device === "yun") {
      
         trigger =
            data.x > 550 + th_yun || data.x < 550 - th_yun || 
            data.y > 550 + th_yun || data.y < 550 - th_yun;
      
      } else {
         console.log("received accelerometer data from unknown device class");
      }      

      if (trigger) {
         if (alarm_armed) {
            set_alarm_active([true]);
         }
      }
   }

   var accel_subscription = null;
   var accel_subscription_yun = null;

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
