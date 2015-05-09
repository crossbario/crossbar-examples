require(['knockout', 'autobahn', 'dashboardviewmodel'], function (ko, autobahn, WorkerOverview, ViewModel) {
    // console.log("HERE", ko, autobahn, WorkerOverview, ViewModel);

    ko.components.register('devops-center', {
        require: 'components/devops_center/devops_center.js'
    });

    ko.components.register('stack-switch', {
        require: 'components/stack_switch/stack_switch.js'
    });

    var viewModel = new DasboardViewModel();
    vm = viewModel;

    console.log("viewModel");

    ko.applyBindings({vm: viewModel});  
});



// Establish connection to WAMP router

var session = null;

// the URL of the WAMP Router (Crossbar.io)
//
var wsuri;
if (document.location.origin == "file://") {
   wsuri = "ws://127.0.0.1:8080/ws";
} else {
   wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws";
}

// the WAMP connection to the Router
//
var connection = new autobahn.Connection({
   url: wsuri, // replace with URL of WAMP router if this doesn't serve the file!
   realm: "iot_cookbook"
});


// fired when connection is established and session attached
//
connection.onopen = function (sess, details) {
   console.log("connected");
   session = sess;
};

// fired when connection was lost (or could not be established)
//
connection.onclose = function (reason, details) {
   console.log("Connection lost: " + reason);
}

// now actually open the connection
//
connection.open();


var vm = new DashboardViewModel();
ko.applyBindings(vm);

// create KO viewmodel

var DashboardViewModel = function () {

   var self = this;

   // one object per widget, which is passed to the widget
   self.salesBar = {

   };


   self.productMixPie = {
      products: ["premium", "midTier", "lowEnd"]
   }


}