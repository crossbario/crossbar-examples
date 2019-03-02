
https://github.com/observing/thor

wget https://nodejs.org/dist/v10.15.1/node-v10.15.1-linux-x64.tar.xz
sudo tar xvf node-v*.tar.?z --strip-components=1 -C /usr/local && \
node --version


git clone git@github.com:observing/thor.git
cd thor
sudo npm install -g .


thor --amount 5000 ws://localhost:8080







oberstet@matterhorn:~$ k6 run --vus 100 --duration 30s test.js 

          /\      |‾‾|  /‾‾/  /‾/   
     /\  /  \     |  |_/  /  / /    
    /  \/    \    |      |  /  ‾‾\  
   /          \   |  |‾\  \ | (_) | 
  / __________ \  |__|  \__\ \___/ .io

  execution: local
     output: -
     script: test.js

    duration: 30s, iterations: -
         vus: 100, max: 100

    done [==========================================================] 30s / 30s

    ✓ status is 101

    checks................: 100.00% ✓ 257   ✗ 0    
    data_received.........: 6.7 GB  225 MB/s
    data_sent.............: 6.8 GB  225 MB/s
    iteration_duration....: avg=9.75s   min=1.31s  med=10.13s  max=15.45s   p(90)=13.61s  p(95)=14.29s  
    iterations............: 257     8.566645/s
    vus...................: 100     min=100 max=100
    vus_max...............: 100     min=100 max=100
    ws_connecting.........: avg=46.53ms min=7.37ms med=33.44ms max=224.72ms p(90)=87.73ms p(95)=144.91ms
    ws_msgs_received......: 25799   859.964489/s
    ws_msgs_sent..........: 25800   859.997822/s
    ws_session_duration...: avg=9.74s   min=1.3s   med=10.12s  max=15.45s   p(90)=13.6s   p(95)=14.29s  
    ws_sessions...........: 258     8.599978/s

oberstet@matterhorn:~$ k6 run --vus 100 --duration 30s test.js 

          /\      |‾‾|  /‾‾/  /‾/   
     /\  /  \     |  |_/  /  / /    
    /  \/    \    |      |  /  ‾‾\  
   /          \   |  |‾\  \ | (_) | 
  / __________ \  |__|  \__\ \___/ .io

  execution: local
     output: -
     script: test.js

    duration: 30s, iterations: -
         vus: 100, max: 100

    done [==========================================================] 30s / 30s

    ✓ status is 101

    checks................: 100.00% ✓ 360   ✗ 0    
    data_received.........: 9.4 GB  315 MB/s
    data_sent.............: 9.5 GB  315 MB/s
    iteration_duration....: avg=6.84s   min=772.99ms med=6.59s   max=16.77s   p(90)=11.99s  p(95)=16.1s  
    iterations............: 360     11.998914/s
    vus...................: 100     min=100 max=100
    vus_max...............: 100     min=100 max=100
    ws_connecting.........: avg=26.47ms min=1.26ms   med=23.46ms max=124.92ms p(90)=48.07ms p(95)=61.72ms
    ws_msgs_received......: 36196   1206.424139/s
    ws_msgs_sent..........: 36198   1206.4908/s
    ws_session_duration...: avg=6.83s   min=772.65ms med=6.59s   max=16.77s   p(90)=11.98s  p(95)=16.07s 
    ws_sessions...........: 362     12.065575/s

oberstet@matterhorn:~$ 




oberstet@matterhorn:~$ cat test.js
import ws from "k6/ws";
import { check } from "k6";

const msg = Array(262144).join('x');

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
