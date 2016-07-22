// needs to:
   // connect to the backend
   // subscribe to the on_competition_update and on_competition_ended events
   // get the ident of the compute node loaded with it
   // log:
      // the fact that it's connected
      // updates regarding the position of the component (is it 1st or 2nd)
      // final update


var frontend = {
   when: autobahn.when,
   wsuri: null,
   session: null,
   connection: null,
   currentBestLength: 0,
   currentBestRoute: null,
   currentBestSolution: null,
   points: null,
   computeTime: null
};

frontend.when = autobahn.when;

// the URL of the WAMP Router (Crossbar.io)
//
frontend.wsuri = null;

// var computeGroup = "competition";

if (document.location.origin == "file://") {
   frontend.wsuri = "ws://127.0.0.1:8080/ws";

} else {
   frontend.wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws";
}

// the WAMP connection to the Router
//
frontend.connection = new autobahn.Connection({
   url: frontend.wsuri,
   realm: "realm1"
});
frontend.session = null;

frontend.connection.onopen = function(newSession, details) {
   console.log("compute frontend code connected");

   frontend.session = newSession;

   // subscribe to global data
   // for now: just the "new_best_result" event - FIXME
   frontend.session.subscribe("io.crossbar.demo.tsp.new_best_result", frontend.onBestResultReceived);
   // get the points, compute time
   frontend.session.subscribe("io.crossbar.demo.tsp.started", frontend.onDemoStarted);

   // get local stats via local mechanism (a global object)?
   // IMPLEMENT ME - FIXME
};

frontend.connection.onclose = function(reason, details) {
   console.log("Connection fail: ", reason, details);
};

// // connect automatically in NodeJS, but only on user action in browser
// if(!isBrowser) {
//    connection.open();
// } else {
//    // add event listener to connect button
// }

frontend.connection.open();

frontend.onDemoStarted = function(args, kwargs, details) {
   console.log("onDemoStarted", kwargs);

   frontend.points = kwargs.points;
   frontend.computeTime = kwargs.computeTime;
};

frontend.onBestResultReceived = function(args, kwargs, details) {
   console.log("onStatsReceived", kwargs);

   // update the best results part of the stats
   // via the frontend object for now, but move to KO - FIXME
   frontend.currentBestSolution = kwargs;
   frontend.currentBestRoute = kwargs.bestRoute;
   frontend.currentBestLength = kwargs.bestLength;

   // draw the current best route
   frontend.paint();

};


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
