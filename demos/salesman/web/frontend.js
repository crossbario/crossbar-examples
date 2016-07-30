// work in progress - expect this to fail at the moment!

console.log("loaded");


// KnockoutJS viewmodel
// Instantiate and bind the viewmodel
var vm = new ViewModel();
ko.applyBindings(vm);

function ViewModel () {

   var self = this;

   self.isRunning = ko.observable(false);
   self.connectedNodes = ko.observable(0);
   self.localComputeNodeConnected = ko.observable(false);

   self.startComputation = function() {
      // call the orchestrator to start a new computation run;
   }

   self.numberOfCities = ko.observable(0);
   self.initialRouteLength = ko.observable(0);
   self.currentBestRouteLength = ko.observable(0);
   self.currentTemperature = ko.observable(0);
   self.runningComputeNodes = self.connectedNodes;
   self.iterationsPerSecond = ko.observable(0);

}

var onDemoStateUpdate = function(args, kwargs, details) {

};


var onComputationStateUpdate = function(args, kwargs, details) {

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
   console.log("Connected");

   session = newSession;

   // update the status line - FIXME!

   // subscribe to demo + computation state update events
   session.subscribe("io.crossbar.demo.tsp.on_demo_state_update", onDemoStateUpdate);
   session.subscribe("io.crossbar.demo.tsp.on_computation_state_update", onComputationStateUpdate);

   // request initial demo state data
   session.call("io.crossbar.demo.tsp.get_demo_state").then(function(res) {
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

frontend.tsp_canvas = document.getElementById('tsp-canvas');
frontend.tsp_ctx = frontend.tsp_canvas.getContext("2d");

// should really be two paint functions:
// - initially paint the points (which do not change)
// - have second, transparent overlay canvas where the connections are drawn
frontend.paint = function () {
   console.log("paint called");

   frontend.tsp_ctx.clearRect(0,0, frontend.tsp_canvas.width, frontend.tsp_canvas.height);

   // points
   var pointsLength = frontend.points.length;

   // console.log("paint called", pointsLength);

	for(var i = 0; i < pointsLength; i++) {
      // console.log("i", i);

		frontend.tsp_ctx.beginPath();
		frontend.tsp_ctx.arc(frontend.points[i][0], frontend.points[i][1], 4, 0, 2 * Math.PI);
		frontend.tsp_ctx.fillStyle = "#0000ff";
		frontend.tsp_ctx.strokeStyle = "#000";
		frontend.tsp_ctx.closePath();
		frontend.tsp_ctx.fill();
		frontend.tsp_ctx.lineWidth=1;
		frontend.tsp_ctx.stroke();

   }

   // Links
	frontend.tsp_ctx.strokeStyle = "#ff0000";
	frontend.tsp_ctx.lineWidth=2;
	frontend.tsp_ctx.moveTo(frontend.points[frontend.currentBestRoute[0]][0], frontend.points[frontend.currentBestRoute[0]][1]);

   for(var i = 0; i < pointsLength - 1; i++)	{
		frontend.tsp_ctx.lineTo(frontend.points[frontend.currentBestRoute[i+ 1]][0], frontend.points[frontend.currentBestRoute[i + 1]][1]);
	}
	frontend.tsp_ctx.lineTo(frontend.points[frontend.currentBestRoute[0]][0], frontend.points[frontend.currentBestRoute[0]][1]);
	frontend.tsp_ctx.stroke();
	frontend.tsp_ctx.closePath();


};
