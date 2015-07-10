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


// function randomChannelId() {
//    var id = "";
//    for (var i = 0; i < _idlen; i += 1) {
//       id += _idchars.charAt(Math.floor(Math.random() * _idchars.length));
//    }
//    return id;
// };

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

   // check for demo setup data in the URL
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
   console.log("controllerChannelId", controllerChannelId);

   connect();

});

var newWindowLink = null,
    currentMasterSubscription = null,
    currentEqSubscription = null,
    isReconnect = false;


function setupDemo() {

   sess.prefix("api", demoPrefix + ".spreadsheet");

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

   sess.subscribe("api:" + controllerChannelId + ".master", onMaster).then(
      function(subscription) {
         currentMasterSubscription = subscription;
      },
      function(error) {
         console.log("subscription failed ", error);
      }
   );

   sess.subscribe("api:" + controllerChannelId + ".eq", onEq).then(
      function(subscription) {
         currentEqSubscription = subscription;
      },
      function(error) {
         console.log("subscription failed ", error);
      }
   );

   // get the initial values
   var cells = [[2,0], [4,0], [5,0], [6,0], [7,0], [8,0], [9,0], [10,0]];
   sess.call("api:" + controllerChannelId + ".get_values", cells).then(function (res) {
      console.log("get_values", res, res.length);
      // handle the master 
      $("#master").slider({
         value: res[0]
      });
      res.shift();
      console.log("res.length", res.length);
      // handle the eqs
      res.forEach(function(val, i) {
         console.log("it", i);
          $("#eq span:nth-child(" + ( i + 1 ) + ")").slider({
            value: val
         });
      });
   }, sess.log);
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
