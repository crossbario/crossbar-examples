/******************************************************************************
 *
 *  Copyright 2013-2014 Tavendo GmbH.
 *
 *  Licensed under the Apache 2.0 license
 *  http://www.apache.org/licenses/LICENSE-2.0.html
 *
 ******************************************************************************/

/* global document: false, console: false, ab: true, $: true */

"use strict";

var session = null;
var spread = null;
var sheet = null;


$(document).ready(function() {
   start();
});


function start() {

   // create wijspread control
   $("#ss").wijspread({sheetCount: 1});

   // get instance of wijspread control
   spread = $("#ss").wijspread("spread");

   // get active worksheet of the wijspread control
   sheet = spread.getActiveSheet();

   var wsuri;

   if (document.location.protocol === "file:") {
      wsuri =  "ws://127.0.0.1:8080/ws";
   } else {
      var scheme = document.location.protocol === 'https:' ? 'wss://' : 'ws://';
      var port = document.location.port !== "" ? ':' + document.location.port : '';
      wsuri = scheme + document.location.hostname + port + "/ws";
   }

   var connection = new autobahn.Connection({
      url: wsuri,
      realm: 'iot_cookbook',
      max_retries: 30,
      initial_retry_delay: 2
      }
   );

   connection.onopen = function (newSession) {
      session = newSession;

      console.log("connected");

      updateStatusline("Connected to " + wsuri);

      main(session);

   };

   connection.onclose = function() {
      session = null;
      console.log("connection closed ", arguments);
      updateStatusline("Not connected");
   }

   connection.open();
}


function updateStatusline(status) {
   $(".statusline").text(status);
};

function main (session) {

   spread.isPaintSuspended(true);

   sheet.getColumn(0).locked(false);
   sheet.getColumn(1).locked(false);
   sheet.getColumn(2).locked(false);
   sheet.getColumn(3).locked(false);
   sheet.getColumn(4).locked(false);

   // Set up the raw sample value cells + conversion factors + publication of converted values
   var maxResistance = 1010;
   var pins = {1: [4, 0], 2: [5, 0]};
   var firstLine = 0;
   var lastLine = 0;

   for (var pin in pins) {
      if (pins.hasOwnProperty(pin)) {   
         
         // raw values
         sheet.getCell(pins[pin][0], pins[pin][1]).value(0);
         sheet.getCell(pins[pin][0], 1).text("Pad on Pin " + pin);
         
         // conversion factor
         sheet.getCell(pins[pin][0], 3).value(1);
         sheet.getCell(pins[pin][0], 4).text("Conversion factor");

         // publish converted values
         var sourceCell = "A" + (pins[pin][0] + 1);
         var conversionCell = "D" + (pins[pin][0] + 1);
         sheet.getCell(pins[pin][0], 6).formula('=PUBLISH("io.crossbar.examples.yun.weighingpad.converted_samples.' + pin + '",'  +  sourceCell + ' * ' + conversionCell);

         if (pins[pin][0] < firstLine) {
            firstLine = pins[pin][0];
         } 
         if (pins[pin][0] > lastLine) {
            lastLine = pins[pin][0];
         }
      }
   }

   // Set up the sum & average fields and publishing these values
   var sumCell = ("A" + (lastLine + 3));
   sheet.getCell(lastLine + 2, 0).formula('=SUM(A' + (firstLine + 1) + ":A" + (lastLine + 1) + ")");
   sheet.getCell(lastLine + 2, 1).text("Sum");
   sheet.getCell(lastLine + 2, 3).formula('=PUBLISH("io.crossbar.examples.yun.weighingpad.sum",'  +  sumCell);

   var averageCell = ("A" + (lastLine + 6));
   sheet.getCell(lastLine + 5, 0).formula('=ROUND(AVERAGE(A' + (firstLine + 1) + ":A" + (lastLine + 1) + "); 1)");
   sheet.getCell(lastLine + 5, 1).text("Average");
   sheet.getCell(lastLine + 5, 3).formula('=PUBLISH("io.crossbar.examples.yun.weighingpad.average",'  +  averageCell);



   // Subscribe to pads
   session.subscribe("io.crossbar.examples.yun.weighingpad.on_sample", function (args) {
      var data = args[0];
      var samples = data.samples;
      for (var pin in samples) {
         if (samples.hasOwnProperty(pin)) {
            console.log("pin " + pin + " value " + samples[pin]);
            sheet.getCell(pins[pin][0], pins[pin][1]).value(maxResistance - samples[pin]);
         }
      }
   })

   setupCustomFuns();

   spread.isPaintSuspended(false);

   // allow request of current data so that output components may display these on initialization
   session.register("io.crossbar.examples.yun.weighingpad.get_values", function (cellArr) {
      var values = [];

      cellArr.forEach(function(el) {
         values.push(sheet.getValue(el[0], el[1]));
      })

      return values;
   });
}

var subs = {};
var pubs = {};
var subIdsToUris = {};
var pubIdsToUris = {};

function setupCustomFuns () {

   // create custom SUBSCRIBE spreadsheet function
   var sub = $.ce.createFunction("SUBSCRIBE", function (args) {

      var uri = args[0];

      if (subs[uri] !== undefined) {

         return subs[uri];

      } else {

         var row = sheet.getActiveRowIndex();
         var col = sheet.getActiveColumnIndex();

         subs[uri] = 0;

         session.subscribe(uri, function (args, kwargs, details) {
            console.log("subscription evt received", args, kwargs, details, uri);
            subs[uri] = args[0];

            spread.isPaintSuspended(true);

            var cell = sheet.getCell(row, col);
            cell.value(args[0]);

            spread.isPaintSuspended(false);

            sheet.repaint();
         }).then(
            function(subscription) {
               console.log("custom subscription", subscription, uri);
               // no allowing unsubscribe, so do nothing with the received object
            },
            function(error) {
               console.log("subscription error custom subscription", error);
            }
         );

         return subs[uri];
      }

   }, {minArg: 1, maxArg: 1});

   spread.addCustomFunction(sub);


   // create custom PUBLISH spreadsheet function
   var pub = $.ce.createFunction("PUBLISH", function (args) {

      var uri = args[0];
      var evt = args[1];

      if (pubs[uri] !== undefined && pubs[uri] === evt) {

         console.log("PUBLISH", "Value already published");

      } else {

         pubs[uri] = evt;
         session.publish(uri, [evt]);
         return evt;
      }

   }, {minArg: 2, maxArg: 2});

   spread.addCustomFunction(pub);


   // this is how to listen on cell changes
   if (false) {
      spread.bind($.wijmo.wijspread.Events.CellChanged, function (event, data) {
         console.log(data.col);
         console.log(data.row);
         console.log(data);
         var cell = sheet.getCell(data.row, data.col);
         console.log(cell);
         console.log(cell.value());
      });
   }
}
