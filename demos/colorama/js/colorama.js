/******************************************************************************
 *
 *  Copyright 2016 Tavendo GmbH.
 *
 *  Licensed under the Apache 2.0 license
 *  http://www.apache.org/licenses/LICENSE-2.0.html
 *
 ******************************************************************************/

"use strict";

// the URL of the WAMP Router (Crossbar.io)
var wsuri;
if (document.location.origin == "file://") {
   wsuri = 'wss://demo.crossbar.io/ws';

} else {
   wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws";
}

var httpUri;

if (document.location.origin == "file://") {
   httpUri = "https://demo.crossbar.io/lp";

} else {
   httpUri = (document.location.protocol === "http:" ? "http:" : "https:") + "//" +
               document.location.host + "/lp";
}

var connection = null;
var sess = null;

function updateStatusline(status) {
   $(".statusline").html(status);
};


$(document).ready(function()
{
   updateStatusline("Not connected.");

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

      setupDemo();

      if (details.x_cb_node_id) {
         updateStatusline("Connected to node <strong>" + details.x_cb_node_id + "</strong> at " + wsuri);
      } else {
         updateStatusline("Connected to " + wsuri);
      }

      if(typeof(afterAuth) !== "undefined" ) {
         afterAuth(); // only exists in colorpicker demo
      }
   };

   connection.onclose = function(reason, details) {
      sess = null;
      console.log("connection closed ", reason, details);

       if (details.will_retry) {
         updateStatusline("Trying to reconnect in " + parseInt(details.retry_delay) + " s.");
      } else {
         updateStatusline("Disconnected");
      }
   }

   connection.open();
});



function setupDemo() {
   // setup the color pickers
   var colorPickersCount = 2; // total number of color pickers as contained in the HTML
   for (var i = 0; i < colorPickersCount; ++i) {
      setupPicker(i);
   }

   $("#helpButton").click(function() { $(".info_bar").toggle() });

   sess.subscribe("io.crossbar.demo.colorama.color_change", onColorChangeRemote);
}


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
   $('#picker' + k).farbtastic(

      // this is the callback fired when the user manipulates a color picker
      function onColorChangeLocal(color) {

         // set colors associated with color picker
         setExtraColors(k, color);

         // publish the color change event on our topic
         sess.publish("io.crossbar.demo.colorama.color_change", [{ index: k, color: color }]);
      }
   )
}


// our event handler for processing remote color changes
function onColorChangeRemote(args, kwargs, details) {
   // set color in color picker
   $.farbtastic('#picker' + args[0].index).setColor(args[0].color, true);

   // set colors associated with color picker
   setExtraColors(args[0].index, args[0].color);
};
