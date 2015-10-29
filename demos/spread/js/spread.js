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

   // Ticker
   sheet.getCell(0, 0).value(0);
   sheet.getCell(0, 1).text("Ticks");
   var ticks = 0;
   window.setInterval(function () {
      ticks += 1;
      sheet.getCell(0, 0).value(ticks);
   }, 1000);

   // create random channel
   // change the URI - we want this separated
   var channel = parseInt(Math.random() * 1000000);
   // var slidersbaseUri = "io.crossbar.demo.sliders.123456.";
   var controllerBaseUri = "io.crossbar.demo.spreadsheet." + channel + ".";

   // set up link for control sliders
   var controllerLink = document.getElementById("controllerLink");
   controllerLink.href = "controller.html?channel=" + channel;

   var outputLink = document.getElementById("outputLink");
   outputLink.href = "output.html?channel=" + channel;


   // Master volume
   sheet.getCell(2, 0).value(0);
   sheet.getCell(2, 1).text("Single");
   session.subscribe(controllerBaseUri + "master", function (args, kwargs, details) {
      sheet.getCell(2, 0).value(args[0]);
   });

   // Graphic EQ
   for (var i = 1; i < 8; ++i) {
      sheet.getCell(3 + i, 0).value(0);
      sheet.getCell(3 + i, 1).text("Set-" + i);
   }
   session.subscribe(controllerBaseUri + "eq", function (args, kwargs, details) {
      sheet.getCell(3 + args[0].idx, 0).value(args[0].val);
   });

   // Create some formulas
   sheet.getCell(12, 1).text("Set Sum");
   sheet.getCell(12, 0).formula("=SUM(A5:A12)");
   sheet.getCell(13, 1).text("Set Avg.");
   sheet.getCell(13, 0).formula("=ROUND(AVERAGE(A5:A12); 1)");
   // sheet.getCell(13, 2).text("test");
   sheet.getCell(12, 2).formula('=PUBLISH("io.crossbar.demo.spreadsheet.' + channel + '.g0", A13)');
   sheet.getCell(13, 2).formula('=PUBLISH("io.crossbar.demo.spreadsheet.' + channel + '.g1", A14)');

   setupCustomFuns();

   spread.isPaintSuspended(false);


   // allow request of current data
   session.register(controllerBaseUri + "get_values", function (cellArr) {
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
