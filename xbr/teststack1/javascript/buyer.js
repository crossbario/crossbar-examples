var autobahn = require('autobahn');

console.log("Buyer running AutobahnJS " + autobahn.version);

const url = process.env.CBURL;
const realm = process.env.CBREALM;

console.log("Buyer connecting to " + url + " (realm " + realm + ") ..");

var connection = new autobahn.Connection({url: url, realm: realm});

connection.onopen = function (session, details) {
   console.log("Buyer session open!", details);
   // connection.close();
};

connection.onclose = function (reason, details) {
   console.log("Buyer session closed: " + reason, details);
}

connection.open();
