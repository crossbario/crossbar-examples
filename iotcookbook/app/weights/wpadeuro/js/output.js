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

var demoRealm = "iot_cookbook";
var demoPrefix = "io.crossbar.examples";

var wsuri;
if (document.location.origin == "file://") {
   wsuri = "ws://127.0.0.1:8080/ws";

} else {
   wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws";
}

var session;
var windowUrl;
var isReconnect = false;

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

   connection.onopen = function (sess) {

      session = sess;

      setupDemo();

      updateStatusline("Connected to " + wsuri);

   };

   connection.onclose = function() {
      session = null;
      console.log("connection closed ", arguments);
   }

   connection.open();
}

$(document).ready(function()
{
   updateStatusline("Not connected.");

   connect();

});

var newWindowLink = null,
    currentSubscriptions = [],
    padGauges = [],
    sliders = null,
    isReconnect = false;

function setupDemo() {

   // session.prefix("api", demoPrefix + ".spreadsheet");

   if (isReconnect) {
      return;
   }
   isReconnect = true;

   var gaugeValues = [30, 20];
   // create and configure padGauges
   //

   padGauges.push(new JustGage({
      id: "g" + padGauges.length,
      value: gaugeValues[padGauges.length],
      min: 0,
      max: 1010,
      title: "Pad 1",
      label: "resistance"
   }));

   padGauges.push(new JustGage({
      id: "g" + padGauges.length,
      value: gaugeValues[padGauges.length],
      min: 0,
      max: 1010,
      title: "Pad 2",
      label: "resistance"
   }));


   for (var k = 0; k < padGauges.length; ++k) {
      (function (p) {
         session.subscribe("io.crossbar.examples.yun.weighingpad.converted_samples." + (k + 1), function (args, kwargs, details) {
            console.log("refresh", p, args[0]);
            padGauges[p].refresh(args[0]);
            $("#s" + p).slider({ value: args[0]});
         }).then(
            function(subscription) {
               console.log("subscribed ", "io.crossbar.examples.yun.weighingpad.converted_samples." + (k + 1), subscription);
               currentSubscriptions.push(subscription);
            },
            function(error) {
               console.log("unsubscribe failed ", error);
            }
         );
      })(k);
   }

   // set up the sum
   var sumGauge = new JustGage({
      id: "g2",
      value: 0,
      min: 0,
      max: 2020,
      title: "Sum of Pads",
      label: "???"
   });

   session.subscribe("io.crossbar.examples.yun.weighingpad.sum", function (args) {
      sumGauge.refresh(args[0]);
      if (args[0] > 800) {
         console.log("sumAlarm triggered");
         document.getElementById("sumAlarm").style.backgroundColor = "red";
      } else {
         console.log("sumAlarm cancelled");
         document.getElementById("sumAlarm").style.backgroundColor = "green";
      }
   })


   // set up the average
   var averageGauge = new JustGage({
      id: "g3",
      value: 0,
      min: 0,
      max: 1010,
      title: "Average of Pads",
      label: "???"
   });

   session.subscribe("io.crossbar.examples.yun.weighingpad.average", function (args) {
      averageGauge.refresh(args[0]);
   })

   // get initial values and apply these
   var cells = [[4,0], [5,0], [7,0], [10,0]];
   session.call("io.crossbar.examples.yun.weighingpad.get_values", cells).then(function (res) {
      console.log("get_values", res, res.length);
      padGauges[0].refresh(res[0]);
      padGauges[1].refresh(res[1]);
      sumGauge.refresh(res[2]);
      averageGauge.refresh(res[3]);
   }, session.log);

}
