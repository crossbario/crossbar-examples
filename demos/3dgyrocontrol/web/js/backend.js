// the URL of the WAMP Router (Crossbar.io)
//
var wsuri;
var sessionvar;

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
   realm: "realm1"
});

function callbackgyro(o) {
    sessionvar.publish ('com.example.image',[JSON.stringify(o)]);
    document.getElementById('WAMPEvent').innerHTML =JSON.stringify(o ,undefined, 2);

    }
 
connection.onopen = function (session) {

   console.log("connected");
   document.getElementById('WAMPEvent').innerHTML =  "connected";

   sessionvar = session;
   gyro.frequency = 0.1;
   gyro.startTracking(callbackgyro);

};
document.getElementById('WAMPEvent').innerHTML = "connecting .......";

connection.open();
