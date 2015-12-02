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
// var demoPrefix = "io.crossbar.examples";

// var wsuri = "ws://192.168.1.143:8080/ws";
var wsuri = "wss://demo.crossbar.io/ws";
// if (document.location.origin == "file://") {
//    wsuri = "ws://127.0.0.1:8080/ws";

// } else {
//    wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
//                document.location.host + "/ws";
// }

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

      console.log("connected");

      session = sess;

      updateStatusline("Connected to " + wsuri);

      setup();

   };

   connection.onclose = function() {
      session = null;
      console.log("connection closed ", arguments);
   }

   connection.open();
}

$(document).ready(function() {
   updateStatusline("Not connected.");

   connect();

});


var newWindowLink = null,
    padGauges = [],
    isReconnect = false;

function setup() {

   console.log("setting up");

   if (isReconnect) {
      return;
   }
   isReconnect = true;

   // create and configure padGauges
   //

   padGauges.push(new JustGage({
      id: "g" + padGauges.length,
      value: 0,
      min: 0,
      max: 1023,
      title: "Pad 1",
      refreshAnimationTime: 1
   }));


   padGauges.push(new JustGage({
      id: "g" + padGauges.length,
      value: 0,
      min: 0,
      max: 1023,
      title: "Pad 2",
      refreshAnimationTime: 1
   }));


   padGauges.push(new JustGage({
      id: "g" + padGauges.length,
      value: 0,
      min: 0,
      max: 1023,
      title: "Pad 3",
      refreshAnimationTime: 1
   }));


   padGauges.push(new JustGage({
      id: "g" + padGauges.length,
      value: 0,
      min: 0,
      max: 1023,
      title: "Pad 4",
      refreshAnimationTime: 1
   }));


   // var crateCounter = document.getElementById("crateCounter");
   // var cratesDisplay = document.getElementById("cratesDisplay");
   // var cratesImages = cratesDisplay.getElementsByTagName("img");
   // var maxCrates = cratesImages.length;
   
   // var updateCratesDisplay = function (numberOfCrates) {
   //    if (numberOfCrates > maxCrates) {
   //       console.log("cannot display that many crates");
   //       return;
   //    }

   //    crateCounter.innerHTML = numberOfCrates;

   //    // cratesImages is a node list, not an array, so no 'forEach' iteration
   //    for (var i = 0; i < cratesImages.length; i++) {
   //       if (i < numberOfCrates) {
   //          cratesImages[i].classList.add("shown");
   //       } else {
   //          cratesImages[i].classList.remove("shown");
   //       }
   //    }

   // };

   // below first value = 0 crates
   var cratesThresholds = [4.8, 6.5, 8.5, 11, 12.9, 14.0, 15.5];
   var cratesThresholds = [4.8, 7.5, 10, 12.5, 14.5, 16, 19];

   var sensorRanges = [[0, 390], [391, 764], [765, 863], [864, 901], [902, 923], [924, 1000]];


   var processed = false;
   var doProcessing = function (values) {

      console.log("doProcessing", values);

      // // sum
      // var sum = 0;
      // var cuSum = 0;

      // values.forEach(function (val) {

      //    sum += val;

      //    // check which interval the value falls into
      //    var range = null;
      //    var rangeBase = null;
      //    for (var i = 0; i < sensorRanges.length; i++) {
      //       var currRange = sensorRanges[i];
      //       if (val >= currRange[0] && val <= currRange[1]) {
      //          range = currRange;
      //          rangeBase = i;
      //          break;
      //       }
      //    };

      //    // calculate the "crate units" return based on linear interpolation
      //    console.log()
      //    var cu = rangeBase + ( (val - range[0]) / (range[1] - range[0]) );
      //    // console.log("cu", cu);
      //    cuSum += cu;

      // });

      // sumGauge.refresh(sum);  

      // // console.log("sum: ", sum);
      // // console.log("cuSum: ", cuSum);

      // // average
      // var average = parseInt(sum / values.length);

      // averageGauge.refresh(average);


      // // calculate number of crates
      // var numberOfCrates = 0;
      // // var numberOfCrates = 5;
      // // var numberOfCrates = (parseInt(cuSum / 4) * 2);
      // // updateCratesDisplay(numberOfCrates);

      // var determineNumberOfCrates = function () {
         
      //    var foundNumberOfCrates = cratesThresholds.some(function(currentThreshold, i) {
      //       if (cuSum < currentThreshold) {
      //          numberOfCrates = i;
      //          return true           
      //       }
      //    });

      //    return foundNumberOfCrates;

      // }

      // if (!determineNumberOfCrates()) {
      //    console.log("too many crates");
      // }

      // updateCratesDisplay(numberOfCrates);



      // four crates display


      // the states we can have 
      var crateStates = {
         NU: [false, false, false, false],

         A1: [false, false, false, true ],
         A2: [false, false, true,  false],
         A3: [false, true,  false, false],
         A4: [true,  false, false, false],

         B1: [true,  true,  false, false],
         B2: [true,  false, true,  false],
         B3: [true,  false, false, true ],
         B4: [false, true,  true,  false],
         B5: [false, true,  false, true ],
         B6: [false, false, true,  true],

         C1: [true,  true,  false, true],
         C2: [true,  true,  true,  false],
         C3: [true,  false, true,  true],
         C4: [false, true,  true,  true],

         FU: [true, true, true, true]
      };

      // our measurements for the states
      var measurements = [
         { val: [571, 316, 299, 419], state: "NU"},
         { val: [737, 730, 365, 544], state: "A1"},
         { val: [625, 464, 461, 715], state: "A2"},
         { val: [850, 470, 420, 410], state: "A3"},
         { val: [690, 330, 660, 520], state: "A4"},
         { val: [870, 533, 749, 567], state: "B1"},
         { val: [715, 481, 787, 747], state: "B2"},
         { val: [771, 702, 770, 634], state: "B3"},
         { val: [863, 636, 607, 730], state: "B4"},
         { val: [885, 761, 497, 551], state: "B5"},
         { val: [742, 811, 506, 736], state: "B6"},
         { val: [898, 776, 777, 635], state: "C1"},
         { val: [884, 660, 764, 731], state: "C2"},
         { val: [800, 820, 773, 779], state: "C3"},
         { val: [900, 820, 635, 742], state: "C4"},
         { val: [892, 820, 800, 787], state: "FU"}
      ];

      var lSqDifference = null;
      var closestState = null;
      
      measurements.forEach(function(mes) {

         var comparativeValues = mes.val;

         console.log("comp: ", comparativeValues, mes.state );
         console.log("val:", values);

         var lSqDiff = null;
         values.forEach(function(val, i) {
            lSqDiff += Math.pow((val - comparativeValues[i]), 2);
         })

         console.log("lSqDiff", lSqDiff);

         if (lSqDifference === null || lSqDiff < lSqDifference) {
            console.log("storing lsqDiff");
            lSqDifference = lSqDiff;
            closestState = mes.state;
         }
      })

      var currentState = crateStates[closestState];
      console.log("currentState", closestState, currentState);

      var fourCrates = {
         A0: currentState[0],
         A1: currentState[1],
         A2: currentState[2],
         A3: currentState[3]
      };

      var fourCratesCounter = document.getElementById("fourCratesCounter");

      var fourCratesImages = {
         A0: document.getElementById("A0"),
         A1: document.getElementById("A1"),
         A2: document.getElementById("A2"),
         A3: document.getElementById("A3")
      };

      var cratesCount = 0;
      
      for (var crate in fourCrates) {   
         if (fourCrates.hasOwnProperty(crate)) {

            if (fourCrates[crate]) {

               cratesCount += 1;

               fourCratesImages[crate].classList.add("shown");     

            } else {

               fourCratesImages[crate].classList.remove("shown");

            }

         }  

      }
      
      fourCratesCounter.innerHTML = cratesCount;

      // processed = true;
   };


   // subscribe to pad value updates & set these
   session.subscribe("io.crossbar.demo.wpad.1.on_change", function (args) {
      

      var values = args[0].values;



      // §%$&`?! - values is now eight long since it includes another unrelated sensor!
      if (values.length > 4) {
         values = values.slice(0, 4);
      }

      console.log("pad data: ", values);

      var reversedValues = [];

      values.forEach(function(val, i) {
         // we get resistance values from the pads, which decrease with pressure
         // we want values to increase with pressure
         var reversedVal = 1023 - val; // theoretical max is 1023, adjust to fit your pads

         padGauges[i].refresh(reversedVal);

         reversedValues.push(reversedVal);

      });

      console.log("rev data: ", reversedValues);

      doProcessing(reversedValues);

   });

   // // set up the sum
   // var sumGauge = new JustGage({
   //    id: "sum",
   //    value: 0,
   //    min: 0,
   //    max: 4040,
   //    title: "Sum of Pads",
   //    // label: "???",
   //    refreshAnimationTime: 1
   // });

   // // set up the average
   // var averageGauge = new JustGage({
   //    id: "avg",
   //    value: 0,
   //    min: 0,
   //    max: 1010,
   //    title: "Average of Pads",
   //    // label: "???",
   //    refreshAnimationTime: 1
   // });

   // set up the page switching
   var gaugesPage = document.getElementById("gaugesPage");
   var cratesPage = document.getElementById("cratesPage");
   document.getElementById("gaugesSwitch").addEventListener("click", function() {
      console.log("addEventListener 1");
      cratesPage.classList.remove("shown");
      gaugesPage.classList.add("shown");
   });
   document.getElementById("crateSwitch").addEventListener("click", function() {
      console.log("addEventListener 2");
      gaugesPage.classList.remove("shown");
      cratesPage.classList.add("shown");
   });

}
