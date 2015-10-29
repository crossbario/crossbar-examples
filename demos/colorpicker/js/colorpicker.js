/******************************************************************************
 *
 *  Copyright 2012-2014 Tavendo GmbH.
 *
 *  Licensed under the Apache 2.0 license
 *  http://www.apache.org/licenses/LICENSE-2.0.html
 *
 ******************************************************************************/

"use strict";

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

var colorPickersCount = 3, // total number of color pickers as contained in the HTML
    currentSubscription = null,
    newWindowLink = null;

function setupDemo() {

   sess.prefix("api", demoPrefix + ".colorpicker");

   newWindowLink = document.getElementById('secondInstance');

   // setup the color pickers
   for (var i = 0; i < colorPickersCount; ++i) {
      setupPicker(i);
   }

   $("#helpButton").click(function() { $(".info_bar").toggle() });

}

function afterAuth() {
   $.farbtastic('#picker0').setColor("#d0b800");
   $.farbtastic('#picker1').setColor("#555");
   $.farbtastic('#picker2').setColor("#fff");
};

// set colors associated with / controlled by a color picker
function setExtraColors(k, color) {
   // adjust background rectangle color / color text value
   $('#color' + k).css('background-color', color);
   $('#colorvalue' + k).text(color);

   $('#colortext' + k).css('background-color', color);

   $('#colortext' + k + 'a').css('color', color);
   $('#colortext' + k + 'b').css('color', color);
   $('#colortext' + k + 'c').css('color', color);

   $('#c' + k + 'a').css('background-color', color);
   $('#c' + k + 'b').css('background-color', color);
}


// setup color picker by index
function setupPicker(k) {
   $('#picker' + k).farbtastic(function onColorChangeLocal(color) {
      // this is the callback fired when the user manipulates a color picker

      // set colors associated with color picker
      setExtraColors(k, color);

      // publish the color change event on our topic
      sess.publish("api:" + controllerChannelId + ".color_change", [{ index: k, color: color }], {}, {acknowledge: true}).then(
         function(publication) {
            console.log("published", publication, "api" + controllerChannelId + ".color_change");

         },
         function(error) {
            console.log("publication error", error);
         }
      );
   });
}


// our event handler for processing remote color changes
function onColorChangeRemote(args, kwargs, details) {
   console.log("color change remote", args, kwargs, details);
   // set color in color picker
   $.farbtastic('#picker' + args[0].index).setColor(args[0].color, true);

   // set colors associated with color picker
   setExtraColors(args[0].index, args[0].color);
};


function onChannelSwitch(oldChannelId, newChannelId) {

   if (oldChannelId) {
      currentSubscription.unsubscribe();
   }

   oldChannelId = newChannelId;

   sess.subscribe("api:" + newChannelId + ".color_change", onColorChangeRemote).then(
      function(subscription) {
         console.log("subscribed", subscription, "api:" + newChannelId + ".color_change");
         currentSubscription = subscription;

      },
      function(error) {
         console.log("subscription error", error);
      }
   );

   newWindowLink.setAttribute('href', window.location.pathname + '?channel=' + newChannelId);
}
