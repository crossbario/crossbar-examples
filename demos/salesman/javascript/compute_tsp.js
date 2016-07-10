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
var computeGroup = "competition";
if (isBrowser && document.location.origin == "file://") {
   wsuri = "ws://127.0.0.1:8080/ws";

} else if (isBrowser) {
   wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws";
} else {
   console.log("arguments", process.argv[2]);
   wsuri = process.argv[2] || 'ws://127.0.0.1:8080/ws';
   computeGroup = process.argv[3] || 'competition';
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

   // set the URL prefix based on the compute group we are part of
   session.prefix("api", "io.crossbar.demo.tsp." + computeGroup);

   session.register("api:compute_tsp", computeTsp);
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

/*
events are logged in the console. in addition, since we want feedback on mobile browsers as well, where the console is not available, the HTML code loading this compute code may subscribe to events which this may produce (later stage of development - IMPLEMENT ME! FIXME). Events are namespaced via a random int which the page generates and which is accessed by this code via local storage.
*/

var computeTsp = function(args, kwargs, details) {
   var points = kwargs.points;
   var startRoute = kwargs.startRoute;
   var currentBestRoute = startRoute;
   var currentRoute = startRoute;
   var temp = kwargs.temperature;
   var tempDecrease = kwargs.tempDecrease;
   var iterations = kwargs.iterations;

   while(iterations) {
      // get current length
      var currentLength = computeLength(points, currentRoute);
      var currentBestLength = computeLength(points, currentBestRoute); // this should really be cached and only recalculated when a "new best route" flag has been set on the previous iteration - FIXME

      // decide whether to keep the current permutation
      if(
         currentLength < currentBestLength ||
         Math.random() < Math.exp((currentLength - currentBestLength)/temp)
      ) {
         // keep and work from this
         currentBestRoute = currentRoute;
      }

      if(currentLength < currentBestLength) {
         currentBestLength = currentLength;
      }

      // swap currentPoints
      currentRoute = randomSwapTwo(currentRoute);

      temp *= tempDecrease;

      // console.log(iterations, currentLength, currentBestLength);
      console.log(iterations, currentBestRoute.slice(-5));
      iterations--;
   }

   return {
      route: currentBestRoute,
      length: computeLength(points, currentBestRoute)
   };

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

var deepCopyArray = function(array) {
   var copiedArray = [];
   array.forEach(function(el) {
      copiedArray.push(el);
   })
   return copiedArray;
}

// random swap of two points
var randomSwapTwo = function(route) {

   // route is array, and since we don't want to overwrite this, wee need to deep-copy it
   var routeCopy = deepCopyArray(route);

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

   return routeCopy;
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

var testCompute = function() {
   var points = createPoints(30);
   var startRoute = createPointsIndex(points);
   var temp = 1;
   var tempDecrease = 0.95;
   var iterations = 200;

   // console.log("test result: ", computeTsp([], {
   //    points: points,
   //    startRoute: startRoute,
   //    temp: temp,
   //    tempDecrease: tempDecrease,
   //    iterations: iterations
   // }))

   var testResult = session.call("api:compute_tsp", [], {
      points: points,
      startRoute: startRoute,
      temp: temp,
      tempDecrease: tempDecrease,
      iterations: iterations
   });

   testResult.then(function() {
      console.log("test done", arguments);
   });
}
