/******************************************************************************
 *
 *  Copyright (C) 2012-2014 Tavendo GmbH.
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

var notificationCount = null;

// notification-related variables
var ad,
    ad_countdown,
    ad_hide,
    ad_shown = false,
    ad_width = 600,
    ad_time_to_hide = 6,
    ad_time_remaining = 0,
    currentSubscription = null;


function abChangeFavicon() {

   var currentIcon = $("#favicon").attr("href");

   $("#favicon").remove();
   var newIcon;
   if (currentIcon === "record.ico") {
      newIcon = "<link id='favicon' rel='shortcut icon' href='favicon.ico'>";
   }
   else {
      newIcon = "<link id='favicon' rel='shortcut icon' href='record.ico'>";
   }
   $(newIcon).appendTo("head");

}


function setupDemo() {

   sess.prefix("api", demoPrefix + ".notification");

   $("#notification_message").val("Hello World!");

   // set up event handlers
   $("#send_notification").click(sendNotification);

   Tinycon.setOptions({
      background: '#000000',
      font: '12px arial',
      width: 8,
      height: 11,
      fallback: true
   });

   // add elements
   ad = document.getElementById('webmqad');
   ad_countdown = document.getElementById('webmqad_countdown');

   // allow manual slide in/out
   ad.onclick = toggle;

   ad_countdown.style.visibility = 'hidden';

   $("#helpButton").click(function() { $(".info_bar").toggle(); });

   // select the current channel string on focus
   var publishChannel = document.getElementById("pub_topic");
   publishChannel.onmouseup = function() { return false; };
   publishChannel.onfocus = function(evt) {
         evt.target.select();
   };
}

function onChannelSwitch(oldChannelId, newChannelId) {
   // gets called during initialization of the demo and on each channel switch

   if (oldChannelId) {

      currentSubscription.unsubscribe().then(
         function() {
            console.log("successful unsubscribe");
         },
         function(error) {
            console.log("unsubscribe error ", error);
         }
      );

   } else {

      // initial setup
      $("#pub_topic").val(newChannelId);
      $("#pub_topic_full").text(sess.resolve("api:" + newChannelId));

   }

   sess.subscribe("api:" + newChannelId, onNotification).then(
      function(subscription) {
         console.log("subscribe");
         currentSubscription = subscription;
      },
      function(error) {
         console.log("subscription error ", error);
      }
   );

   $('#new-window').attr('href', window.location.pathname + '?channel=' + newChannelId);
   $('#secondInstance').attr('href', window.location.pathname + '?channel=' + newChannelId);
   $("#sub_topic_full").text(sess.resolve("api:" + newChannelId));
}

function sendNotification () {
   sess.publish("api:" + $("#pub_topic").val(), [$("#notification_message").val()], {}, {exclude_me: false});
}

function onNotification(args, kwargs, details) {

   notificationCount += 1;

   // change Favicon
   Tinycon.setBubble(notificationCount);

   // display side-scrolling notification
   $("#webmqad_message").text(args[0]);
   toggle("emptyEvent", true);

}

// reset persistent state
function reset() {
   delete localStorage["webmq_ad_hidden"];
}

function countdown() {
   window.setTimeout(function() {
      if (ad_shown && ad_time_remaining > 0) {
         ad_time_remaining = ad_time_remaining - 1;
         ad_countdown.innerHTML = ad_time_remaining;

         if (ad_time_remaining > 0) {
            countdown();
         }
      }
   }, 1000);
}

function toggle(event, newNotification) {

   // if already displayed  & new notification, do nothing
   // P: this does not reset the counter on receiving additional notifications
   //    within an initial countdown period - FIXME
   if (newNotification && ad_shown) {
      return;
   }

   // toggle the slide in/out
   if (ad_shown) {
      ad.style.right = '-' + (ad_width + 25) + 'px';
      ad_shown = false;
      ad_countdown.style.visibility = 'hidden';
      // switch arrow to pointing left
      window.setTimeout(function() {
         ad.style.backgroundImage = "url('img/slide_in_left_arrow_d.png')";
      }, 500);

   } else {
      ad.style.right = '0px';
      ad_shown = true;
      // switch arrow to pointing right
      window.setTimeout(function() {
         ad.style.backgroundImage = "url('img/slide_in_right_arrow_d.png')";
      }, 500);
   }

   // if triggered based on a new notification,
   // start the countdown and hide after this
   if (newNotification) {
      ad_time_remaining = ad_time_to_hide;
      ad_countdown.innerHTML = ad_time_remaining;

      window.setTimeout(function() {
         if (ad_shown) {
            // slide out
            ad.style.right = '-' + (ad_width + 25) + 'px';
            ad_shown = false;
            ad_countdown.style.visibility = 'hidden';
            window.setTimeout(function() {
               ad.style.backgroundImage = "url('img/slide_in_left_arrow_d.png')";
            }, 500);
         }
      }, 1000 * ad_time_to_hide);

      ad_countdown = document.getElementById('webmqad_countdown');
      ad_countdown.style.visibility = 'visible';
      countdown();
   }
}
