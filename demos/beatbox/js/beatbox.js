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

var newWindowLink = null;

var currentSubscriptions = [];


// options checkboxes
var enable_audio = null;
var pub_trigger = null;
var direct_trigger = null;

var samples = [];
var buttons = [];

var isReconnect = false;

/**
 * For unclear reasons, Chrome will persistently fail to rewind the samples when
 * the media files are served from Flask/SocketServer.
 * When Flask is served from Twisted, this will fail on first load, but then
 * on refresh (F5) it succeeds. Needs further investigation.
 * With the sound files served from Apache, this does not happen ..
 */
var samplesBaseUri = 'snd/';


function loadSample(btn, file) {
   samples[btn] = document.createElement('audio');
   samples[btn].setAttribute('src', samplesBaseUri + file);
   samples[btn].load();
   samples[btn].volume = 1;
   samples[btn].loop = true;
}


function setupDemo() {

   console.log("setupDemo", sess.id, sess.isOpen);

   sess.prefix("api", demoPrefix + ".beatbox");

   if (isReconnect) {
      return;
   }
   isReconnect = true;

   newWindowLink = document.getElementById('secondInstance');

   // IE doesn't do WAV, FF doesn't do mp3s
   if(navigator.userAgent.indexOf("Trident") !== -1)  {
      console.log("IE detected - loading mp3s");
      loadSample(0, 'demo_beatbox_sample_a.mp3');
      loadSample(1, 'demo_beatbox_sample_b.mp3');
      loadSample(2, 'demo_beatbox_sample_c.mp3');
      loadSample(3, 'demo_beatbox_sample_d.mp3');
   } else {
      console.log("using WAV versions of samples");
      loadSample(0, 'demo_beatbox_sample_a.wav');
      loadSample(1, 'demo_beatbox_sample_b.wav');
      loadSample(2, 'demo_beatbox_sample_c.wav');
      loadSample(3, 'demo_beatbox_sample_d.wav');
   }

   // check if audio enabled via URL switch
   if ("audio" in setupInfoDictionary && setupInfoDictionary.audio === "off") {
      document.getElementById('enable_audio').checked = false;
   }

   enable_audio = document.getElementById('enable_audio');
   pub_trigger = document.getElementById('pub_trigger');
   direct_trigger = document.getElementById('direct_trigger');

   buttons[0] = { btn: document.getElementById('button-a'), pressed: false };
   setPadButtonHandlers(buttons[0].btn, 0);

   buttons[1] = { btn: document.getElementById('button-b'), pressed: false };
   setPadButtonHandlers(buttons[1].btn, 1);

   buttons[2] = { btn: document.getElementById('button-c'), pressed: false };
   setPadButtonHandlers(buttons[2].btn, 2);

   buttons[3] = { btn: document.getElementById('button-d'), pressed: false };
   setPadButtonHandlers(buttons[3].btn, 3);

   // for suppressing key-autorepeat events
   var keysPressed = {};

   window.onkeydown = function(e) {

      if (keysPressed[e.keyCode]) {
         return;
      } else {
         keysPressed[e.keyCode] = true;
      }

      switch (e.keyCode) {
         case 65:
            padButton(0, true);
            break;
         case 66:
            padButton(1, true);
            break;
         case 67:
            padButton(2, true);
            break;
         case 68:
            padButton(3, true);
            break;
      }
   };

   window.onkeyup = function(e) {

      keysPressed[e.keyCode] = false;

      switch (e.keyCode) {
         case 65:
            padButton(0, false);
            break;
         case 66:
            padButton(1, false);
            break;
         case 67:
            padButton(2, false);
            break;
         case 68:
            padButton(3, false);
            break;
      }
   };

   $("#helpButton").click(function() { $(".info_bar").toggle(); });
}

function onPadButtonDown(args, kwargs, details) {

   console.log("onPadButtonDown", args, kwargs, details);

   if (!buttons[kwargs.b].pressed) {

      if (enable_audio.checked) {
         console.log("playing a sample");

         // do NOT change order/content of the following 2 lines!
         samples[kwargs.b].currentTime = 0;
         samples[kwargs.b].play();
      }

      buttons[kwargs.b].pressed = true;
      buttons[kwargs.b].btn.style.background = "#d0b800";
   }
}


function onPadButtonUp(args, kwargs, details) {

   console.log("onPadButtonUp", args, kwargs, details);

   if (buttons[kwargs.b].pressed) {

      if (enable_audio.checked) {
         // do NOT change order/content of the following 2 lines!
         samples[kwargs.b].currentTime = 0;
         samples[kwargs.b].pause();
      }

      buttons[kwargs.b].pressed = false;
      buttons[kwargs.b].btn.style.background = "#666";
   }
}


function padButton(btn, down) {

   if (down) {
      if (direct_trigger.checked) {
         onPadButtonDown(null, { "b": btn, "t": 0 });
      }
      if (pub_trigger.checked) {
         sess.publish("api:" + controllerChannelId + ".pad_down", [], { "b": btn, "t": 0 }, { exclude_me: false, acknowledge: true }).then(
            function(publication) {
               console.log("published", publication);
            },
            function(error) {
               console.log("publication error");
            }
         );
      }
   } else {
      if (direct_trigger.checked) {
         onPadButtonUp(null, { "b": btn, "t": 0});
      }
      if (pub_trigger.checked) {
         sess.publish("api:" + controllerChannelId + ".pad_up", [], { "b": btn, "t": 0}, { exclude_me: false, acknowledge: true }).then(
            function(publication) {
               console.log("published", publication);
            },
            function(error) {
               console.log("publication error");
            }
         );
      }
   }
}


function setPadButtonHandlers(button, btn) {

   button.ontouchstart = function(evt) {
      padButton(btn, true);
      evt.preventDefault();
   };
   button.ontouchend = function(evt) {
      padButton(btn, false);
      evt.preventDefault();
   };

   button.onmousedown = function() {
      padButton(btn, true);
   };
   button.onmouseup = function() {
      padButton(btn, false);
   };
   // prevent buttons from getting stuck on mouseout, since mouseup no longer on button
   button.onmouseout = function() {
      padButton(btn, false);
   };



}


function onChannelSwitch(oldChannelId, newChannelId) {

   if (oldChannelId) {
      // check whether session for subscriptions still open
      // since this might be called on a reconnect
      if(currentSubscriptions[0].session.isOpen === true) {
         currentSubscriptions[0].unsubscribe();
         currentSubscriptions[1].unsubscribe();
      }
   }

   sess.subscribe("api:" + newChannelId + ".pad_down", onPadButtonDown).then(
      function(subscription) {
         console.log("subscribed pad_down", subscription);
         currentSubscriptions[0] = subscription;
      },
      function(error) {
         console.log("subscription error pad_down", error);
      }
   );
   sess.subscribe("api:" + newChannelId + ".pad_up", onPadButtonUp).then(
      function(subscription) {
         console.log("subscribed pad_up", subscription);
         currentSubscriptions[1] = subscription;
      },
      function(error) {
         console.log("subscription error pad_up", error);
      }
   );

   newWindowLink.setAttribute('href', window.location.pathname + '?channel=' + newChannelId + '&audio=off');
}
