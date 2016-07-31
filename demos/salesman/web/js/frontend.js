// work in progress - expect this to fail at the moment!

console.log("frontend loaded");

// KnockoutJS viewmodel
// Instantiate and bind the viewmodel
var vm = new ViewModel();
ko.applyBindings(vm);

function ViewModel () {

   var self = this;

   self.isRunning = ko.observable(false);
   self.connectedNodes = ko.observable(0);
   self.localComputeNodeRegistered = ko.observable(false);

   self.startComputation = function() {
      // call the orchestrator to start a new computation run;
   }

   self.numberOfCities = ko.observable(0);
   // self.points = ko.observable([]);
   self.points = [];
   self.initialRouter = [];
   self.initialLength = ko.observable(0);
   self.currentBestRoute = [];
   self.currentBestLength = ko.observable(0);
   self.temp = ko.observable(0);
   self.runningComputeNodes = self.connectedNodes;
   self.iterationsPerSecond = ko.observable(0);

   self.registerLocalComputeNode = function() {
      console.log("registerLocalComputeNode called"),
      registerComputeNode();
      // feedback based on whether the registration suceeded not trivial,
      // so simulating for now - FIXME!
      self.localComputeNodeRegistered(true);
   }

   //
   // no necessity to have the rest below in the view model,
   // but this way it stays separate from the compute_tsp code
   //

   var onDemoStateUpdate = function(args, kwargs, details) {
      console.log("onDemoStateUpdate", args);

      var property = args[0];
      var value = args[1];

      self[property](value);

   };


   var onComputationStateUpdate = function(args, kwargs, details) {
      console.log("onComputationStateUpdate", args);

      var property = args[0];
      var value = args[1];

      // we have both ko observables and object/primitives, so distinguish
      // how to assign the value
      if(typeof(self[property]) != "function") {
         self[property] = value;
      } else {
         self[property](value);
      }

      if(property === "currentBestRoute") {
         paint();
      }
   };


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

   var updateStatusline = function (status) {
      document.getElementsByClassName("statusline")[0].innerHTML = status;
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

   var session = null;

   connection.onopen = function(newSession, details) {
      session = newSession;

      console.log("Frontend connected", session.id);


      // update the status line - FIXME!

      // subscribe to demo + computation state update events
      session.subscribe("io.crossbar.demo.tsp.on_demo_state_update", onDemoStateUpdate);
      session.subscribe("io.crossbar.demo.tsp.on_computation_state_update", onComputationStateUpdate);

      // request initial demo state data
      session.call("io.crossbar.demo.tsp.get_demo_state").then(function(res) {
         console.log("get_demo_state:", res);
         // reformat this so that 'onDemoStateUpdate' can process it

         // if computation running: request the state for this
         if(res.isRunning) {
            session.call("io.crossbar.demo.tsp.get_computation_state").then(function(res) {
               // reformat res so that 'onComputationStateUpdate' can process it
            })
         }
      })

   };

   connection.onclose = function(reason, details) {
      console.log("Connection fail: ", reason, details);

      // update the statusline - get from newer demos what we need here in terms of displayed state! - FIXME
   };

   connection.open();


   // code for canvas painting based on https://github.com/abdulfatir/SimulatedAnnealing-TSP, MIT license

   var tsp_canvas = document.getElementById('tsp-canvas');
   var tsp_ctx = tsp_canvas.getContext("2d");

   // should really be two paint functions:
   // - initially paint the points (which do not change)
   // - have second, transparent overlay canvas where the connections are drawn

   var paint = function () {
      console.log("paint called");

      tsp_ctx.clearRect(0,0, tsp_canvas.width, tsp_canvas.height);

      // points
      var pointsLength = self.points.length;

      console.log("paint called", pointsLength);

   	for(var i = 0; i < pointsLength; i++) {
         // console.log("i", i);

   		tsp_ctx.beginPath();
   		tsp_ctx.arc(self.points[i][0], self.points[i][1], 4, 0, 2 * Math.PI);
   		tsp_ctx.fillStyle = "#0000ff";
   		tsp_ctx.strokeStyle = "#000";
   		tsp_ctx.closePath();
   		tsp_ctx.fill();
   		tsp_ctx.lineWidth=1;
   		tsp_ctx.stroke();

      }

      // Links
   	tsp_ctx.strokeStyle = "#ff0000";
   	tsp_ctx.lineWidth=2;
   	tsp_ctx.moveTo(self.points[self.currentBestRoute[0]][0], self.points[self.currentBestRoute[0]][1]);

      for(var i = 0; i < pointsLength - 1; i++)	{
   		tsp_ctx.lineTo(self.points[self.currentBestRoute[i+ 1]][0], self.points[self.currentBestRoute[i + 1]][1]);
   	}
   	tsp_ctx.lineTo(self.points[self.currentBestRoute[0]][0], self.points[self.currentBestRoute[0]][1]);
   	tsp_ctx.stroke();
   	tsp_ctx.closePath();


   };

}
