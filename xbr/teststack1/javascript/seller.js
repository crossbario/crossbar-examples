var autobahn = require('autobahn');

console.log("Seller running AutobahnJS " + autobahn.version);

const url = process.env.CBURL;
const realm = process.env.CBREALM;

console.log("Seller connecting to " + url + " (realm " + realm + ") ..");

var connection = new autobahn.Connection({url: url, realm: realm});

connection.onopen = function (session, details) {
   console.log("Seller session open!", details);
   // connection.close();
};

connection.onclose = function (reason, details) {
   console.log("Seller session closed: " + reason, details);
}

connection.open();
