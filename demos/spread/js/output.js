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

var demoRealm = "crossbardemo";
var demoPrefix = "io.crossbar.demo";

var wsuri;
if (document.location.origin == "file://") {
   wsuri = "ws://127.0.0.1:8080/ws";

} else {
   wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws";
}

var sess;
var windowUrl;
var isReconnect = false;

var _idchars = "0123456789";
var _idlen = 6;
var _idpat = /^\d*$/;


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


function updateStatusline(status) {
   $(".statusline").text(status);
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

   connection.onopen = function (session) {

      sess = session;

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
      controllerChannelId = setupInfoDictionary.channel;
   }

   connect();

});

var newWindowLink = null,
    currentSubscriptions = [],
    gauges = [],
    sliders = null,
    isReconnect = false;

function setupDemo() {

   sess.prefix("api", demoPrefix + ".spreadsheet");

   if (isReconnect) {
      return;
   }
   isReconnect = true;

   newWindowLink = document.getElementById('secondInstance');

   var gaugeValues = [30, 20];
   // create and configure gauges
   //

   gauges.push(new JustGage({
      id: "g" + gauges.length,
      value: gaugeValues[gauges.length],
      min: 0,
      max: 700,
      title: "Gauge 1",
      label: "total"
   }));

   gauges.push(new JustGage({
      id: "g" + gauges.length,
      value: gaugeValues[gauges.length],
      min: 0,
      max: 100,
      title: "Gauge 2",
      label: "average"
   }));


   for (var k = 0; k < gauges.length; ++k) {
      (function (p) {
         // sess.subscribe("api:" + controllerChannelId + ".g" + p, function (args, kwargs, details) {
         sess.subscribe("api:" + controllerChannelId + ".g" + p, function (args, kwargs, details) {
            console.log("refresh", p, args[0]);
            gauges[p].refresh(args[0]);
            $("#s" + p).slider({ value: args[0]});
         }).then(
            function(subscription) {
               console.log("subscribed ", "api:" + controllerChannelId, subscription);
               currentSubscriptions.push(subscription);
            },
            function(error) {
               console.log("unsubscribe failed ", error);
            }
         );
      })(k);
   }

   // get initial values and apply these
   var cells = [[12,0], [13,0]];
   sess.call("api:" + controllerChannelId + ".get_values", cells).then(function (res) {
      console.log("get_values", res, res.length);
      gauges[0].refresh(res[0]);
      gauges[1].refresh(res[1]);
   }, sess.log);

}
