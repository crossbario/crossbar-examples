## Results

### Loopback TCP / PyPy 2.6 / FreeBSD

```console
(pypy260)[oberstet@brummer1 ~/scm/crossbarexamples/rest/caller_performance]$ make test_local
Testing over loopback TCP with single client and sequential requests
wrk -t1 -c1 -d30s --latency -s wrk/test_add.lua http://127.0.0.1:8080
Running 30s test @ http://127.0.0.1:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   447.25us    3.20ms  46.53ms   98.62%
    Req/Sec     8.65k     0.94k    9.06k    93.08%
  Latency Distribution
     50%   96.00us
     75%  102.00us
     90%  141.00us
     99%   15.19ms
  136851 requests in 30.06s, 31.45MB read
Requests/sec:   4552.96
Transfer/sec:      1.05MB
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   796.93us    4.50ms  46.76ms   97.29%
    Req/Sec     8.60k     0.95k    9.08k    91.33%
  Latency Distribution
     50%   97.00us
     75%  108.00us
     90%  142.00us
     99%   30.41ms
  256799 requests in 30.01s, 59.02MB read
Requests/sec:   8555.72
Transfer/sec:      1.97MB
wrk -t1 -c1 -d30s --latency -s wrk/test_sub.lua http://127.0.0.1:8080
Running 30s test @ http://127.0.0.1:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   725.25us    3.92ms  46.11ms   97.90%
    Req/Sec     4.68k   485.70     4.93k    93.00%
  Latency Distribution
     50%  187.00us
     75%  219.00us
     90%  239.00us
     99%   25.78ms
  139714 requests in 30.01s, 32.24MB read
Requests/sec:   4655.66
Transfer/sec:      1.07MB
wrk -t1 -c1 -d30s --latency -s wrk/test_mul.lua http://127.0.0.1:8080
Running 30s test @ http://127.0.0.1:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   521.82us    3.31ms  46.68ms   98.50%
    Req/Sec     6.22k   519.26     6.55k    93.67%
  Latency Distribution
     50%  142.00us
     75%  163.00us
     90%  175.00us
     99%   17.55ms
  185865 requests in 30.01s, 42.72MB read
Requests/sec:   6194.38
Transfer/sec:      1.42MB
wrk -t1 -c1 -d30s --latency -s wrk/test_div.lua http://127.0.0.1:8080
Running 30s test @ http://127.0.0.1:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   690.86us    3.90ms  45.77ms   97.90%
    Req/Sec     5.51k   546.26     5.82k    93.33%
  Latency Distribution
     50%  159.00us
     75%  188.00us
     90%  202.00us
     99%   25.60ms
  164466 requests in 30.01s, 37.80MB read
Requests/sec:   5479.96
Transfer/sec:      1.26MB
Testing over loopback TCP with multiple clients and concurrent requests
wrk -t4 -c200 -d30s --latency -s wrk/test_add.lua http://127.0.0.1:8080
Running 30s test @ http://127.0.0.1:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    16.76ms    8.72ms 170.71ms   95.48%
    Req/Sec     3.16k   468.63     4.07k    89.43%
  Latency Distribution
     50%   15.11ms
     75%   15.30ms
     90%   15.69ms
     99%   62.23ms
  378528 requests in 30.15s, 87.00MB read
Requests/sec:  12554.63
Transfer/sec:      2.89MB
wrk -t4 -c200 -d30s --latency -s wrk/test_sub.lua http://127.0.0.1:8080
Running 30s test @ http://127.0.0.1:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    24.06ms   10.95ms 184.94ms   92.36%
    Req/Sec     2.17k   437.65     6.49k    84.95%
  Latency Distribution
     50%   21.23ms
     75%   21.59ms
     90%   24.40ms
     99%   66.51ms
  258750 requests in 30.09s, 59.72MB read
Requests/sec:   8599.62
Transfer/sec:      1.98MB
wrk -t4 -c200 -d30s --latency -s wrk/test_mul.lua http://127.0.0.1:8080
Running 30s test @ http://127.0.0.1:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    19.60ms   10.62ms 161.17ms   92.93%
    Req/Sec     2.75k   529.79     4.04k    77.77%
  Latency Distribution
     50%   16.54ms
     75%   16.94ms
     90%   24.91ms
     99%   62.60ms
  327473 requests in 30.06s, 75.26MB read
Requests/sec:  10892.17
Transfer/sec:      2.50MB
wrk -t4 -c200 -d30s --latency -s wrk/test_div.lua http://127.0.0.1:8080
Running 30s test @ http://127.0.0.1:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    22.14ms   10.71ms 178.31ms   92.55%
    Req/Sec     2.37k   443.95     3.03k    75.04%
  Latency Distribution
     50%   19.36ms
     75%   19.75ms
     90%   22.83ms
     99%   65.23ms
  283391 requests in 30.16s, 65.13MB read
Requests/sec:   9395.31
Transfer/sec:      2.16MB
```
