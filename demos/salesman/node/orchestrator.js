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

   session.prefix("api", "io.crossbar.demo.tsp");

   startOrchestration();

};

connection.onclose = function(reason, details) {
   console.log("Connection fail: ", reason, details);
};

connection.open();

var startOrchestration = function() {
  // we check whether there are any registered components, and only start once there are
  // check whether any compute nodes for our computeGroup are present, if so: start, else subscribe to the join event and start when this is called the first time
  session.call("wamp.registration.match", ["io.crossbar.demo.tsp.compute_tsp"]).then(function(res) {

     console.log("wamp.registration.match", res);

     if(res !== null) {

        // start calling them
        console.log("computeTsp registered, starting calling");

        orchestrate();

     } else {

        console.log("computeTsp not registered, subscribe to registration event");

        var sub = session.subscribe("wamp.registration.on_create", function(args, kwargs, details) {
           console.log("registration event received, analyzing");
           // filter this for the first registration for "io.crossbar.demo.tsp." + computeGroup + ".compute_tsp"
           var registrationUri = args[1].uri;
           if(registrationUri === "io.crossbar.demo.tsp.compute_tsp") {
              console.log("registration for computeTsp received, starting calling");
              // session.unsubscribe(sub);

              // start the calling of compute nodes
              orchestrate();
           }

        });
     }
  }, session.log);

};

var orchestrate = function() {
  console.log("orchestrate called");

  // we create the problem to be solved
  var points = createPoints(50, [300, 300], 5);
  var initialRoute = createPointsIndex(points);
  var initialLength =  computeLength(points, initialRoute);
  var routeToSend = initialRoute;
  var currentBestRoute = initialRoute;
  var currentBestLength = initialLength;
  var temp = 1;
  var tempDecrease = 0.97;
  var solutions = [];

  console.log("we are computing a better solution for", points, initialRoute, initialLength);

  var process = function(res) {
    // console.log("all calls back", res);

    res.forEach(function(el, i) {
      if(el.length < currentBestLength) {
        currentBestLength = el.length;
        currentBestRoute = el.route;
      }
    });

    temp *= tempDecrease;

    if(temp > 0.01) {
        call();
    } else {
      console.log("computed", currentBestRoute, currentBestLength, "original length was", initialLength);
    }
  };

   var call = function() {
      console.log("issuing calls");

      var calls = [];
      // below only scales up to max concurrency 30 across all nodes
      // we could watch the registrations for our topic and adjust this,
      // or work without queueing (see the crossbar config) and handle errors on max concurrency reached as back pressure
      for(var i = 0; i < 30; i++) {
         // issue call and push to array of deferreds
         calls.push(session.call("api:compute_tsp", [], {
            points: points,
            startRoute: routeToSend,
            temp: temp,
            iterations: 400
         }));
      }
      // when all calls return and deferreds are resolved, we trigger processing the results
      when.all(calls).then(process);
   };
   call();

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
