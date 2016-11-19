/******************************************************************************
 *
 *  Copyright 2016 Tavendo GmbH.
 *
 *  Licensed under the Apache 2.0 license
 *  http://www.apache.org/licenses/LICENSE-2.0.html
 *
 ******************************************************************************/

"use strict";

// serial numbers from IoT Starterkit devices
//var devices_serials = [1307984267, 3711643271];
var devices_serials = [3623412118, 3711643271];

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

   for (var i = 0; i < devices_serials.length; ++i) {
      (function (k) {
         sess.call('io.crossbar.demo.iotstarterkit.' + devices_serials[k] + '.pixelstrip.get_color', [0]).then(
            function (res) {
               set_col(devices_serials[k], res);
            },
            function (err) {
               console.log("could not get color:", err);
            }
         );
      })(i);
   }

   sess.subscribe('io.crossbar.demo.iotstarterkit..pixelstrip.on_color_set', onColorChangeRemote, {match: 'wildcard'}).then(
      null,
      function (err) {
         console.log("failed to subscribe:", err);
      }
   );
}

function action (k, action_name) {
   sess.call('io.crossbar.demo.iotstarterkit.' + devices_serials[k] + '.pixelstrip.' + action_name).then(
      null,
      function (err) {
         console.log("could not perform action on LEDs:", err);
      }
   );
}

function color_components (color) {
   var c = JSON.stringify(color);
   c = c.substring(2, 8);
   var red = parseInt(c.substring(0, 2), 16);
   var green = parseInt(c.substring(2, 4), 16);
   var blue = parseInt(c.substring(4, 6), 16);
   return [red, green, blue];
   //return {red: red, green: green, blue: blue};
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
      function (color) {

         var color_rgb = color_components(color);

         sess.call('io.crossbar.demo.iotstarterkit.' + devices_serials[k] + '.pixelstrip.set_color', color_rgb).then(
            null,
            function (err) {
               console.log("could not set color:", err);
            }
         );
      }
   )
}

function set_col(serial, col_ev) {
      var serial_index = null;
      for (var i = 0; i < devices_serials.length; ++i) {
         if (devices_serials[i] === serial) {
            serial_index = i;
            break;
         }
      }

      var color = 'rgba(' + col_ev.r + ', ' + col_ev.g + ', ' + col_ev.b + ', 1)';

      // set color in color picker
      $.farbtastic('#picker' + serial_index).setColor(color, true);

      // set colors associated with color picker
      setExtraColors(serial_index, color);
}

// our event handler for processing remote color changes
function onColorChangeRemote(args, kwargs, details) {
   var col_ev = args[0];
   if (col_ev.led == 0) {
      // "io.crossbar.demo.iotstarterkit.1307984267.pixelstrip.on_color_set"
      var serial = parseInt(details.topic.split('.')[4]);

      set_col(serial, col_ev);
   }
};
