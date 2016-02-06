var session = null;

// the URL of the WAMP Router (Crossbar.io)
var wsuri;
if (document.location.origin == "file://") {
   wsuri = "ws://127.0.0.1:8080/ws"; // localhost for development
} else {
   wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws"; // URL of the Crossbar.io instance this is served from
}

// the WAMP connection to the Router
//
var connection = new autobahn.Connection({
   url: "ws://127.0.0.1:8080/ws", // replace with the url of your crossbar instance
   realm: "iot_cookbook"
});


// fired when connection is established and session attached
//
connection.onopen = function (sess, details) {
   console.log("connected", details);

   connectingIndicator.style.display = "none";

   session = sess;

   main();

};

function main () {

   // get the current alarm armed & alarm state
   session.call("io.crossbar.examples.iotcookbook.alarmapp.get_alarm_armed").then(
      function(res) {
         if (res === true) {
            setArmed();   
         } else {
            setUnarmed();
         }         
      },
      function(err) {
         console.log("get_alarm_armed error", err);
      }
   )

   session.call("io.crossbar.examples.iotcookbook.alarmapp.get_alarm_active").then(
      function(res) {
         if (res === true) {
            setAlarm();
         } else {
            cancelAlarm();
         }
      },
      function(err) {
         console.log("get_alarm_active error", err);
      }
   )


   // subscribe to changes in the alarm armed & alarm state
   session.subscribe("io.crossbar.examples.iotcookbook.alarmapp.on_alarm_armed", function(args) {
      console.log("armed state changed", args[0]);
      if (args[0] === true) {
         setArmed();   
      } else {
         setUnarmed();
      }  
   })

   session.subscribe("io.crossbar.examples.iotcookbook.alarmapp.on_alarm_active", function(args) {
      console.log("alarm active changed", args[0]);
       if (args[0] === true) {
         setAlarm();
      } else {
         cancelAlarm();
      }      
   })

   // session.subscribe("io.crossbar.iotberlin.alarmapp.keepalive", function(args) {
   //    console.log("io.crossbar.iotberlin.alarmapp.keepalive", args[0]);
   // });
}


// fired when connection was lost (or could not be established)
//
connection.onclose = function (reason, details) {

   console.log("Connection lost: " + reason);

   initialState();

}

// now actually open the connection
//
connection.open();

function hexToBase64(str) {
  return btoa(String.fromCharCode.apply(null,
    str.replace(/\r|\n/g, "").replace(/([\da-fA-F]{2}) ?/g, "0x$1 ").replace(/ +$/, "").split(" "))
  );
}

// cache the elemens we need to manipulate
var alarmIndicator = document.getElementById("alarmIndicator");
var alarmArmedIndicator = document.getElementById("alarmArmedIndicator");
var armButton = document.getElementById("armButton");
var disamButton = document.getElementById("disamButton");
var alarmActions = document.getElementById("alarmActions");
var cancelButton = document.getElementById("cancelButton");
var triggerButton = document.getElementById("triggerButton");
var connectingIndicator = document.getElementById("connectingIndicator");


// attach click event handlers to buttons
armButton.addEventListener("click", function() {
   session.call("io.crossbar.examples.iotcookbook.alarmapp.set_alarm_armed", [true]).then(session.log, session.log);
});

disarmButton.addEventListener("click", function() {
   session.call("io.crossbar.examples.iotcookbook.alarmapp.set_alarm_armed", [false]).then(session.log, session.log);
});

cancelButton.addEventListener("click", function() {
   session.call("io.crossbar.examples.iotcookbook.alarmapp.set_alarm_active", [false]).then(session.log, session.log);
});

triggerButton.addEventListener("click", function() {
   session.call("io.crossbar.examples.iotcookbook.alarmapp.set_alarm_active", [true]).then(session.log, session.log);
});


// functions for setting interface states

var initialState = function () {
   alarmArmedIndicator.style.backgroundColor = "white";
   alarmIndicator.style.display = "none";
   armButton.style.display = "none";
   disarmButton.style.display = "none";
   cancelButton.style.display = "none";
   triggerButton.style.display = "none";
   connectingIndicator.style.display = "block";
}
initialState();

var setArmed = function () {
   alarmArmedIndicator.style.backgroundColor = "red";
   armButton.style.display = "none";
   disarmButton.style.display = "inline-block";
};

var setUnarmed = function () {
   alarmArmedIndicator.style.backgroundColor = "green";
   armButton.style.display = "inline-block";
   disarmButton.style.display = "none";
};

var setAlarm = function () {
   alarmIndicator.style.display = "block";
   cancelButton.style.display = "inline-block";
   triggerButton.style.display = "none";
};

var cancelAlarm = function () {
   alarmIndicator.style.display = "none";
   cancelButton.style.display = "none";
   triggerButton.style.display = "inline-block";
};




