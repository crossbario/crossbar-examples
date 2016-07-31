console.log("loaded");

try {
   // for Node.js
   var autobahn = require('autobahn');
   var ko = require('knockout');
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
   realm: "crossbardemo"
});
var session = null;
var registrationId = null;
var registrations = 0;

connection.onopen = function(newSession, details) {
   console.log("Connected");

   session = newSession;

   session.prefix("api", "io.crossbar.demo.tsp");

   // set up the procedures for the clients to call
   session.register("api:get_demo_state", getDemoState);
   session.register("api:get_computation_state", getComputationState);

   // we check if there is a registration for the compute_tsp function
   // if so, we retrieve the number of callees and start calling them
   // we subscribe to the registration created event (no registration exists, or all callees disconnected at some point and this gets re-created when one connects again)
   // we also subscribe to the events for existing registrations (register, unregister, delete) and filter these based on the registation ID either of the above actions has retrieved


   // startOrchestration();

};

connection.onclose = function(reason, details) {
   console.log("Connection fail: ", reason, details);
};

connection.open();

var demoState = {
   isRunning: false,
   connectedNodes: 0,
   registrationId: null // id of the registration for the "io.crossbar.demo.tsp.compute_tsp", if any
};

var computationState = {
   numberOfCities: 0,
   points: [],
   initialRoute: [],
   initialLength: 0,
   currentBestRoute: [],
   currentBestLength: 0,
   temp: 1,
   runningComputeNodes: 0,
   iterationsPerSecond: 0
};

var updateDemoState = function(property, value) {
   // we update the property
   demoState[property] = value;

   // we publish the changed state
   session.publish("api:on_demo_state_update", [property, value]);
};

var updateComputationState = function(property, value) {
   console.log("updateComputationState called", property, value);
   // we update the property
   computationState[property] = value;

   // we publish the changed state
   session.publish("api:on_computation_state_update", [property, value]);
};


var getDemoState = function() {
   console.log("getDemoState called");
   // return "functionality not implemented yet";
   return demoState;
};

var getComputationState = function() {
   console.log("getComputationState called");
   // return "functionality not implemented yet";
   return computationState;
};




var startOrchestration = function() {
   // we check whether there are any registered components, and only start once there are
   // check whether any compute nodes for our computeGroup are present, if so: start, else subscribe to the join event and start when this is called the first time
   session.call("wamp.registration.match", ["io.crossbar.demo.tsp.compute_tsp"]).then(function(res) {

      console.log("wamp.registration.match", res);

      if(res !== null) {

         // start calling them
         console.log("computeTsp registered, starting calling");

         // store the registration Id
         registrationId = res;

         orchestrate();

      } else {

         console.log("computeTsp not registered, subscribe to registration event");

         var sub = session.subscribe("wamp.registration.on_create", function(args, kwargs, details) {
            console.log("registration event received, analyzing");
            // filter this for the first registration for "io.crossbar.demo.tsp." + computeGroup + ".compute_tsp"
            var registrationUri = args[1].uri;
            if(registrationUri === "io.crossbar.demo.tsp.compute_tsp") {
               console.log("registration for computeTsp received, starting calling", args);
               // we cancel the subscription since the orchestration should only be triggered once
               // session.unsubscribe(sub);
               console.log("sub", sub);
               registrationId = args[1].id;

               // start the calling of compute nodes
               orchestrate();
            }

         });
      }
   }, session.log);

};

var checkRegistration = function(callUri) {
   var isRegistration = when.defer();

   session.call("wamp.registration.match", [callUri]).then(function(res) {
      isRegistration.resolve(res);
   });

   return isRegistration.promise;
};

var getNumberOfCallees = function(registrationId) {
   var numberOfCallees = when.defer();
   session.call("wamp.registration.count_callees", [registrationId]).then(function(res) {
      // console.log(res);
      numberOfCallees.resolve(res);
   });

   return numberOfCallees.promise;
};

var watchRegistrations = function(callUri, onRegisterCallback) {
   var sub = session.subscribe("wamp.registration.on_register", function(args, kwargs, details) {
      console.log("registration event received, analyzing", args, kwargs, details);


      // filter this for the first registration for "io.crossbar.demo.tsp." + computeGroup + ".compute_tsp"
      // var registrationUri = args[1].uri;
      // if(registrationUri === callUri) {
      //    console.log("registration for computeTsp received, starting calling", args);
      //    // we cancel the subscription since the orchestration should only be triggered once
      //    // session.unsubscribe(sub);
      //
      //    registrationId = args[1].id;
      //
      //    // start the calling of compute nodes
      //    // orchestrate();
      //    onRegisterCallback(registrationId);
      // }

   });
};

var orchestrate = function() {
   console.log("orchestrate called");

   // we update the demo state
   updateDemoState("isRunning", true);

   // create object and reference other object properties
   // in a compact way
   var cState = new (function() {
      this.numberOfCities = 50;
      this.points = createPoints(this.numberOfCities, [300, 300], 5);
      this.initialRoute = createPointsIndex(this.points);
      this.initialLength =  computeLength(this.points, this.initialRoute);
      this.routeToSend = this.initialRoute;
      this.currentBestRoute = this.initialRoute;
      this.currentBestLength = this.initialLength;
      this.temp = 1;
      this.tempDecrease = 0.97;
   });

   // we update the computation state with our initial values
   var vals = ["numberOfCities", "points", "initialRoute", "initialLength", "currentBestRoute", "currentBestLength", "temp"];

   vals.forEach(function(el) {
      updateComputationState(el, cState[el]);
   });

   console.log("we are computing a better solution for", cState.points, cState.initialRoute, cState.initialLength);

   call(cState);

};

var call = function(cState) {
   // console.log("start issuing calls for temperature ", temp);

   // we check what the number of callees for our current registrationId is
   // if the registration does not exist anymore, we pause, subscribe to the registration creation event and re-start once there is a registration for our procedure
   // if there are callees for the procudure, then we adjust the # of calls upwards if it exceeds the minimum number of calls we make on each temp setting

   var calls = [];
   // below only scales up to max concurrency 30 across all nodes
   // we could watch the registrations for our topic and adjust this,
   // or work without queueing (see the crossbar config) and handle errors on max concurrency reached as back pressure
   for(var i = 0; i < 5; i++) {
      // issue call and push to array of deferreds
      calls.push(session.call("api:compute_tsp", [], {
         points: cState.points,
         startRoute: cState.routeToSend,
         temp: cState.temp,
         iterations: 400
      }));
   }

   // when all calls return and deferreds are resolved, we trigger processing the results
   when.all(calls).then(function(res) {
      process(res, cState);
   });
};

var process = function(res, cState) {
   //  console.log("all calls back", res);

   res.forEach(function(el, i) {
      if(el.length < cState.currentBestLength) {
         // cState.currentBestLength = el.length;
         // cState.currentBestRoute = el.route;
         updateComputationState("currentBestLength", el.length);
         updateComputationState("currentBestRoute", el.route);
      }
   });

   // ??? - without the second line (direct setting of value) temp does not change  ??? - FIXME
   var newTemp = cState.temp * cState.tempDecrease;
   cState.temp *= cState.tempDecrease;
   console.log("temps", newTemp, cState.temp);
   updateComputationState("temp", newTemp);

   if(cState.temp > 0.01) {
      call(cState);
   } else {
      console.log("computed", cState.currentBestRoute, cState.currentBestLength, "original length was", cState.initialLength);

      updateDemoState("isRunning", false);
   }
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
   console.log("createPointsIndex", points);

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
