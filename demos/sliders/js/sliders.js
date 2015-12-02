/******************************************************************************
 *
 *  Copyright 2012-2014 Tavendo GmbH.
 *
 *                                Apache License
 *                          Version 2.0, January 2004
 *                       http://www.apache.org/licenses/
 *
 ******************************************************************************/

"use strict";

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


function updateStatusline(status) {
   $(".statusline").text(status);
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

   connection.onopen = function (session) {

      sess = session;

      controllerChannelId = null;

      setupDemo();

      updateStatusline("Connected to " + wsuri);

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

var newWindowLink = null,
    currentMasterSubscription = null,
    currentEqSubscription = null,
    isReconnect = false;


function setupDemo() {

   sess.prefix("api", demoPrefix + ".sliders");

   if (isReconnect) {
      return;
   }
   isReconnect = true;

   newWindowLink = document.getElementById('secondInstance');

   $("#master").slider({
      value: 60,
      orientation: "horizontal",
      range: "min",
      animate: true
   });

   $("#master").slider({
      slide: function(event, ui) {
         sess.publish("api:" +  controllerChannelId + ".master", [ui.value]);
      }
   });

   var i = 1;

   $("#eq > span").each(function() {
      // read initial values from markup and remove that
      var value = parseInt($(this).text(), 10);
      var k = i;

      $(this).empty().slider({
         value: value,
         range: "min",
         animate: true,
         orientation: "vertical",

         slide: function(event, ui) {
            sess.publish("api:" +  controllerChannelId + ".eq", [{ idx: k, val: ui.value }]);
         }
      });
      i += 1;
   });

   $("#helpButton").click(function() { $(".info_bar").toggle() });
}


function onMaster(args, kwargs, details) {

   $("#master").slider({
      value: args[0]
   });
}


function onEq(args, kwargs, details) {

   $("#eq span:nth-child(" + args[0].idx + ")").slider({
      value: args[0].val
   });
}


function onChannelSwitch(oldChannelId, newChannelId) {

   if (oldChannelId) {
      currentMasterSubscription.unsubscribe().then(
         function() {
            console.log("unsubscribed master");
         },
         function(error) {
            console.log("master unsubscribe failed", error);
         });
      currentEqSubscription.unsubscribe().then(
         function() {
            console.log("unsubscribed eq");
         },
         function(error) {
            console.log("eq unsubscribe failed", error);
         });
   }

   sess.subscribe("api:" + newChannelId + ".master", onMaster).then(
      function(subscription) {
         currentMasterSubscription = subscription;
      },
      function(error) {
         console.log("subscription failed ", error);
      }
   );

   sess.subscribe("api:" + newChannelId + ".eq", onEq).then(
      function(subscription) {
         currentEqSubscription = subscription;
      },
      function(error) {
         console.log("subscription failed ", error);
      }
   );

   newWindowLink.setAttribute('href', window.location.pathname + '?channel=' + newChannelId);
}
