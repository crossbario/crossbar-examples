/******************************************************************************
 *
 *  Copyright 2012-2013 Tavendo GmbH.
 *
 *  Licensed under the Apache 2.0 license
 *  http://www.apache.org/licenses/LICENSE-2.0.html
 *
 ******************************************************************************/

var session = null;
var toggleRandomDataSendButton = null;

$(document).ready(function()
{
   updateStatusline("Not connected.");

   setupDemo();

   connect();
});

function connect() {

   var demoPrefix = "io.crossbar.demo.dashboard";

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

   connection.onopen = function (sess) {

      session = sess;

      updateStatusline("Connected to " + wsuri + " in session " + session.id);

      /** define session prefixes ***/
      session.prefix("sales", "io.crossbar.demo.dashboard");

      /** subscribe to events ***/
      session.subscribe("sales:revenue", onEqTr);
      session.subscribe("sales:revenue-by-product", onEqRbp);
      session.subscribe("sales:revenue-by-region", onEqUbp);
      session.subscribe("sales:asp-by_region", onEqAbr);
      session.subscribe("sales:units-by-product", onEqRbr);
   };


   connection.onclose = function(reason, details) {
      session = null;
      updateStatusline(reason);
      console.log("connection closed ", arguments);
   };

   connection.open();
}


function updateStatusline(status) {
   $(".statusline").text(status);
};


function setupDemo() {

   // Total Revenue Sliders

   var i = 1;

   $( "#eq_tr > span" ).each(function() {
      // read initial values from markup and remove that
      var value = parseInt( $( this ).text(), 10 );
      var k = i;

      $( this ).empty().slider({
         value: value,
         range: "min",
         animate: true,
         orientation: "vertical",

         slide: function(event, ui) {
            session.publish("sales:revenue", [], { idx: k, val: ui.value });
         }
      });
      i += 1;
   });


   // Revenue by Product Sliders

   var n = 1;

   $( "#eq_rbp > span" ).each(function() {
      // read initial values from markup and remove that
      var value = parseInt( $( this ).text(), 10 );
      var k = n;

      $( this ).empty().slider({
         value: value,
         range: "min",
         animate: true,
         orientation: "vertical",

         slide: function(event, ui) {
            // console.log("ui " + k + " val: ", ui.value);
            session.publish("sales:revenue-by-product", [], { idx: k, val: ui.value });
         }
      });
      n += 1;
   });


   // Units by Product Sliders

   var s = 1;

   $("#eq_ubp > span").each(function() {
      // read initial values from markup and remove that
      var value = parseInt($(this).text(), 10);
      var k = s;

      $(this).empty().slider({
         value: value,
         range: "min",
         animate: true,
         orientation: "vertical",

         slide: function(event, ui) {
            session.publish("sales:units-by-product", [], { idx: k, val: ui.value });
         }
      });
      s += 1;
   });


   // ASP by Region Sliders

   var t = 1;

   $("#eq_abr > span").each(function() {
      // read initial values from markup and remove that
      var value = parseInt($(this).text(), 10);
      var k = t;

      $(this).empty().slider({
         value: value,
         range: "min",
         animate: true,
         orientation: "vertical",

         slide: function(event, ui) {
            session.publish("sales:asp-by-region", [], { idx: k, val: ui.value });
         }
      });
      t += 1;
   });


   // Revenue by Region Sliders

   var u = 1;

   $("#eq_rbr > span").each(function() {
      // read initial values from markup and remove that
      var value = parseInt($(this).text(), 10);
      var k = u;

      $(this).empty().slider({
         value: value,
         range: "min",
         animate: true,
         orientation: "vertical",

         slide: function(event, ui) {
            session.publish("sales:revenue-by-region", [], { idx: k, val: ui.value });
         }
      });
      u += 1;
   });

   $("#helpButton").click(function() { $(".info_bar").toggle() });

   toggleRandomDataSendButton =  document.getElementById("toggleRandomDataSend");
   toggleRandomDataSendButton.addEventListener("click", toggleRandomDataSend);
}

function send_activity() {

   var data = {};

   data.product = document.getElementById("product_select").value;
   data.units = document.getElementById("units").value;
   data.region = document.getElementById("region_select").value;
   data.revenue = document.getElementById("revenue").value;

   session.publish("sales:sale", [], data);
}

function switch_dashboard(number) {
   session.publish("sales:switch-dashboard", [number]);
}

var randomDataSend = false;
function toggleRandomDataSend () {
   randomDataSend = !randomDataSend;

   if (randomDataSend) {
      sendRandomData();
      toggleRandomDataSendButton.innerHTML = "Stop";
   } else {
      toggleRandomDataSendButton.innerHTML = "Start";
   } 
}

var products = ["Product A", "Product B", "Product C"];
var regions = ["North", "East", "South", "West"];

function sendRandomData () {

   // only do something if randomDataSend not toggled to off
   if (randomDataSend) {
      // pick which kind of data to send
      var dataCategories = ["revenue", "revenue-by-product", "units-by-product", "asp-by-region", "revenue-by-region", "sale"];
      var currentCategory = dataCategories[Math.floor(Math.random() * dataCategories.length)];

      // generate the event data for the category
      var event = {};
      switch (currentCategory) {
      
         case "revenue":
            var revenue = Math.floor(Math.random() * 100);
            event = { idx: 1, val: revenue};
            break;
      
         case "revenue-by-product":
         case "units-by-product":
            var product = Math.floor(Math.random() * 4);
            var value = Math.floor(Math.random() * 100);
            event = { idx: product, val: value };
            break;
      
         case "asp-by-region":
         case "revenue-by-region":
            var region = Math.floor(Math.random() * 5);
            var value = Math.floor(Math.random() * 100);
            event = { idx: region, val: value };
            break;
      
         case "sale":
            var product = products[Math.floor(Math.random() * 4)];
            var region = regions[Math.floor(Math.random() * 5)];
            var units = Math.floor(Math.random() * 100);
            var revenue = Math.floor(Math.random() * 50) * units;
            event = {product: product, region: region, units: units, revenue: revenue};
            break;
      
         default:
            console.log("unknown event category", currentCategory);
            break;
      }

      // send event
      session.publish("sales:" + currentCategory, [], event);

      // pick when sendRandomData is next called
      var maxInterval = 300;
      var minInterval = 1;
      var nextCallInterval = Math.floor(Math.random() * (maxInterval - minInterval) + minInterval);
      setTimeout(sendRandomData, nextCallInterval);
   }
   
}


// Set slider positions on remote value changes, e.g. when using multiple control boards

function onEqTr(topicUri, event) {

   $("#eq_tr span:nth-child(" + event.idx + ")").slider({
      value: event.val
   });
}

function onEqRbp(topicUri, event) {

   $("#eq_rbp span:nth-child(" + event.idx + ")").slider({
      value: event.val
   });
}

function onEqUbp(topicUri, event) {

   $("#eq_ubp span:nth-child(" + event.idx + ")").slider({
      value: event.val
   });
}

function onEqAbr(topicUri, event) {

   $("#eq_abr span:nth-child(" + event.idx + ")").slider({
      value: event.val
   });
}

function onEqRbr(topicUri, event) {

   $("#eq_rbr span:nth-child(" + event.idx + ")").slider({
      value: event.val
   });
}
