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
var controlUrl = "googlechrome://navigate?url="+document.location.origin + "/backend.html" ;
var controlUrl1 =  document.location.origin + "/backend.html" ;

var codeDiv = document.getElementById("qrcode");
var codeDiv1 = document.getElementById("qrcode1");
codeDiv.innerHTML = "";
codeDiv1.innerHTML = "";

new QRCode(codeDiv, controlUrl);
new QRCode(codeDiv1, controlUrl1);
document.getElementById("directlink").href = controlUrl1 ;


var xvalue = 0, yvalue = 0, zvalue = 0;
  
var camera, scene, renderer;
var geometry, material, mesh;

init();
animate();

function init() {

	camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 0.01, 10 );
	camera.position.z = 1;

	scene = new THREE.Scene();

	geometry = new THREE.BoxGeometry( 0.2, 0.05, 0.4 );
	material = new THREE.MeshNormalMaterial();

	mesh = new THREE.Mesh( geometry, material );
	scene.add( mesh );

	renderer = new THREE.WebGLRenderer( { antialias: true } );
	renderer.setSize( window.innerWidth, window.innerHeight/2 );
	document.body.appendChild( renderer.domElement );

}

function animate() {
	mesh.rotation.x = xvalue;
	mesh.rotation.y = yvalue;
        mesh.rotation.z = zvalue;
	renderer.render( scene, camera );
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

 
connection.onopen = function (session) {

      function VRCam (args) {
            obj = JSON.parse(args);
            xvalue = obj.beta/30;
            yvalue = obj.alpha/30;
            zvalue = obj.gamma/30;
            requestAnimationFrame( animate );
}

session.subscribe('com.example.image', VRCam).then(
   function (sub) {
       console.log('subscribed to topic');
   },
   function (err) {
      console.log('failed to subscribe to topic', err);
   }
);


};

connection.open();
