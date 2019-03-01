import ws from "k6/ws";
import { check } from "k6";

// binary websocket currently not supported by k6
// https://docs.k6.io/docs/socketsend
//const msg = Array(262144).join('x');
const msg = Array(64).join('x');
const msg_count = 268435456 / msg.length;

export default function() {
    var url = "ws://127.0.0.1:8080";
    var count = msg_count;

    var res = ws.connect(url, {}, function(socket) {
        socket.on('open', function() {
        socket.send(msg);
    });

    socket.on('message', function(data) {
        count -= 1;
        if (!count) {
          socket.close();
        } else {
          socket.send(msg);
        }
    });

    socket.on('close', function() {
    });
  });

  check(res, { "status is 101": (r) => r && r.status === 101 });
}
