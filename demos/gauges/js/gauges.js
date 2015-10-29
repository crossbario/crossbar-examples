/******************************************************************************
 *
 *  Copyright 2012-2014 Tavendo GmbH.
 *
 *                                Apache License
 *                          Version 2.0, January 2004
 *                       http://www.apache.org/licenses/
 *
 ******************************************************************************/

/* global document: false, console: false, ab: true, $: true, JustGage: false, getRandomInt: false */

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

var newWindowLink = null,
    currentSubscriptions = [],
    gauges = [],
    sliders = null,
    isReconnect = false;

function setupDemo() {

   sess.prefix("api", demoPrefix + ".gauges");

   if (isReconnect) {
      return;
   }
   isReconnect = true;

   newWindowLink = document.getElementById('secondInstance');

   var gaugeValues = [30, 20, 40, 60];
   // create and configure gauges
   //

   gauges.push(new JustGage({
      id: "g" + gauges.length,
      value: gaugeValues[gauges.length],
      min: 0,
      max: 100,
      title: "Big Fella",
      label: "pounds"
   }));

   gauges.push(new JustGage({
      id: "g" + gauges.length,
      value: gaugeValues[gauges.length],
      min: 0,
      max: 100,
      title: "Small Buddy",
      label: "oz"
   }));

   gauges.push(new JustGage({
      id: "g" + gauges.length,
      value: gaugeValues[gauges.length],
      min: 0,
      max: 100,
      title: "Tiny Lad",
      label: "oz"
   }));

   gauges.push(new JustGage({
      id: "g" + gauges.length,
      value: gaugeValues[gauges.length],
      min: 0,
      max: 100,
      title: "Little Pal",
      label: "oz"
   }));



   // auto-animate gauges
   //
   if (false) {
      setInterval(function () {
         for (var j = 0; j < gauges.length; ++j) {
            gauges[j].refresh(getRandomInt(0, 100));
         }
      }, 2500);
   }


   // instantiate sliders
   $("#s0").slider({
      value: gaugeValues[0],
      orientation: "horizontal",
      range: "min",
      animate: true
   });

   var i = 1;

   $("#eqSliders > span").each(function() {
      // read initial values from markup and remove that
      // var value = parseInt($(this).text(), 10);
      var k = i;

      $(this).empty().slider({
         value: gaugeValues[i],
         range: "min",
         animate: true,
         orientation: "vertical"
      });
      i += 1;
   });

   // store sliders in array
   // sliders = [$("#s0")[0], $("#s1")[0], $("#s2")[0], $("#s3")[0]];
}

function onChannelSwitch(oldChannelId, newChannelId) {
   console.log("onChannelSwitch");

   // unsubscribe
   if (oldChannelId) {
      currentSubscriptions.forEach( function (el, index, array) {
         el.unsubscribe().then(
            function() {
               console.log("unsubscribed");
            },
            function(error) {
               console.log("unsubscribe failed", error);
            }
         );
      });
   }

   // wire up gauges + sliders for PubSub events
   //

   for (var k = 0; k < gauges.length; ++k) {
      (function (p) {
         sess.subscribe("api:" + newChannelId + ".g" + p, function (args, kwargs, details) {
            console.log("refresh", p, args[0]);
            gauges[p].refresh(args[0]);
            $("#s" + p).slider({ value: args[0]});
         }).then(
            function(subscription) {
               console.log("subscribed ", "api:" + newChannelId, subscription);
               currentSubscriptions.push(subscription);
            },
            function(error) {
               console.log("unsubscribe failed ", error);
            }
         );
      })(k);
   }

   // update publish for the sliders
   $("#s0").slider({
      slide: function(event, ui) {
         sess.publish("api:" + newChannelId + ".g0", [ui.value], {}, {acknowledge: true, exclude_me: false}).then(
            function(publication) {
               console.log("gauges published ", publication);
            },
            function(error) {
               console.log("gauges publish failed ", error);
            }
         );
      }
   });


   var i = 1;
   $("#eqSliders > span").each(function() {
      // read initial values from markup and remove that
      // var value = parseInt($(this).text(), 10);
      var k = i;

      $(this).slider({

         slide: function(event, ui) {
            sess.publish("api:" + newChannelId + ".g" + k, [ui.value], {}, {acknowledge: true, exclude_me: false}).then(
               function(publication) {
                  console.log("gauges published ", publication);
               },
               function(error) {
                  console.log("gauges publish failed ", error);
               }
            );
         }
      });
      i += 1;
   });


   newWindowLink.setAttribute('href', window.location.pathname + '?channel=' + newChannelId);
}
