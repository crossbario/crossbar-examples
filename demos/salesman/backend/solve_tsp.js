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

   testSolveTsp();
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

var solvers = [];
var solveTsp = function(args, kwargs) {
   console.log("soveTsp called", kwargs);

   // deferred which we resolve once the compute time has expired
   var solution = when.defer();

   // create the solver object
   // this gets the call data + 'solution' deferred
   // it resolves the deferred with the current best solution, leaderboard etc.
   // once the compute time has expired
   solvers.push(createSolver(kwargs, solution));

   return solution.promise;
}

var createSolver = function(startData, solution) {
   console.log("createSolver called", startData, solution);

   var solver = {};

   // create the data structures we needed
   solver.data = createDataStructure(startData, solution);

   // set the timeout after which we resolve with our current solution
   setTimeout(function() {
      solver.data.timeExpired = true;
   }, solver.data.computeTime);

   // calculate the temperature fall across the compute timeout
   // simple linear falling for now - FIXME - should instead be exponential!!
   solver.data.timeTempDecrease = 1 / solver.data.computeTime * solver.data.timeTempDecreaseInterval;

   // check whether any compute nodes for our computeGroup are present, if so: start, else subscribe to the join event and start when this is called the first time
   session.call("wamp.registration.match", ["io.crossbar.demo.tsp." + solver.data.computeGroup + ".compute_tsp"]).then(function(res) {
      console.log("wamp.registration.match", res);

      if(res !== null) {
         // start calling them
         console.log("computeTsp registered, starting calling");
         startCalling(solver);
      } else {
         console.log("computeTsp not registered, subscribe to registration event");
         session.subscribe("wamp.registration.on_create", function(args, kwargs, details) {
            console.log("registration event received, analyzing");
            // filter this for the first registration for "io.crossbar.demo.tsp." + computeGroup + ".compute_tsp"
            var registrationUri = args[1].uri;
            if(registrationUri === "io.crossbar.demo.tsp." + solver.data.computeGroup + ".compute_tsp") {
               console.log("registration for computeTsp received, starting calling");
               // start the calling of compute nodes
               startCalling(solver);
            }

         });
      }
   }, session.log);

   // needs to keep track of the number of currently connected compute instances
   // so subscribe to the meta-events and filter these for joins/leaves
   // FIXME

   return solver;
};

var createDataStructure = function(startData, solution) {
   var data = {
      // data we receive from the startTSP component
      points: startData.points,
      computeTime: startData.computeTime,
      computeGroup: startData.computeGroup,
      solution: solution, // the deferred object which we resolve at the end of compute time

      // results storage
      leaderBoard: [], // contains the 10 best routes + the ID of the components which found them
      nickRegistrations:{}, // nicks and the associated component IDs
      idsToNicks: {}, // generate this for lookup - needed to update nickStats + the leaderboard
      nickStats: {}, // number of connected components (current/max/total), number of total compute cylces contributed, current compute cycles/s
      currentBestRoute: [], // indices of points
      currentBestLength: null,

      // iteration related
      callingStarted: false, // whether we've started calling the compute nodes
      temp: 1, // the temperature to use for the compute_tsp call
      tempDecrease: 1, // temp decrease factor to be applied after each computation cylce (1 = no temp decrease)
      timeTempDecrease: null, // temp decrease per time interval, calculated based on compute time and timeTempDecreaseInterval
      timeTempDecreaseInterval: 10, // decrease temperature every x ms during compute time
      iterations: 50, // adjust as needed once we have clients running on slow devices, so that we get a reasonable time until the computations return
      onErrorWait: 300, // timeout before attempting to send the next call when a call returns that all compute components are presently busy. Should really not be a hardcoded constant, but depend on the current average return time of calls - FIXME
      onSuccessWait: 10,
      timeExpired: false,

   };

   return data;
};


var startCalling = function(solver) {

   console.log("start calling", solver.data.computeGroup, solver.data.solution);

   // trigger the temperature falling
   // FIXME
   setInterval(function() {
      solver.data.temp -= solver.data.timeTempDecrease;
   }, solver.data.timeTempDecreaseInterval);

   // create the initial route to send to the compute nodes
   // store the length of this
   var straightIndex = createPointsIndex(solver.data.points);
   console.log("straightIndex", straightIndex);
   solver.data.currentBestRoute = randomSwapMultiple(straightIndex, straightIndex.length);
   solver.data.currentBestLength = computeLength(solver.data.points, solver.data.currentBestRoute);

   console.log("initial route", solver.data.currentBestRoute, solver.data.currentBestLength);

   // send current best result after end of compute time
   setTimeout(function() {
      solver.data.solution.resolve({
         currentBestRoute: solver.data.currentBestRoute,
         currentBestLength: solver.data.currentBestLength
      });
      solver.data.timeExpired = true; // should be checked before each sending of compute task
   }, solver.data.computeTime);

   // trigger loop:
   // - has adjustable delay between issuing calls
   // - checks for a "max concurrency reached" flag
   // - if "max concurrency reached", then increase delay (e.g. by one order of magnitude)
   // - delay on max concurrency reached may be adaptive, i.e. we check whether the next call after the delay succeeds and decrease the delay in this case, else increase it
   // - checks whether the compute time has expired and stops in that case

   var triggerComputation = function() {
      console.log("triggerComputation called");

      if(solver.data.timeExpired || solver.data.stopCompute) {
         return;
      }

      computeCall = callComputation(solver);

      // for now, while there is no
      computeCall.then(
         function(res) {
            console.log("received computation result", res);
            // process the result
            onComputationResult(solver, res);
            // call triggerCompute after the shorter timeout
            // setTimeout(function() {
               triggerComputation();
            // }, solver.data.onSuccessWait);
         },
         function(err) {
            // check if error reason is that all slots are currently busy - FIXME
            console.log("call error", err);
            // // if so: call triggerCompute after longer timeout
            // setTimeout(function() {
            //    triggerComputation();
            // }, solver.data.onErrorWait);
         }
      );

   };
   triggerComputation();

};


var onComputationResult = function(solver, res) {

   var resultLength = res.length;
   var resultRoute = res.route;

   // check whether we have a new best route
   if(resultLength < solver.data.currentBestLength) {
      solver.data.currentBestLength = resultLength;
      solver.data.currentBestRoute = resultRoute;

      // announce the change in best results
      session.publish("io.crossbar.demo.tsp.new_best_result", [], {
         computeGroup: solver.data.computeGroup,
         bestLength: resultLength,
         bestRoute: resultRoute
      });
   }

   // check whether/where this belongs into the leaderboard
   // this may be expensive, so possibly do outside of this function
   // and periodically. But needs to be triggered on a new best result, since this should be shown immediately
   // solver.data.leaderBoard.forEach(function(el, i) {
   //
   // })

   // update the nickStats


   // triggerComputation();
};
//
//    var onComputationError = function(error, details) {
//       console.log("computation call error", error, detaisl);
//       // wait the current timeout and then try to call again
//       setTimeout(function() {
//          triggerComputation();
//       }, onErrorWait)
//    }
//
//    var triggerComputation = function() {
//
//       session.call("io.crossbar.demo.tsp." + computeGroup + ".compute_tsp", [], {
//          points: points,
//          startRoute: currentBestRoute,
//          temp:temp,
//          tempDecrease: tempDecrease,
//          iterations: iterations
//       }).then(onComputation, onComputationError);
//
//    }
//
//    // create the initial route to send to the compute nodes
//    // store the length of this
//    var straightIndex = createPointsIndex(points);
//    currentBestRoute = randomSwapMultiple(straightIndex);
//    currentBestLength = computeLength(currentBestRoute);
//
//    // initial trigger of computation recursion
//    triggerComputation();


var callComputation = function(solver) {
   // console.log("callComputation called");

   // console.log("call computeTsp: ", {
   //    points: solver.data.points,
   //    startRoute: solver.data.currentBestRoute,
   //    temp:solver.data.temp,
   //    tempDecrease: solver.data.tempDecrease,
   //    iterations: solver.data.iterations
   // });


   return session.call("io.crossbar.demo.tsp." + solver.data.computeGroup + ".compute_tsp", [], {
      points: solver.data.points,
      startRoute: solver.data.currentBestRoute,
      temp:solver.data.temp,
      tempDecrease: solver.data.tempDecrease,
      iterations: solver.data.iterations
   });


};


var createPoints = function(amount, maxCoordinates, minDistance) {
   var amount = amount || 30;
   var maxCoordinates = maxCoordinates || [500, 500];
   var minDistance = minDistance || 10;
   var points = [];

   console.log("creating points", amount, maxCoordinates, minDistance);

   while(amount) {

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

};

var createPointsIndex = function(points) {
   var index = [];
   var i = 0;
   points.forEach(function(p, i) {
      index.push(i);
      i++;
   });
   return index;
};


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
};


var computeLength = function(points, route) {
   // console.log("computeLength", points, route);

   var length = null;

   route.forEach(function(pointIndex, i) {
      if(route[i + 1]) {
         // console.log(points[i + 1], points[i]);
         // console.log("i", points[route[i + 1]], points[route[i]]);
         var distance = computeDistance(points[route[i + 1]], points[route[i]]);
         length += distance;
      }
   });

   return length;
};

var computeDistance = function(firstPoint, secondPoint) {
   var distance = Math.sqrt(
      Math.pow(firstPoint[0] - secondPoint[0], 2) +
      Math.pow(firstPoint[1] - secondPoint[1], 2)
   );

   return distance;
};


var deepCopyArray = function(array) {
   var copiedArray = [];
   array.forEach(function(el) {
      copiedArray.push(el);
   });
   return copiedArray;
};


/*

Test/Trial code below - weed out unneeded before release - FIXME

*/

var testComputeLength = function() {
   var points = createPoints(10, [300, 300], 10);
   var route = createPointsIndex(points);
   var length = computeLength(points, route);

   console.log("testComputeLength", length);
};


var testMetaRegistered = function(computeGroup) {
   var computeGroup = computeGroup || "competition";

   session.call("wamp.registration.match", ["io.crossbar.demo.tsp." + computeGroup + ".compute_tsp"]).then(function(res) {
      console.log("current registrations for " + computeGroup + ": ", res);
   });
};

var testMetaSubscribe = function(computeGroup) {
   var computeGroup = computeGroup || "competition";

   session.subscribe("wamp.registration.on_create", function(args, kwargs, details) {
      console.log("wamp.registration.on_create", args[0], args[1]);
   });
};

// currently called on connect to auto-test on page reload
var testSolveTsp = function() {

   var testData = {
      points: createPoints(40, [600, 600], 5),
      computeTime: 30000,
      computeGroup: "competition"
   };

   var solution = solveTsp([], testData);
   console.log("solution - sync:", solution);

   solution.then(
      function(res) {
         console.log("solveTsp returns", res);
      },
      function(err) {
         console.log("solveTps error", err);
      }
   );

   session.publish("io.crossbar.demo.tsp.started", [], {
      points: testData.points,
      computeTime: testData.computeTime
   });

};





// var testDefer = function(returnTime) {
//    var deferred = when.defer();
//    var timeOut = returnTime || 1000;
//
//    setTimeout(function() {
//       deferred.resolve("resolution value");
//    }, timeOut);
//
//    return deferred.promise;
//
// };
//
// console.log("testDefer");
// testDefer(5000).then(
//    function() {
//       console.log("resolved", arguments);
//    },
//    function() {
//       console.log("error", arguments);
//    }
// );
