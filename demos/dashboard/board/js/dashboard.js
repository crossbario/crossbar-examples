/******************************************************************************
 *
 *  Copyright 2012-2013 Tavendo GmbH.
 *
 *  Licensed under the Apache 2.0 license
 *  http://www.apache.org/licenses/LICENSE-2.0.html
 *
 ******************************************************************************/

// highlight timer objects

var highlight_timeout = 300;

var simple_timer = {};
simple_timer.targetClass = ".simple_indicator";
simple_timer.highlighted = false;
simple_timer.timeout = highlight_timeout;

var bars_timer = {};
bars_timer.targetClass = ".bar_chart";
bars_timer.highlighted = false;
bars_timer.timeout = highlight_timeout;

var hundred_timer = {};
hundred_timer.targetClass = ".hundred_bar";
hundred_timer.highlighted = false;
hundred_timer.timeout = highlight_timeout;

var bullet_timer = {};
bullet_timer.targetClass = ".bullet_graph";
bullet_timer.highlighted = false;
bullet_timer.timeout = highlight_timeout;

var pie_timer = {};
pie_timer.targetClass = ".pie_chart";
pie_timer.highlighted = false;
pie_timer.timeout = highlight_timeout;

var activity_timer = {};
activity_timer.targetClass = ".activity_stream";
activity_timer.highlighted = false;
activity_timer.timeout = highlight_timeout;


// initial thresholds for display in the activity stream
var revenue_threshold = 0;
var unit_threshold = 0;


// colors for the widgets

// var themeColors = ["rgb(185, 96, 96)", "rgb(83, 38, 38)", "rgb(214, 165, 165)", "rgb(160, 18, 18)"];
var themeColors = ["rgb(120, 120, 120)", "rgb(100, 100, 100)", "rgb(80, 80, 80)", "rgb(60, 60, 60)"];

// pie chart sections
var chartColor01 = themeColors[0];
var chartColor02 = themeColors[1];
var chartColor03 = themeColors[2];
var chartColor04 = themeColors[3];

// bar chart bars
var barColor01 = themeColors[0];
var barColor02 = themeColors[1];
var barColor03 = themeColors[2];

// hundred bar sections
var hundredColor01 = themeColors[0];
var hundredColor02 = themeColors[1];
var hundredColor03 = themeColors[2];

// bullet graph section
var bulletColor01 = themeColors[0];
var bulletColor02 = themeColors[1];
var bulletColor03 = themeColors[2];
var bulletColor04 = themeColors[3];

var session = null;
// makes the values within the DashboardViewModel accessible from outside the model
var vm = new DashboardViewModel();

$(document).ready(function() {
   updateStatusline("Not connected.");

   // set up knockout.js view model
   ko.applyBindings(vm);  

   // Connect to Crossbar.io ..
   //
   var demoRealm = "crossbardemo";
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

      console.log("connected");

      // main(session);
      updateStatusline("Connected to " + wsuri + " in session " + session.id);

      ///** define session prefixes ***/
      session.prefix("event", demoPrefix);
      session.prefix("sales", demoPrefix);


      // subscribe to events
      session.subscribe("event:switch-dashboard", onDashboardSwitch);

      // sales events
      session.subscribe("sales:revenue", onRevenue);
      session.subscribe("sales:revenue-by-product", onRevenueByProduct);
      session.subscribe("sales:units-by-product", onUnitsByProduct);
      session.subscribe("sales:revenue-by-region", onRevenueByRegion);
      session.subscribe("sales:asp-by-region", onAspByRegion);
      session.subscribe("sales:sale", onSale);

      session.subscribe("sales:revenue-threshold", onRevenueThresholdChanged);
      session.subscribe("sales:unit-threshold", onUnitThresholdChanged);

      onDashboardSwitch([1]);

      // // Oracle Dashboard Demo
      // session.prefix("orasales", "io.crossbar.demo.dashboard");

      // // sales events
      // session.subscribe("orasales:totalRevenue", onRevenue);
      // session.subscribe("orasales:revenueByProduct", onRevenueByProduct);
      // session.subscribe("orasales:unitsByProduct", onUnitsByProduct);
      // session.subscribe("orasales:revenueByRegion", onRevenueByRegion);
      // session.subscribe("orasales:aspByRegion", onAspByRegion);
      // session.subscribe("orasales:onSale", onSale);

      // session.subscribe("orasales:revenue-threshold", onRevenueThresholdChanged);
      // session.subscribe("orasales:unit-threshold", onUnitThresholdChanged);

      initialize();

      console.log("post-initialize");

   };

   connection.onclose = function(reason, details) {
      session = null;
      updateStatusline(reason);
      console.log("connection closed ", arguments);
   }

   connection.open();

})

function initialize() {

   console.log("initialize called");

   // set up the sliders for the activity stream
   $("#revenue_threshold").slider({
      value: 0,
      orientation: "horizontal",
      range: "min",
      animate: true
   });

   $("#unit_threshold").slider({
      value: 0,
      orientation: "horizontal",
      range: "min",
      animate: true
   });

   $("#revenue_threshold").slider({
      slide: function(event, ui) {
         revenue_threshold = parseInt(ui.value * 100);
         $(".revenue_threshold_value").text(thousand_formatted(revenue_threshold));
         session.publish("sales:revenue-threshold-changed", [revenue_threshold]);
      }
   });

   $("#unit_threshold").slider({
      slide: function(event, ui) {
         unit_threshold = parseInt(ui.value / 10);
         $(".unit_threshold_value").text(unit_threshold);
         session.publish("sales:unit-threshold-changed", [unit_threshold]);
      }
   });

   $("#revenue_threshold_02").slider({
      value: 0,
      orientation: "horizontal",
      range: "min",
      animate: true
   });

   $("#unit_threshold_02").slider({
      value: 0,
      orientation: "horizontal",
      range: "min",
      animate: true
   });

   $("#revenue_threshold_02").slider({
      slide: function(event, ui) {
         revenue_threshold = parseInt(ui.value * 100);
         $(".revenue_threshold_value").text(thousand_formatted(revenue_threshold));
         session.publish("sales:revenue-threshold-changed", [revenue_threshold]);
      }
   });

   $("#unit_threshold_02").slider({
      slide: function(event, ui) {
         unit_threshold = parseInt(ui.value / 10);
         $(".unit_threshold_value").text(unit_threshold);
         session.publish("sales:unit-threshold-changed", [unit_threshold]);
      }
   });

   console.log("pre-pie chart");

   // generate SVG canvases for pie charts and draw charts with initial settings
   document.getElementById("pie_chart_content_container").appendChild(SVG.makeCanvas("pieChart1", 350, 300, 350, 300));
   document.getElementById("pie_chart_content_container_02").appendChild(SVG.makeCanvas("pieChart2", 350, 300, 350, 300));
   drawPieChart();

   $("#helpButton").click(function() { $(".info_bar").toggle() });
}



function updateStatusline(status) {
   $(".statusline").text(status);
};




function DashboardViewModel () {

   var self = this;

   self.simpleIndicatorHighlighted = ko.observable();
   self.barChartHighlighted = ko.observable();
   self.hundredBarHighlighted = ko.observable();
   self.activityStreamHighlighted = ko.observable();
   self.bulletGraphHighlighted = ko.observable();
   self.pieChartHighlighted = ko.observable();

   // dashboard display
   this.dashboard_01_display = ko.observable("block");
   this.dashboard_02_display = ko.observable("none");
   this.dashboard_03_display = ko.observable("none");

   /*****************************
    *     simple indicator
    *****************************/
   self.simpleIndicatorBigNumber = ko.observable(45);
   self.simpleIndicatorComparisonValue = ko.observable(34);
   self.simpleIndicatorTrend = ko.computed(function() {
      //session.log("simpleIndicatorTrend", parseInt((self.simpleIndicatorBigNumber() / self.simpleIndicatorComparisonValue() - 1) * 100));
      // session.log("the parts", self.simpleIndicatorBigNumber(), self.simpleIndicatorComparisonValue());
      return (parseInt(( self.simpleIndicatorBigNumber() / self.simpleIndicatorComparisonValue() - 1 ) * 100));
   },self);
   self.simpleIndicatorTrendDisplay = ko.computed(function() {
      var displayValue;
      self.simpleIndicatorTrend() > 0 ? displayValue = "+" + self.simpleIndicatorTrend() : displayValue = self.simpleIndicatorTrend();
      return displayValue;
   },self);

   self.simpleIndicatorBigNumberDisplay = ko.computed(function() {
      return thousand_formatted(parseInt(self.simpleIndicatorBigNumber()));
   }, self);


   /*****************************
    *      bar chart
    *****************************/

   this.bar_01_value = ko.observable("30"),
   this.bar_02_value = ko.observable("634"),
   this.bar_03_value = ko.observable("34");

   this.bar_scale_max_value = ko.computed(function () {
      var bar_values = [this.bar_01_value(), this.bar_02_value(), this.bar_03_value()];
      var bar_max_value = 0;
      for (var i = 0; i < bar_values.length; i++) {
         if ( parseInt(bar_values[i]) > bar_max_value) {
            bar_max_value = parseInt(bar_values[i]);
         }
      }
      return bar_max_value;
      }, this);

   this.bar_chart_total_height = ko.observable(105);

   this.bar_01_height = ko.computed(function() {
      return bar_chart_height(this.bar_01_value(), this.bar_scale_max_value(), this.bar_chart_total_height());
   }, this);
   this.bar_02_height = ko.computed(function() {
      return bar_chart_height(this.bar_02_value(), this.bar_scale_max_value(), this.bar_chart_total_height());
   }, this);
   this.bar_03_height = ko.computed(function() {
      return bar_chart_height(this.bar_03_value(), this.bar_scale_max_value(), this.bar_chart_total_height());
   }, this);


   /*****************************
    *      hundred bar
    *****************************/

   // target width in px
   self.hundred_bar_width = 335;

   // hundred bar sections to be iterated over
   // arguments: value (is scaled), color, label for legend
   this.hundred_bar_sections = ko.observableArray([
      new hundred_bar_section(100, hundredColor01, "One"),
      new hundred_bar_section(200, hundredColor02, "Two"),
      new hundred_bar_section(100, hundredColor03, "Three"),
   ]);

   // fires when stacked bar array has changed: compute total
   // and rescale individual bars
   this.hundred_bar_total = ko.computed(function() {
      var cnt = self.hundred_bar_sections().length;
      var total = 0;
      for (var i = 0; i < cnt; ++i) {
         total += self.hundred_bar_sections()[i].hundred_width();
      }
      for (var i = 0; i < cnt; ++i) {
         var e = self.hundred_bar_sections()[i];
         e.width(Math.floor((self.hundred_bar_width - 5) * e.hundred_width() / total));
         // Math.floor since otherwise rounding errors in Firefox could mean that
         // the total allowed bar length was exceeded by a small fraction of a pixel

         // (self.hundred_bar_width - 5) is an attempt at giving a little play,
         // since the sequential adjustment of the sub-bar-widths means that
         // during the update cycle the total length can exceed that allowed may lenght,
         // and this results in a line break within the bar, which disappears once the
         // update cycle has finished - FIXME
      }
      return total;
   });

   this.activity_stream_events = ko.observableArray([]);

   /*****************************
    *      bullet graph
    *****************************/

      // section widths (in percent) - sections for all four graphs the same
   this.bulletSection01 = ko.observable("20%");
   this.bulletSection02 = ko.observable("30%");
   this.bulletSection03 = ko.observable("40%");
   this.bulletSection04 = ko.observable("10%");

      // target position
   this.bulletTarget01 = ko.observable(45);
   this.bulletTarget02 = ko.observable(68);
   this.bulletTarget03 = ko.observable(10);
   this.bulletTarget04 = ko.observable(80);

      // bar values
   this.bulletBarPixelWidth = 200;
   this.bulletBarMaxValue = 100;
   this.bulletBar01 = ko.observable(80);
   this.bulletBar02 = ko.observable(50);
   this.bulletBar03 = ko.observable(80);
   this.bulletBar04 = ko.observable(80);

      // actual bar lengths
   this.bulletBar01_length = ko.computed(function() {
      return bar_chart_height(this.bulletBar01(), this.bulletBarMaxValue, this.bulletBarPixelWidth);
   }, this);
   this.bulletBar02_length = ko.computed(function() {
      return bar_chart_height(this.bulletBar02(), this.bulletBarMaxValue, this.bulletBarPixelWidth);
   }, this);
   this.bulletBar03_length = ko.computed(function() {
      return bar_chart_height(this.bulletBar03(), this.bulletBarMaxValue, this.bulletBarPixelWidth);
   }, this);
   this.bulletBar04_length = ko.computed(function() {
      return bar_chart_height(this.bulletBar04(), this.bulletBarMaxValue, this.bulletBarPixelWidth);
   }, this);

   // actual target positions
   this.bulletTarget01_position = ko.computed(function() {
      return bar_chart_height(this.bulletTarget01(), this.bulletBarMaxValue, this.bulletBarPixelWidth);
   }, this);
   this.bulletTarget02_position = ko.computed(function() {
      return bar_chart_height(this.bulletTarget02(), this.bulletBarMaxValue, this.bulletBarPixelWidth);
   }, this);
   this.bulletTarget03_position = ko.computed(function() {
      return bar_chart_height(this.bulletTarget03(), this.bulletBarMaxValue, this.bulletBarPixelWidth);
   }, this);
   this.bulletTarget04_position = ko.computed(function() {
      return bar_chart_height(this.bulletTarget04(), this.bulletBarMaxValue, this.bulletBarPixelWidth);
   }, this);




   /*****************************
    *      pie chart
    *****************************/

   this.pieSection01 = ko.observable(30);
   this.pieSection02 = ko.observable(40);
   this.pieSection03 = ko.observable(50);
   this.pieSection04 = ko.observable(50);
}

// binding variables for the activity stream template
function activity_stream_event (product, units, region, revenue, icon) {
   //this.actvitiy_text = text;
   this.product = product;
   this.units = units;
   this.region = region;
   this.revenue = revenue;
   this.activity_timestamp = format_date(new Date());
   //this.activity_icon = "img/" + icon;
   this.iconmap = {
      "call":"img/cell.png",
      "sale":"img/dollar.png",
      "emergency":"img/fire.png",
      "agreement":"img/handshake.png",
      "news":"img/wireless.png"
   }
   this.activity_icon = this.iconmap[icon];
   session.log(this.activity_icon);
}



// binding variables for the hundred bar section template
function hundred_bar_section (width, color, label) {
   this.hundred_width = ko.observable(width);
   this.width = ko.observable();
   // this.section_color = color;
   this.section_color = color;
   this.legend_label = label;
}

function highlightTimer ( timer ) {

   if (!timer.highlighted) {
      $(timer.targetClass).addClass("highlighted");
      timer.highlighted = true;
   }
   else {
      clearTimeout(timer.timer)
   }

   timer.timer = setTimeout(function () {
      $(timer.targetClass).removeClass("highlighted");
      timer.highlighted = false;
      clearTimeout(timer.timer);
   }, timer.timeout);

}

function drawPieChart () {
   console.log("drawPieChart called");
   // arguments:
      // id of svg element, [ values for section size, get normalized ], center_x, center_y, radius, [ colors ], [ legend labels ], legend_x, legend_y
   pieChart("pieChart1", [parseInt(vm.pieSection01()), parseInt(vm.pieSection02()), parseInt(vm.pieSection03()), parseInt(vm.pieSection04())], 125, 170, 125, [chartColor01, chartColor02, chartColor03, chartColor04], ["North", "East", "South", "West"], 265, 0);
   pieChart("pieChart2", [parseInt(vm.pieSection01()), parseInt(vm.pieSection02()), parseInt(vm.pieSection03()), parseInt(vm.pieSection04())], 125, 170, 125, [chartColor01, chartColor02, chartColor03, chartColor04], ["North", "East", "South", "West"], 265, 0);
}

// subscription event handling

function onDashboardSwitch (args) {
  session.log("onDashboardSwitch", args );
   var dashboards = [ vm.dashboard_01_display, vm.dashboard_02_display, vm.dashboard_03_display];
   for ( var i = 0; i < dashboards.length; i++) {
      if ( i === args[0] ) {
         dashboards[i]("block");
      }
      else {
         dashboards[i]("none");
      }
   }
}




/*********************************
 *    DEMO EVENTS       *
 *********************************/
// event with 'idx' is sent by the dashboard controller
function onRevenue (args, kwargs) {
   //session.log(topicURI, event);
   if (kwargs["idx"]) {
      switch (kwargs["idx"]) {
         case 1:
            vm.simpleIndicatorBigNumber(kwargs["val"]);
            break;
         case 2:
            vm.simpleIndicatorComparisonValue(kwargs["val"]);
            break;
         default:
            session.log("uncovered value", topicURI, kwargs);
            break;
      }
   }
   else {
      vm.simpleIndicatorBigNumber(kwargs[0]);
      vm.simpleIndicatorComparisonValue(kwargs[1]);
   }
   highlightTimer(simple_timer);
}
function onRevenueByProduct (args, kwargs) {
   // session.log(args, kwargs);
   if (kwargs["idx"]) {
      switch (kwargs["idx"]) {
         case 1:
            vm.bar_01_value(kwargs["val"]);
            break;
         case 2:
            vm.bar_02_value(kwargs["val"]);
            break;
         case 3:
            vm.bar_03_value(kwargs["val"]);
            break;
         default:
            session.log("uncovered value", topicURI, kwargs);
            break;
      }
   }
   else {
      if(kwargs["Product A"]) {
         vm.bar_01_value(kwargs["Product A"][0]);
      }
      if(kwargs["Product B"]) {
         vm.bar_02_value(kwargs["Product B"][0]);
      }
      if(kwargs["Product C"]) {
         vm.bar_03_value(kwargs["Product C"][0]);
      }
   }
   highlightTimer( bars_timer );
}
function onUnitsByProduct (args, kwargs) {
   // session.log(topicURI, kwargs);
   if (kwargs["idx"]) {
      switch (kwargs["idx"]) {
         case 1:
            vm.hundred_bar_sections()[0].hundred_width(kwargs["val"]);
            break;
         case 2:
            vm.hundred_bar_sections()[1].hundred_width(kwargs["val"]);
            break;
         case 3:
            vm.hundred_bar_sections()[2].hundred_width(kwargs["val"]);
            break;
         default:
            session.log("uncovered value", topicURI, kwargs);
            break;
      }
   }
   else {
      if(kwargs["Product A"]) {
         vm.hundred_bar_sections()[0].hundred_width(kwargs["Product A"][0]);
      }
      if(kwargs["Product B"]) {
         vm.hundred_bar_sections()[1].hundred_width(kwargs["Product B"][0]);
      }
      if(kwargs["Product C"]) {
         vm.hundred_bar_sections()[2].hundred_width(kwargs["Product C"][0]);
      }
   }
   highlightTimer ( hundred_timer );
}
function onRevenueByRegion (args, kwargs) {
   // session.log(topicURI, kwargs);
   if (kwargs["idx"]) {
      switch (kwargs["idx"]) {
         case 1:
            vm.pieSection01(kwargs["val"]);
            break;
         case 2:
            vm.pieSection02(kwargs["val"]);
            break;
         case 3:
            vm.pieSection03(kwargs["val"]);
            break;
         case 4:
            vm.pieSection04(kwargs["val"]);
            break;
         default:
            session.log("uncovered value", topicURI, kwargs);
            break;
      }
   }
   else {
      if(kwargs["North"]) {
         vm.pieSection01(kwargs["North"][0]);
      }
      if(kwargs["East"]) {
         vm.pieSection02(kwargs["East"][0]);
      }
      if(kwargs["South"]) {
         vm.pieSection03(kwargs["South"][0]);
      }
      if(kwargs["West"]) {
         vm.pieSection04(kwargs["West"][0]);
      }
   }
   drawPieChart();
   highlightTimer ( pie_timer );
}
function onAspByRegion (args, kwargs) {
   // session.log(topicURI, kwargs);
   if (kwargs["idx"]) {
      switch (kwargs["idx"]) {
         case 1:
            vm.bulletBar01(kwargs["val"]);
            break;
         case 2:
            vm.bulletBar02(kwargs["val"]);
            break;
         case 3:
            vm.bulletBar03(kwargs["val"]);
            break;
         case 4:
            vm.bulletBar04(kwargs["val"]);
            break;
         default:
            session.log("uncovered value", topicURI, kwargs);
            break;
      }
   }
   else {
      if(kwargs["North"]) {
         vm.bulletBar01(kwargs["North"][0] * .2);
         vm.bulletTarget01(kwargs["North"][1] * .2);
      }
      if(kwargs["East"]) {
         vm.bulletBar02(kwargs["East"][0] * .2);
         vm.bulletTarget02(kwargs["East"][1] * .2);
      }
      if(kwargs["South"]) {
         vm.bulletBar03(kwargs["South"][0] * .2);
         vm.bulletTarget03(kwargs["South"][1] * .2);
      }
      if(kwargs["West"]) {
         vm.bulletBar04(kwargs["West"][0] * .2);
         vm.bulletTarget04(kwargs["West"][1] * .2);
      }
   }


   //vm.bulletTarget01(kwargs["North"][1]);
   //vm.bulletTarget02(kwargs["East"][1]);
   //vm.bulletTarget03(kwargs["South"][1]);
   //vm.bulletTarget04(kwargs["West"][1]);

   highlightTimer ( bullet_timer );

}

// var onSaleTest = { "revenue": 2000, "units": 3, "product": "Hummer", "region": "moon"};

function onSale(args, kwargs) {
   session.log("onSale", kwargs, kwargs.revenue > revenue_threshold);

   if (kwargs["revenue"] > revenue_threshold || kwargs["units"] > unit_threshold) {

      var icon = "sale";

      vm.activity_stream_events.push(new activity_stream_event(kwargs["product"], kwargs["units"], kwargs["region"], kwargs["revenue"]));
      session.publish("sales:activity-display-threshold-exceeded", [], kwargs);
      highlightTimer ( activity_timer );
      $(".activity_stream_window").each(function() {
         this.scrollTop = this.scrollHeight;
      })

   };

};

function onRevenueThresholdChanged (args) {
   $("#revenue_threshold").slider({
      value: args[0]
   });
};

function onUnitThresholdChanged (args) {
   $("#unit_threshold").slider({
      value: args[0]
   });
};



/******* SVG PIE CHART CODE ******/
/* from http://jmvidal.cse.sc.edu/talks/canvassvg/javascriptandsvg.xml ***/

// Create a namespace for our SVG-related utilities
var SVG = {};

// These are SVG-related namespace URLs
SVG.ns = "http://www.w3.org/2000/svg";
SVG.xlinkns = "http://www.w3.org/1999/xlink";

// Create and return an empty <svg> element.
// Note that the element is not added to the document
// Note that we can specify the pixel size of the image as well as
// its internal coordinate system.
SVG.makeCanvas = function(id, pixelWidth, pixelHeight, userWidth, userHeight) {
    var svg = document.createElementNS(SVG.ns, "svg:svg");
    svg.setAttribute("id", id);
    // How big is the canvas in pixels
    svg.setAttribute("width", pixelWidth);
    svg.setAttribute("height", pixelHeight);
    // Set the coordinates used by drawings in the canvas
    svg.setAttribute("viewBox", "0 0 " + userWidth + " " + userHeight);
    // Define the XLink namespace that SVG uses
    svg.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink",
                       SVG.xlinkns);
    return svg;
};


/**
 * Draw a pie chart into an <svg> element.
 * Arguments:
 *   canvas: the SVG element (or the id of that element) to draw into.
 *   data: an array of numbers to chart, one for each wedge of the pie.
 *   cx, cy, r: the center and radius of the pie
 *   colors: an array of HTML color strings, one for each wedge
 *   labels: an array of labels to appear in the legend, one for each wedge
 *   lx, ly: the upper-left corner of the chart legend
 */
function pieChart(canvas, data, cx, cy, r, colors, labels, lx, ly) {
    //session.log(arguments);
    // Locate canvas if specified by id instead of element
    if (typeof canvas == "string") canvas = document.getElementById(canvas);

    // Add up the data values so we know how big the pie is
    var total = 0;
    for(var i = 0; i < data.length; i++) total += data[i];

    // Now figure out how big each slice of pie is.  Angles in radians.
    var angles = []
    for(var i = 0; i < data.length; i++) angles[i] = data[i]/total*Math.PI*2;

    // Loop through each slice of pie.
    startangle = 0;
    for(var i = 0; i < data.length; i++) {
        // This is where the wedge ends
        var endangle = startangle + angles[i];

        // Compute the two points where our wedge intersects the circle
        // These formulas are chosen so that an angle of 0 is at 12 o'clock
        // and positive angles increase clockwise.
        var x1 = cx + r * Math.sin(startangle);
        var y1 = cy - r * Math.cos(startangle);
        var x2 = cx + r * Math.sin(endangle);
        var y2 = cy - r * Math.cos(endangle);

        // This is a flag for angles larger than than a half circle
        var big = 0;
        if (endangle - startangle > Math.PI) big = 1;

        // We describe a wedge with an <svg:path> element
        // Notice that we create this with createElementNS()
        var path = document.createElementNS(SVG.ns, "path");

        // This string holds the path details
        var d = "M " + cx + "," + cy +  // Start at circle center
            " L " + x1 + "," + y1 +     // Draw line to (x1,y1)
            " A " + r + "," + r +       // Draw an arc of radius r
            " 0 " + big + " 1 " +       // Arc details...
            x2 + "," + y2 +             // Arc goes to to (x2,y2)
            " Z";                       // Close path back to (cx,cy)
        // This is an XML element, so all attributes must be set
        // with setAttribute().  We can't just use JavaScript properties
        path.setAttribute("d", d);              // Set this path
        path.setAttribute("fill", colors[i]);   // Set wedge color
        //path.setAttribute("class", colors[i]);
        //path.setAttribute("stroke", "black");   // Outline wedge in black
        //path.setAttribute("stroke-width", "2"); // 2 units thick
        canvas.appendChild(path);               // Add wedge to canvas

        // The next wedge begins where this one ends
        startangle = endangle;

        // Now draw a little matching square for the key
        var icon = document.createElementNS(SVG.ns, "rect");
        icon.setAttribute("x", lx);             // Position the square
        icon.setAttribute("y", ly + 30*i);
        icon.setAttribute("width", 20);         // Size the square
        icon.setAttribute("height", 20);
        icon.setAttribute("fill", colors[i]);   // Same fill color as wedge
        //icon.setAttribute("class", colors[i]);   // Same fill color as wedge
        //icon.setAttribute("stroke", "black");   // Same outline, too.
        //icon.setAttribute("stroke-width", "2");
        canvas.appendChild(icon);               // Add to the canvas

        // And add a label to the right of the rectangle
        var label = document.createElementNS(SVG.ns, "text");
        label.setAttribute("x", lx + 30);       // Position the text
        label.setAttribute("y", ly + 30*i + 18);
        // Text style attributes could also be set via CSS
        label.setAttribute("font-family", "sans-serif");
        label.setAttribute("font-size", "12");
        //label.setAttribute("stroke", "#bbbbbb");
        label.setAttribute("fill", "#bbbbbb");
        // Add a DOM text node to the <svg:text> element
        label.appendChild(document.createTextNode(labels[i]));
        canvas.appendChild(label);              // Add text to the canvas
    }
}


// helper functions

// takes a javascript date object and returns a formatted string
function format_date (myDate) {
   return (((myDate.getMonth()+1) < 10 ? '0' : '') + myDate.getMonth()) + "/" + ((myDate.getDate() < 10 ? '0' : '') + myDate.getDate()) + "/" + myDate.getFullYear() + "  " + ((myDate.getHours() < 10 ? '0' : '') + myDate.getHours()) + ":" + ((myDate.getMinutes() <10 ? '0' : '') + myDate.getMinutes())/* + "  " + "GMT " + (( myDate.getTimezoneOffset()/60*-1 < 0 ) ? "-" : "+") + myDate.getTimezoneOffset()/60*-1*/;
};

// takes a current value, the maximum possible value and a display element dimension, returns a scaled current value to fit with the display element
function bar_chart_height(value, maxvalue, totalHeight) {
   return value/maxvalue*totalHeight;
}

// takes a number (can be passed as a string or integer), returns this as a string with a dot to mark three decimal places)
function thousand_formatted(number) {
   var full = number.toString();
   var formatted = "";
   while ( full.length > 3) {
      var thousand = full.slice((full.length - 3), full.length);
      var formatted = "." + thousand + formatted;
      var full = full.slice(0, (full.length - 3));
   }
   var formatted = full + formatted;
   return formatted;
}


/*** scaling with CSS
 *
 * regular starting point is the top left corner of the element (moz), opera claims middle (test this)
 * is set with transform-origin: top/left..., % or px
 *
 * then use transform: scale (x,y)
 *
 * so:
 * - render the page
 * - get the width of the viewport
 * - get the width of the table
 * - scale factor = viewportwidth/tablewidth
 * - scale by this
 *
 *
 *
 *
 */
