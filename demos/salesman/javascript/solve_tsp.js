console.log("loaded");

try {
   // for Node.js
   var autobahn = require('autobahn');
   var isBrowser = false;
} catch (e) {
   // for browsers (where AutobahnJS is available globally)
   var isBrowser = true;
}

var when = autobahn.when;

console.log("isBrowser ", isBrowser);

// the URL of the WAMP Router (Crossbar.io)
//
var wsuri = null;

// var computeGroup = "competition";

if (isBrowser && document.location.origin == "file://") {
   wsuri = "ws://127.0.0.1:8080/ws";

} else if (isBrowser) {
   wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws";
} else {
   console.log("arguments", process.argv[2]);
   wsuri = process.argv[2] || 'ws://127.0.0.1:8080/ws';
   // computeGroup = process.argv[3] || 'competition';
}

// the WAMP connection to the Router
//
var connection = new autobahn.Connection({
   url: wsuri,
   realm: "realm1"
});
var session = null;

connection.onopen = function(newSession, details) {
   console.log("Connected");

   session = newSession;

   session.register("io.crossbar.demo.tsp.solve_tsp", solveTsp);
};

connection.onclose = function(reason, details) {
   console.log("Connection fail: ", reason, details);
};

// // connect automatically in NodeJS, but only on user action in browser
// if(!isBrowser) {
//    connection.open();
// } else {
//    // add event listener to connect button
// }

connection.open();

var solveTsp = function(args, kwargs) {
   // needs to create an object which contains all the functionality, since this can be called multiple times in parallel! - FIXME

   // the data we receive to set this up
   var points = kwargs.points;
   var computeTime = kwargs.computeTime;
   var computeGroup = kwargs.computeGroup;

   // the data we need for coordination + results
   var leaderBoard = []; // contains the 10 best routes + the ID of the components which found them
   var nickRegistrations = {}; // nicks and the associated component IDs
   var idsToNicks = {}; // generate this for lookup - needed to update nickStats + the leaderboard
   var nickStats = {}; // number of connected components (current/max/total), number of total compute cylces contributed, current compute cycles/s
   var currentBestRoute = []; // indices of points
   var currentBestLength = null;
   var temp = null; // the temperature to use for a compute_tsp call
   var tempDecrease = 1; // none for the time being, temp is only decreased between compute calls, not during the actual computation
   var iterations = 300; // adjust as needed once we have clients running on slow devices, so that we get a reasonable time until the computations return
   var onErrorWait = 300; // timeout before attempting to send the next call when a call returns that all compute components are presently busy. Should really not be a hardcoded constant, but depend on the current average return time of calls - FIXME
   var timeExpired = false;

   // calculate the temperature fall across the computeTime
   // IMPLEMENT ME

   // create the computeTime timer
   setTimeout(function() {
      timeExpired = true;
   }, computeTime);

   // check whether any compute nodes for our computeGroup are present, if so: start, else subscribe to the join event and start when this is called the first time
   session.call("wamp.registration.match", ["io.crossbar.demo.tsp." + computeGroup + ".compute_tsp"]).then(function(res) {
      if(res.length > 0) {
         // start calling them
      } else {
         session.subscribe("wamp.registration.on_create", function(args, kwargs, details) {
            // filter this for the first registration for "io.crossbar.demo.tsp." + computeGroup + ".compute_tsp"
            // start calling once this has been received
         });
      }
   }, session.log)

   var startCalling = function() {

      // trigger the temperature falling
      // IMPLEMENT ME

      var onComputation = function(res) {
         // check whether time has expired - exit if so
         if(timeExpired) {
            deliverResult();
            return;
         }

         var resultLength = res.length;
         var resultRoute = res.route;

         // check whether we have a new best route
         if(resultLength < currentBestLength) {
            currentBestLength = resultLength;
            currentBestRoute = resultRoute;
         }

         // check whether/where this belongs into the leaderboard
         // this may be expensive, so possibly do outside of this function
         // and periodically. But needs to be triggered on a new best result, since this should be shown immediately
         leaderBoard.forEach(function(el, i) {

         })

         // update the nickStats
         

         triggerComputation();
      }

      var onComputationError = function(error, details) {
         console.log("computation call error", error, detaisl);
         // wait the current timeout and then try to call again
         setTimeout(function() {
            triggerComputation();
         }, onErrorWait)
      }

      var triggerComputation = function() {

         session.call("io.crossbar.demo.tsp." + computeGroup + ".compute_tsp", [], {
            points: points,
            startRoute: currentBestRoute,
            temp:temp,
            tempDecrease: tempDecrease,
            iterations: iterations
         }).then(onComputation, onComputationError);

      }

      // create the initial route to send to the compute nodes
      // store the length of this
      var straightIndex = createPointsIndex(points);
      currentBestRoute = randomSwapMultiple(straightIndex);
      currentBestLength = computeLength(currentBestRoute);

      triggerComputation();

   }

}


var createPoints = function(amount, maxCoordinates, minDistance) {
   var amount = amount || 30;
   var maxCoordinates = maxCoordinates || [500, 500];
   var minDistance = minDistance || 10;
   var points = [];

   console.log(amount, maxCoordinates, minDistance);

   while(amount) {
      console.log("creating a point");

      // create point
      var point = [
         Math.floor(Math.random() * maxCoordinates[0]),
         Math.floor(Math.random() * maxCoordinates[1]),
      ];

      var minDistanceKept = points.every(function(el) {
         if(parseInt(computeDistance(el, point)) < minDistance) {
            return false;
         }
         return true;
      });

      // check that point is not below minimum distance to existing points
      if(minDistanceKept) {
         // if point is OK decrement counter
         points.push(point);
         amount--;
      }

   }

   return points;

}

var createPointsIndex = function(points) {
   var index = [];
   var i = 0;
   points.forEach(function(p, i) {
      index.push(i);
      i++;
   })
   return index;
}


// random swap of multiple points (two points at a time)
var randomSwapMultiple = function(route, iterations) {

   // route is array, and since we don't want to overwrite this, wee need to deep-copy it
   var routeCopy = deepCopyArray(route);

   while(iterations) {

      // pick the two elements to swap
      var first = Math.floor(Math.random() * routeCopy.length);
      var second = first;
      while(second === first) {
         // console.log("calculating second", first, second);
         second = Math.floor(Math.random() * routeCopy.length);
      }

      var store = routeCopy[first];
      routeCopy[first] = routeCopy[second];
      routeCopy[second] = store;

      iterations--;
   }


   return routeCopy;
}


var computeLength = function(points, route) {
   var length = null;

   route.forEach(function(pointIndex, i) {
      if(route[i + 1]) {
         // console.log(points[i + 1], points[i]);
         var distance = computeDistance(points[route[i + 1]], points[pointIndex]);
         length += distance;
      }
   })

   return length;
}

var computeDistance = function(firstPoint, secondPoint) {
   var distance = Math.sqrt(
      Math.pow(firstPoint[0] - secondPoint[0], 2) +
      Math.pow(firstPoint[1] - secondPoint[1], 2)
   );

   return distance;
}



// var testCompute = function() {
//    var points = createPoints(30);
//    var startRoute = createPointsIndex(points);
//    var temp = 1;
//    var tempDecrease = 0.95;
//    var iterations = 200;
//
//    // console.log("test result: ", computeTsp([], {
//    //    points: points,
//    //    startRoute: startRoute,
//    //    temp: temp,
//    //    tempDecrease: tempDecrease,
//    //    iterations: iterations
//    // }))
//
//    var testResult = session.call("api:compute_tsp", [], {
//       points: points,
//       startRoute: startRoute,
//       temp: temp,
//       tempDecrease: tempDecrease,
//       iterations: iterations
//    });
//
//    testResult.then(function() {
//       console.log("test done", arguments);
//    });
// }
