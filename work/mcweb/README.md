https://github.com/oberstet/scratchbox/tree/master/python/twisted/sharedsocket

# Intel E1340 v3

## 8 Workers, JSON

```console
[oberstet@brummer1 ~/scm/crossbarexamples/work/mcweb]$ make test_json
weighttp -n 5000000 -c 128 -t 8 -k http://10.0.1.3:8080/json
weighttp 0.3 - a lightweight and simple webserver benchmarking tool

starting benchmark...
spawning thread #1: 16 concurrent requests, 625000 total requests
spawning thread #2: 16 concurrent requests, 625000 total requests
spawning thread #3: 16 concurrent requests, 625000 total requests
spawning thread #4: 16 concurrent requests, 625000 total requests
spawning thread #5: 16 concurrent requests, 625000 total requests
spawning thread #6: 16 concurrent requests, 625000 total requests
spawning thread #7: 16 concurrent requests, 625000 total requests
spawning thread #8: 16 concurrent requests, 625000 total requests
progress:  10% done
progress:  20% done
progress:  30% done
progress:  40% done
progress:  50% done
progress:  60% done
progress:  70% done
progress:  80% done
progress:  90% done
progress: 100% done

finished in 29 sec, 821 millisec and 497 microsec, 167664 req/s, 48629 kbyte/s
requests: 5000000 total, 5000000 started, 5000000 done, 5000000 succeeded, 0 failed, 0 errored
status codes: 5000000 2xx, 0 3xx, 0 4xx, 0 5xx
traffic: 1485000000 bytes total, 1105000000 bytes http, 380000000 bytes data
wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/json
Running 1m test @ http://10.0.1.3:8080/json
  8 threads and 128 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.01ms    2.06ms  97.57ms   96.44%
    Req/Sec    23.38k     2.44k   28.91k    66.22%
  Latency Distribution
     50%  627.00us
     75%  846.00us
     90%    1.05ms
     99%   13.39ms
  11185892 requests in 1.00m, 3.09GB read
Requests/sec: 186121.22
Transfer/sec:     52.72MB
[oberstet@brummer1 ~/scm/crossbarexamples/work/mcweb]$ make test_json
weighttp -n 5000000 -c 128 -t 8 -k http://10.0.1.3:8080/json
weighttp 0.3 - a lightweight and simple webserver benchmarking tool

starting benchmark...
spawning thread #1: 16 concurrent requests, 625000 total requests
spawning thread #2: 16 concurrent requests, 625000 total requests
spawning thread #3: 16 concurrent requests, 625000 total requests
spawning thread #4: 16 concurrent requests, 625000 total requests
spawning thread #5: 16 concurrent requests, 625000 total requests
spawning thread #6: 16 concurrent requests, 625000 total requests
spawning thread #7: 16 concurrent requests, 625000 total requests
spawning thread #8: 16 concurrent requests, 625000 total requests
progress:  10% done
progress:  20% done
progress:  30% done
progress:  40% done
progress:  50% done
progress:  60% done
progress:  70% done
progress:  80% done
progress:  90% done
progress: 100% done

finished in 29 sec, 380 millisec and 928 microsec, 170178 req/s, 49358 kbyte/s
requests: 5000000 total, 5000000 started, 5000000 done, 5000000 succeeded, 0 failed, 0 errored
status codes: 5000000 2xx, 0 3xx, 0 4xx, 0 5xx
traffic: 1485000000 bytes total, 1105000000 bytes http, 380000000 bytes data
wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/json
Running 1m test @ http://10.0.1.3:8080/json
  8 threads and 128 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.01ms    2.04ms  32.96ms   96.34%
    Req/Sec    23.46k     2.30k   30.29k    69.80%
  Latency Distribution
     50%  644.00us
     75%  805.00us
     90%    1.01ms
     99%   13.63ms
  11221191 requests in 1.00m, 3.10GB read
Requests/sec: 186708.55
Transfer/sec:     52.88MB
[oberstet@brummer1 ~/scm/crossbarexamples/work/mcweb]$ make test_json
weighttp -n 5000000 -c 128 -t 8 -k http://10.0.1.3:8080/json
weighttp 0.3 - a lightweight and simple webserver benchmarking tool

starting benchmark...
spawning thread #1: 16 concurrent requests, 625000 total requests
spawning thread #2: 16 concurrent requests, 625000 total requests
spawning thread #3: 16 concurrent requests, 625000 total requests
spawning thread #4: 16 concurrent requests, 625000 total requests
spawning thread #5: 16 concurrent requests, 625000 total requests
spawning thread #6: 16 concurrent requests, 625000 total requests
spawning thread #7: 16 concurrent requests, 625000 total requests
spawning thread #8: 16 concurrent requests, 625000 total requests
progress:  10% done
progress:  20% done
progress:  30% done
progress:  40% done
progress:  50% done
progress:  60% done
progress:  70% done
progress:  80% done
progress:  90% done
progress: 100% done

finished in 29 sec, 478 millisec and 39 microsec, 169617 req/s, 49195 kbyte/s
requests: 5000000 total, 5000000 started, 5000000 done, 5000000 succeeded, 0 failed, 0 errored
status codes: 5000000 2xx, 0 3xx, 0 4xx, 0 5xx
traffic: 1485000000 bytes total, 1105000000 bytes http, 380000000 bytes data
wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/json
Running 1m test @ http://10.0.1.3:8080/json
  8 threads and 128 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.00ms    2.07ms  65.58ms   96.44%
    Req/Sec    23.48k     2.01k   29.29k    70.28%
  Latency Distribution
     50%  621.00us
     75%  841.00us
     90%    1.10ms
     99%   13.40ms
  11232626 requests in 1.00m, 3.11GB read
Requests/sec: 186899.87
Transfer/sec:     52.94MB
[oberstet@brummer1 ~/scm/crossbarexamples/work/mcweb]$
```

