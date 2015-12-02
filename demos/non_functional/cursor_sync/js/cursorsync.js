/******************************************************************************
 *
 *  Copyright Tavendo GmbH.
 *
 *  Licensed under the Apache 2.0 license
 *  http://www.apache.org/licenses/LICENSE-2.0.html
 *
 ******************************************************************************/

"use strict";

var demoRealm = "crossbardemo";
var demoPrefix = "io.crossbar.demo";

var wsuri;
if (document.location.origin == "file://") {
   wsuri = "ws://127.0.0.1:8080/ws";

} else {
   wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws";
}

var session = null;

var _idchars = "0123456789";
var _idlen = 6;
var _idpat = /^\d*$/;


function randomChannelId() {
   var id = "";
   for (var i = 0; i < _idlen; i += 1) {
      id += _idchars.charAt(Math.floor(Math.random() * _idchars.length));
   }
   return id;
};


function updateStatusline(status) {
   // $(".statusline").text(status);
};

var connection = null;
function connect() {

   connection = new autobahn.Connection({
      url: wsuri,
      realm: demoRealm,
      max_retries: 30,
      initial_retry_delay: 2
      }
   );

   connection.onopen = function (sess) {

      session = sess;

      setupDemo();


   };

   connection.onclose = function() {
      sess = null;
      console.log("connection closed ", arguments);
   }

   connection.open();
}

var setupInfoDictionary = {};

var sendTime = null,
    recvTime = null,

    receivedMessages = null,
    receivedMessagesClear = null,

    pubTopic = null,
    pubMessage = null,
    pubMessageBtn = null,

    currentSubscription = null;

function setupDemo() {

   function setCursorPosition (box, offsetX, offsetY) {
      // we adjust the position of a cursor representation,
         // offset a bit from the actual position - implement me!
         // check that this does maxes out at the vertical + horizontal dimensions of the box (- the dimensions of the cursor)

      //  right and left border
      if (offsetX > elements[box].offsetWidth - 7) {
         offsetX = elements[box].offsetWidth - 7;
      }

      // top and bottom border
      if (offsetY > elements[box].offsetHeight - 9) {
         offsetY = elements[box].offsetHeight - 9;
      }


      elements[box + "cursor"].style.left = (offsetX) + "px"; 
      elements[box + "cursor"].style.top = (offsetY) + "px"; 
   }


   function onMouseMove (evt) {
      // we get the box this occurs on
      var box = evt.target.id;

      // exclude events on the border of the box
      if (box != "box1" && box != "box2" ) {
         return;
      }

      // console.log("onMouseMove", box, evt);
      // we get the current position within the box (offset)
      var offsetX = evt.offsetX + 3;
      var offsetY = evt.offsetY -5;

      setCursorPosition(box, offsetX, offsetY);
     
      // we publish this position 
      session.publish("io.crossbar.demo.cursor_sync." + channel, [], { box: box, offsetX: offsetX, offsetY: offsetY }, { exclude_me: false });
   };

   // we generate the channel ID
   var channel = randomChannelId();
   // we get the two elements
   var elements = {}; 
   
   elements.box1 = document.getElementById("box1");
   elements.box2 = document.getElementById("box2");
   elements.box1cursor = document.getElementById("box1cursor");
   elements.box2cursor = document.getElementById("box2cursor");
   
   // we attach our event listeners
   elements.box1.addEventListener("mousemove", onMouseMove);
   elements.box2.addEventListener("mousemove", onMouseMove);

   var onReceiveMouseMove = function (args, kwargs) {
      
      var box = kwargs.box === "box1" ? "box2" : "box1";

      setCursorPosition(box, kwargs.offsetX, kwargs.offsetY);

   }
  
   session.subscribe("io.crossbar.demo.cursor_sync." + channel, onReceiveMouseMove);

}

connect();