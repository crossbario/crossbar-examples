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
var registrationSub = null;
var unregistrationSub = null;
var computeProcedureUri = "io.crossbar.demo.tsp.compute_tsp";

connection.onopen = function(newSession, details) {
   console.log("Connected");

   session = newSession;

   session.prefix("api", "io.crossbar.demo.tsp");

   // set up the procedures for the clients to call
   session.register("api:get_demo_state", getDemoState);
   session.register("api:get_computation_state", getComputationState);

   // check if there is a registration for the compute_tsp function
   checkRegistration(computeProcedureUri).then(function(regId) {
      console.log("checkRegistration", regId);

      // check if there is a registration
      if(regId != null) {
         startOrchestration(regId);
      }
      // else: do nothing since we check via the registration event
   });

   // we subscribe to the registration created event (no registration exists, or all callees disconnected at some point and this gets re-created when one connects again, so this is in addition to the checkRegistration call above)
   watchCreation(computeProcedureUri, function(regId) {

      startOrchestration(regId);

   });

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

var startOrchestration = function(regId) {
   console.log("start orchestration", regId);
   registrationId = regId;


   // kill a possible previous subscription for the registration
   if(registrationSub) {
      registrationSub.unsubscribe();
   }
   if(unregistrationSub) {
      unregistrationSub.unsubscribe();
   }

   // subscribe to the registration & unregistration events
   // for the procedure now that we have a procedure uri
   // (same happens with the branch that waits for an initial creation of the procedure)
   // - when.all fires when all promises in an array are resolved
   when.all(watchRegistrations(registrationId, updateRegistrations)).then(function(res) {
      console.log("watchRegistrations resolves to ", res);
      registrationSub = res[0];
      unregistrationSub = res[1];
   });

   // retrieve the number of callees and start calling them
   getNumberOfCallees(registrationId).then(function(res) {
      console.log("getNumberOfCallees", res);
      registrations = res;

      orchestrate();
   })
};




// checks whether a registration for a URI exists
var checkRegistration = function(callUri) {

   var isRegistration = when.defer();

   session.call("wamp.registration.match", [callUri]).then(function(res) {
      isRegistration.resolve(res);
   });

   return isRegistration.promise;
};

// filters created procedures for a passed procedure uri
// and calls a passed callback function with the procedure Id
var watchCreation = function(callUri, onCreateCallback) {
   console.log("watchCreation called");
   session.subscribe("wamp.registration.on_create", function(args, kwargs, details) {
      console.log("registration event received, analyzing", args, kwargs, details);

      var registrationUri = args[1].uri;
      if(registrationUri === callUri) {
         var registrationId = args[1].id;
         console.log("registration for callUri received: ", callUri, "calling callback");
         onCreateCallback(registrationId);
      }

   })
};

// returns the number of callees for a registered procedure
var getNumberOfCallees = function(registrationId) {
   var numberOfCallees = when.defer();
   session.call("wamp.registration.count_callees", [registrationId]).then(function(res) {
      // console.log(res);
      numberOfCallees.resolve(res);
   });

   return numberOfCallees.promise;
};


// watches registration & unregistration events
// returns the an array of promises which resolve to the subscription objects
// filters for a particular registration id
// calls the passed callback on registration/unregistration
var watchRegistrations = function(registrationId, onRegisterCallback) {
   console.log("watchRegistrations called");

   var watchRegSub = when.defer();
   var watchUnregSub = when.defer();

   var filter = function(regId) {
      if(regId === registrationId) {
         onRegisterCallback(registrationId);
      }
   };

   session.subscribe("wamp.registration.on_register",
      function(args, kwargs, details) {

         console.log("registration event received, analyzing", args, kwargs, details);

         filter(args[1]);

      }
   ).then(function(subscription) {

      watchRegSub.resolve(subscription);
      // console.log("watchRegistrations subscription", subscription);

   });

   session.subscribe("wamp.registration.on_unregister",
      function(args, kwargs, details) {

         console.log("unregistration event received, analyzing", args, kwargs, details);

         filter(args[1]);

      }
   ).then(function(subscription) {

      watchUnregSub.resolve(subscription);
      // console.log("watchRegistrations subscription", subscription);

   });

   return [watchRegSub.promise, watchUnregSub.promise];
};

// gets the current number of registrations for the compute_tsp functions
// triggered by the registration event
var updateRegistrations = function(registrationId) {
   console.log("updateRegistrations called", registrationId);
   getNumberOfCallees(registrationId).then(function(numberOfCallees) {
      console.log("updated number of callees", numberOfCallees);

      registrations = numberOfCallees;

   })
};

var computationState = null;

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
      this.runningComputeNodes = 0;
      this.iterationsPerSecond = 0;
   });

   computationState = cState;

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
