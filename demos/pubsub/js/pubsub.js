/******************************************************************************
 *
 *  Copyright 2012-2013 Tavendo GmbH.
 *
 *  Licensed under the Apache 2.0 license
 *  http://www.apache.org/licenses/LICENSE-2.0.html
 *
 ******************************************************************************/

"use strict";

"use strict";

var demoRealm = "crossbardemo";
var demoPrefix = "io.crossbar.demo";

// the URL of the WAMP Router (Crossbar.io)
//
var wsuri;
if (document.location.origin == "file://") {
   wsuri = "ws://127.0.0.1:8080";

} else {
   wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws";
}

var httpUri;

if (document.location.origin == "file://") {
   httpUri = "http://127.0.0.1:8080/lp";

} else {
   httpUri = (document.location.protocol === "http:" ? "http:" : "https:") + "//" +
               document.location.host + "/lp";
}


var sess;
var windowUrl;
var isReconnect = false;

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

function checkChannelId(id) {
   return id != null && id != "" && id.length == _idlen && _idpat.test(id);
}

function isValueChar(e) {

   var kc = e.keyCode;
   if ((kc > 8 && kc < 46 && kc !== 32) || (kc > 90 && kc < 94) || (kc > 111 && kc < 186) ) {
      return false;
   } else {
      return true;
   }
}

var controllerChannelId;
var controllerChannel = null;
var controllerChannelSwitch = null;
var controllerChannelCancel = null;


function switchChannel(newChannelId) {

   onChannelSwitch(controllerChannelId, newChannelId);

   controllerChannelId = newChannelId;
   controllerChannel.disabled = false;
   controllerChannelSwitch.disabled = true;
   controllerChannelCancel.disabled = true;
   controllerChannel.value = controllerChannelId;
}


function updateStatusline(statusline) {
   $(".statusline").html(statusline);
};

var connection = null;
function connect() {

   // the WAMP connection to the Router
   //
   var connection = new autobahn.Connection({
      // url: wsuri,
      transports: [
         {
            'type': 'websocket',
            'url': wsuri
         },
         {
            'type': 'longpoll',
            'url': httpUri
         }
      ],
      realm: "crossbardemo"
   });


   connection.onopen = function (session, details) {

      sess = session;

      controllerChannelId = null;

      setupDemo();

      if (details.x_cb_node_id) {
         updateStatusline("Connected to node <strong>" + details.x_cb_node_id + "</strong> at " + wsuri);
      } else {
         updateStatusline("Connected to " + wsuri);
      }

      // establish prefix to use for shorter URL notation
      // sess.prefix("api", channelBaseUri);

      if (checkChannelId(controllerChannel.value)) {
         switchChannel(controllerChannel.value);
      } else {
         switchChannel(randomChannelId());
      }

      if(typeof(afterAuth) !== "undefined" ) {
         afterAuth(); // only exists in colorpicker demo
      }
   };

   connection.onclose = function() {
      sess = null;
      console.log("connection closed ", arguments);
      updateStatusline("Disconnected");
   }

   connection.open();
}

var setupInfoDictionary = {};

$(document).ready(function()
{
   updateStatusline("Not connected.");

   controllerChannelSwitch = document.getElementById('controller-channel-switch');
   controllerChannelCancel = document.getElementById('controller-channel-cancel');
   controllerChannel = document.getElementById('controller-channel');

   // select the current channel string on focus
   controllerChannel.onmouseup = function() { return false; };
   controllerChannel.onfocus = function(evt) {
         evt.target.select();
   };

   // check for additional demo setup data in the URL
   windowUrl = document.URL; // string

   // check if '?' fragment is present
   // then make dictionary of values here
   if (windowUrl.indexOf('?') !== -1) {
      var setupInfoRaw = windowUrl.split('?')[1];
      var setupInfoSeparated = setupInfoRaw.split('&');

      for (var i = 0; i < setupInfoSeparated.length; i++) {
         var pair = setupInfoSeparated[i].split('=');
         var key = pair[0];
         var value = pair[1];
         setupInfoDictionary[key] = value;
      }

   }
   if ("channel" in setupInfoDictionary) {
      controllerChannel.value = setupInfoDictionary.channel;
   }

   controllerChannel.onkeyup = function (e) {

      if (controllerChannel.value != controllerChannelId) {

         controllerChannelCancel.disabled = false;

         if (controllerChannel.value.length == _idlen && _idpat.test(controllerChannel.value)) {
            controllerChannelSwitch.disabled = false;
         } else {
            controllerChannelSwitch.disabled = true;
         }
      } else {
         controllerChannelCancel.disabled = true;
         controllerChannelSwitch.disabled = true;
      }
   };

   controllerChannelCancel.onclick = function () {
      controllerChannel.value = controllerChannelId;
      controllerChannelSwitch.disabled = true;
      controllerChannelCancel.disabled = true;
   }

   controllerChannelSwitch.onclick = function () {

      switchChannel(controllerChannel.value);
      controllerChannelSwitch.disabled = true;
      controllerChannelCancel.disabled = true;
   }

   // setupDemo();

   connect();

});

var sendTime = null,
    recvTime = null,

    receivedMessages = null,
    receivedMessagesClear = null,

    // curlLine = null,

    pubTopic = null,
    pubMessage = null,
    pubMessageBtn = null,

    currentSubscription = null;

// Note: REST bridge functionality has not yet been implemented for
//       the new version of Crossbar.io, and all related functionality
//       has been disabled for now.

// function updateCurl() {
//    var cbody = $("#pub_message").val();
//    curlLine.value = "curl -d 'topic=" + channelBaseUri + "." + $("#pub_topic").val() + "&event=\"" + cbody + "\"' " + hubRestApi;
// }


function setupDemo() {

   sess.prefix("api", demoPrefix + ".pubsub");

   receivedMessages = document.getElementById('sub_message');
   receivedMessages.value = "";
   receivedMessages.disabled = true;

   receivedMessagesClear = document.getElementById('sub_message_clear');
   receivedMessagesClear.disabled = true;

   receivedMessagesClear.onclick = function () {
      receivedMessages.value = "";
      receivedMessages.scrollTop = receivedMessages.scrollHeight;
      receivedMessagesClear.disabled = true;
   }

   // select the current channel string on focus
   var publishChannel = document.getElementById("pub_topic");
   publishChannel.onmouseup = function() { return false; };
   publishChannel.onfocus = function(evt) {
         evt.target.select();
   };

   // curlLine = document.getElementById('pub_curl');
   // curlLine.readOnly = true;

   pubTopic = document.getElementById('pub_topic');
   pubMessage = document.getElementById('pub_message');

   $("#pub_message").val("Hello, world.");

   pubMessageBtn = document.getElementById('pub_publish');

   pubMessageBtn.onclick = function () {

      if ('performance' in window && 'now' in performance) {
         sendTime = performance.now();         
      } else {
         sendTime = (new Date).getTime();         
      }

      sess.publish("api:" + $("#pub_topic").val(), [$("#pub_message").val()], {}, {acknowledge: true, exclude_me: false}).then(
         function(publication) {
            console.log("published", publication);

         },
         function(error) {
            console.log("publication error", error);
         }
      );
   }
   pubMessageBtn.disabled = false;


   // using jQuery because IE8 handles .onkeyup differently
   $(pubTopic).keyup(function(e) {

      if (isValueChar(e)) {
         if (checkChannelId(pubTopic.value)) {
            // updateCurl();
            $("#pub_topic_full").text(sess.resolve("api:" + pubTopic.value));
            pubMessageBtn.disabled = false;
         } else {
            pubMessageBtn.disabled = true;
         }
      }
   });

   $(pubMessage).keyup(function(e) {

      if (isValueChar(e)) {
         // updateCurl();
      }
   });

   $("#helpButton").click(function() { $(".info_bar").toggle() });

}


function onMessage(args, kwargs, details) {
   var event = args[0];
   console.log("event received", details);

   if (sendTime) {
       if ('performance' in window && 'now' in performance) {
         recvTime = performance.now();  
       } else {
         recvTime = (new Date).getTime();         
       }
      var diff = recvTime - sendTime;
      diff = Math.round(diff * 10)/10;
      $("#sub_message_details_time").text(diff + " ms / " + event.length + " bytes");
      sendTime = null;
   } else {
      $("#sub_message_details_time").text(" - / " + event.length + " bytes");
   }

   receivedMessages.value += event + "\r\n";
   receivedMessages.scrollTop = receivedMessages.scrollHeight;

   receivedMessagesClear.disabled = false;
}


function onChannelSwitch(oldChannelId, newChannelId) {
   console.log("onChannelSwitch", oldChannelId, newChannelId);

   if (oldChannelId) {

      currentSubscription.unsubscribe();

   } else {
      console.log("initial setup");

      // initial setup
      $("#pub_topic").val(newChannelId);
      $("#pub_topic_full").text(sess.resolve("api:" + newChannelId));
      // updateCurl();
   }

   sess.subscribe("api:" + newChannelId, onMessage).then(
      function(subscription) {
         console.log("subscribed", subscription, newChannelId);
         currentSubscription = subscription;
      },
      function(error) {
         console.log("subscription error", error);
      }
   );
   console.log("post subscribe");

   $('#new-window').attr('href', window.location.pathname + '?channel=' + newChannelId);
   $('#secondInstance').attr('href', window.location.pathname + '?channel=' + newChannelId);
   $('#pubsub_new_window_link').html(window.location.protocol + "//" + window.location.host + window.location.pathname + '?channel=' + newChannelId);
   $("#sub_topic_full").text(sess.resolve("api:" + newChannelId));
}

var testreceive = function(args, kwargs, details) {
   console.log("testreceive", args, kwargs, details);
}

