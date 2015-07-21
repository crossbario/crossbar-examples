/******************************************************************************
 *
 *  Copyright 2012-2014 Tavendo GmbH.
 *
 *                                Apache License
 *                          Version 2.0, January 2004
 *                       http://www.apache.org/licenses/
 *
 ******************************************************************************/

// Create keyboard events to control HexGL racing game based on WAMP events

(function() {

   "use strict";

   var demoRealm = "iot_cookbook";

   var wsuri = "ws://192.168.1.136:8080/ws";
   // if (document.location.origin == "file://") {
   //    wsuri = "ws://127.0.0.1:8080/ws";

   // } else {
   //    wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
   //                document.location.host + "/ws";
   // }

   var session;

   function updateStatusline(status) {
      $(".statusline").text(status);
   };

   var connection = null;
   function connect() {

      connection = new autobahn.Connection({
         url: wsuri,
         realm: demoRealm
         }
      );

      connection.onopen = function (sess) {

         console.log("connected");

         session = sess;

         setupConnector();

         updateStatusline("Connected to " + wsuri);

      };

      connection.onclose = function() {
         session = null;
         console.log("connection closed ", arguments);
      }

      connection.open();
   }

   connect();

   function setupConnector() {

      var createKeyBoardEvents = function (args, kwargs, details) {

         var code = args[0];
         console.log("received controlEvent", code);

         var keyEvent = new KeyboardEvent("keydown", { code: parseInt(code) });
       
         document.dispatchEvent(keyEvent);

         // var evt = document.createEvent("KeyboardEvent");
         // evt.initKeyboardEvent("keydown", true, true, window, keyCode);
         // document.dispatchEvent(evt);


         // if (document.createEventObject) {
         //    console.log("1");
         //    var eventObj = document.createEventObject();
         //    eventObj.keyCode = keyCode;
         //    document.fireEvent("onkeydown", eventObj);   
         // } else if (document.createEvent) {
         //    console.log("2");
         //    var eventObj = document.createEvent("Events");
         //    eventObj.initEvent("keydown", true, true);
         //    eventObj.which = keyCode;
         //    document.dispatchEvent(eventObj);
         // }

         // var press = jQuery.Event("keypress");
         // press.which = keyCode;
         // $("document").trigger(press);

      };

      // subscribe to the control event
      session.subscribe("io.crossbar.examples.yun.gamecontrol.on_event", createKeyBoardEvents);


      document.addEventListener("keydown", function (evt) {
            console.log("keyDown", evt.code);
      });

   }

})();
