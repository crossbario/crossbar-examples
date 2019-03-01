import ws from "k6/ws";
import { check } from "k6";

// binary websocket currently not supported by k6
// https://docs.k6.io/docs/socketsend
//const msg = Array(262144).join('x');
const msg = Array(64).join('x');

export default function() {
  var url = "ws://127.0.0.1:8080";
  var params = { "tags": { "my_tag": "hello" } };
  var count = 100;

  var res = ws.connect(url, params, function(socket) {
    socket.on('open', function() {
      //console.log('connected');
      socket.send(msg);
    });

    socket.on('message', function(data) {
      //console.log("Message received: ", data);
      count -= 1;
      if (!count) {
	      socket.close();
      } else {
	      socket.send(msg);
      }
    });

    socket.on('close', function() {
      //console.log('disconnected');
    });
  });

  check(res, { "status is 101": (r) => r && r.status === 101 });
}

