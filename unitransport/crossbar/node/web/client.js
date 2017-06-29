var connection = new autobahn.Connection({
   url: 'ws://localhost:8080/ws',
   realm: 'realm1'}
);

var this_service = "service0";
var other_services = ["service1", "service2", "service3"];

connection.onopen = function (session) {

   // SUBSCRIBE to a topic and receive events
   //
   function on_counter(args, kwargs, details) {
      var msg = args[0];
      console.log("AutobahnJS/SUBSCRIBE: event for 'on_counter' received: " + msg, details);
   }
   for (var i = 0; i < other_services.length; ++i) {
      session.subscribe('com.example.' + other_services[i] + '.on_counter', on_counter).then(
         function (sub) {
            console.log("AutobahnJS/SUBSCRIBE: subscribed to topic", sub.topic);
         },
         function (err) {
            console.log("AutobahnJS/SUBSCRIBE: failed to subscribed: " + err);
         }
      );
   }

   // REGISTER a procedure for remote calling
   //
   function add2 (args) {
      var x = args[0];
      var y = args[1];
      console.log("AutobahnJS/REGISTER: add2() called with " + x + " and " + y);
      return 10 + x + y;
   }
   session.register('com.example.' + this_service + '.add2', add2).then(
      function (reg) {
         console.log("AutobahnJS/REGISTER: procedure add2() registered");
      },
      function (err) {
         console.log("AutobahnJS/REGISTER: failed to register procedure: " + err);
      }
   );


   // PUBLISH and CALL every second .. forever
   //
   var counter = 0;
   setInterval(function () {

      // PUBLISH an event
      //
      session.publish('com.example.' + this_service + '.on_counter', [counter]);
      console.log("AutobahnJS/PUBLISH: published to 'on_counter' with on_counter " + counter);

      // CALL a remote procedure
      //
      for (var i = 0; i < other_services.length; ++i) {
         session.call('com.example.' + other_services[i] + '.add2', [counter, 3]).then(
            function (res) {
               console.log("AutobahnJS/CALL: add2() called with result: " + res);
            },
            function (err) {
               if (err.error !== 'wamp.error.no_such_procedure') {
                  console.log('AutobahnJS/CALL: call of add2() failed: ' + err);
               }
            }
         );
      }

      counter += 1;
   }, 1000);
};

connection.open();
