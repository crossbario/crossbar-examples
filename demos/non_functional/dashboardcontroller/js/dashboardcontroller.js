/******************************************************************************
 *
 *  Copyright 2012-2013 Tavendo GmbH.
 *
 *  Licensed under the Apache 2.0 license
 *  http://www.apache.org/licenses/LICENSE-2.0.html
 *
 ******************************************************************************/

var session = null;

$(document).ready(function()
{
   updateStatusline("Not connected.");

   setupDemo();

   connect();
});

function connect() {

   // turn on WAMP debug output
   // ab.debug(true, false, false);

   // use jQuery deferreds
   ab.Deferred = $.Deferred;

   // Connect to Crossbar.io ..
   //
   ab.launch(
      // WAMP app configuration
      {
         // Crossbar.io server URL
         wsuri: ab.getServerUrl("ws", "ws://127.0.0.1:8080/ws"),
         // authentication info
         appkey: null, // authenticate as anonymous
         appsecret: null,
         appextra: null,
         // additional session configuration
         sessionConfig: {maxRetries: 10,
                         sessionIdent: "Vote"}
      },
      // session open handler
      function (newSession) {
         session = newSession;
         updateStatusline("Connected to " + session.wsuri() + " in session " + session.sessionid());
         retryCount = 0;

         /** define session prefixes ***/
         session.prefix("sales", "http://crossbar.io/crossbar/demo/dashboard#");

         /** subscribe to events ***/
         session.subscribe("sales:revenue", onEqTr);
         session.subscribe("sales:revenue-by-product", onEqRbp);
         session.subscribe("sales:revenue-by-region", onEqUbp);
         session.subscribe("sales:asp-by_region", onEqAbr);
         session.subscribe("sales:units-by-product", onEqRbr);
      },
      // session close handler
      function (code, reason, detail) {
         session = null;
         updateStatusline(reason);
      }
   );
}


function updateStatusline(status) {
   $(".statusline").text(status);
};

var channelBaseUri = "http://crossbar.io/crossbar/demo/sliders/";

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
            session.publish("sales:revenue", { idx: k, val: ui.value });
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
            session.publish("sales:revenue-by-product", { idx: k, val: ui.value });
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
            session.publish("sales:units-by-product", { idx: k, val: ui.value });
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
            session.publish("sales:asp-by-region", { idx: k, val: ui.value });
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
            session.publish("sales:revenue-by-region", { idx: k, val: ui.value });
         }
      });
      u += 1;
   });

   $("#helpButton").click(function() { $(".info_bar").toggle() });
}

function send_activity() {

   var data = {};

   data.product = document.getElementById("product_select").value;
   data.units = document.getElementById("units").value;
   data.region = document.getElementById("region_select").value;
   data.revenue = document.getElementById("revenue").value;

   session.publish("sales:sale", data);
}

function switch_dashboard(number) {
   session.publish("sales:switch-dashboard", number);
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
