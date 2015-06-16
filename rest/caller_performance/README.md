## Results

All tests were run on FreeBSD 10.1 and PyPy 2.6. Tests were run multiple times before measuring (to let PyPy's JIT warmup on hot code paths).

### Sequential Requests over Loopback TCP

```console
(pypy260)[oberstet@brummer1 ~/scm/crossbarexamples/rest/caller_performance]$ make test_local_sequential
Testing over loopback TCP with single client and sequential requests
wrk -t1 -c1 -d30s --latency -s wrk/test_add.lua http://127.0.0.1:8080
Running 30s test @ http://127.0.0.1:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.17ms    7.12ms 134.67ms   97.03%
    Req/Sec     8.55k     1.13k    9.08k    90.37%
  Latency Distribution
     50%   96.00us
     75%  107.00us
     90%  146.00us
     99%   39.01ms
  256233 requests in 30.11s, 58.89MB read
Requests/sec:   8508.83
Transfer/sec:      1.96MB
wrk -t1 -c1 -d30s --latency -s wrk/test_sub.lua http://127.0.0.1:8080
Running 30s test @ http://127.0.0.1:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   631.63us    4.19ms  56.48ms   97.97%
    Req/Sec     8.79k     1.11k    9.23k    95.35%
  Latency Distribution
     50%   97.00us
     75%  102.00us
     90%  128.00us
     99%   23.51ms
  263393 requests in 30.11s, 84.15MB read
Requests/sec:   8748.65
Transfer/sec:      2.80MB
wrk -t1 -c1 -d30s --latency -s wrk/test_mul.lua http://127.0.0.1:8080
Running 30s test @ http://127.0.0.1:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   540.99us    3.61ms  52.60ms   98.59%
    Req/Sec     6.22k   546.81     6.53k    95.35%
  Latency Distribution
     50%  142.00us
     75%  163.00us
     90%  176.00us
     99%   17.41ms
  186287 requests in 30.11s, 42.82MB read
Requests/sec:   6187.85
Transfer/sec:      1.42MB
wrk -t1 -c1 -d30s --latency -s wrk/test_div.lua http://127.0.0.1:8080
Running 30s test @ http://127.0.0.1:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   741.84us    4.31ms  51.23ms   97.95%
    Req/Sec     5.49k   575.49     5.80k    93.00%
  Latency Distribution
     50%  159.00us
     75%  188.00us
     90%  202.00us
     99%   28.13ms
  163875 requests in 30.01s, 37.66MB read
Requests/sec:   5460.99
Transfer/sec:      1.26MB
```

### Concurrent Requests over Loopback TCP

```console
(pypy260)[oberstet@brummer1 ~/scm/crossbarexamples/rest/caller_performance]$ make test_local_concurrent
Testing over loopback TCP with multiple clients and concurrent requests
wrk -t4 -c200 -d30s --latency -s wrk/test_add.lua http://127.0.0.1:8080
Running 30s test @ http://127.0.0.1:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    16.78ms    7.64ms  96.42ms   95.86%
    Req/Sec     3.14k   482.13     5.04k    90.25%
  Latency Distribution
     50%   15.21ms
     75%   15.41ms
     90%   15.82ms
     99%   66.53ms
  375341 requests in 30.07s, 86.27MB read
Requests/sec:  12483.91
Transfer/sec:      2.87MB
wrk -t4 -c200 -d30s --latency -s wrk/test_sub.lua http://127.0.0.1:8080
Running 30s test @ http://127.0.0.1:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    17.53ms    9.17ms 104.69ms   95.38%
    Req/Sec     3.05k   513.94     4.53k    89.17%
  Latency Distribution
     50%   15.59ms
     75%   15.73ms
     90%   16.09ms
     99%   75.74ms
  365178 requests in 30.09s, 116.67MB read
Requests/sec:  12136.01
Transfer/sec:      3.88MB
wrk -t4 -c200 -d30s --latency -s wrk/test_mul.lua http://127.0.0.1:8080
Running 30s test @ http://127.0.0.1:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    19.50ms   10.06ms 101.00ms   92.89%
    Req/Sec     2.74k   561.14     5.89k    78.53%
  Latency Distribution
     50%   16.55ms
     75%   16.87ms
     90%   22.75ms
     99%   65.80ms
  328270 requests in 30.12s, 75.45MB read
Requests/sec:  10897.36
Transfer/sec:      2.50MB
wrk -t4 -c200 -d30s --latency -s wrk/test_div.lua http://127.0.0.1:8080
Running 30s test @ http://127.0.0.1:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    22.28ms   10.03ms 103.21ms   93.04%
    Req/Sec     2.36k   479.87     3.03k    74.75%
  Latency Distribution
     50%   19.41ms
     75%   19.76ms
     90%   24.87ms
     99%   69.09ms
  282504 requests in 30.09s, 64.93MB read
Requests/sec:   9389.81
Transfer/sec:      2.16MB
```

### Sequential Requests over 10GbE

```console
[oberstet@brummer2 ~/scm/crossbarexamples/rest/caller_performance]$ make test_network_sequential
Testing over 10GbE TCP with single client and sequential requests
wrk -t1 -c1 -d30s --latency -s wrk/test_add.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   773.63us    4.56ms  52.35ms   97.78%
    Req/Sec     6.41k   742.15     6.70k    95.00%
  Latency Distribution
     50%  136.00us
     75%  140.00us
     90%  187.00us
     99%   30.33ms
  191402 requests in 30.00s, 43.99MB read
Requests/sec:   6379.78
Transfer/sec:      1.47MB
wrk -t1 -c1 -d30s --latency -s wrk/test_sub.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   526.56us    3.66ms  57.17ms   98.57%
    Req/Sec     6.58k   594.90     6.80k    96.00%
  Latency Distribution
     50%  137.00us
     75%  140.00us
     90%  166.00us
     99%   13.58ms
  196463 requests in 30.01s, 62.77MB read
Requests/sec:   6547.39
Transfer/sec:      2.09MB
wrk -t1 -c1 -d30s --latency -s wrk/test_mul.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   496.55us    3.22ms  52.14ms   98.88%
    Req/Sec     5.08k   419.93     5.25k    97.00%
  Latency Distribution
     50%  178.00us
     75%  202.00us
     90%  212.00us
     99%    8.31ms
  151571 requests in 30.00s, 34.84MB read
Requests/sec:   5051.96
Transfer/sec:      1.16MB
wrk -t1 -c1 -d30s --latency -s wrk/test_div.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   688.74us    3.94ms  51.09ms   98.24%
    Req/Sec     4.58k   436.38     4.77k    94.33%
  Latency Distribution
     50%  195.00us
     75%  225.00us
     90%  239.00us
     99%   24.09ms
  136772 requests in 30.00s, 31.44MB read
Requests/sec:   4558.39
Transfer/sec:      1.05MB
```

### Concurrent Requests over 10GbE

```console
[oberstet@brummer2 ~/scm/crossbarexamples/rest/caller_performance]$ make test_network_concurrent
Testing over 10GbE TCP with multiple clients and concurrent requests
wrk -t4 -c200 -d30s --latency -s wrk/test_add.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    18.23ms    8.51ms 100.17ms   94.45%
    Req/Sec     2.90k   488.28     9.52k    88.18%
  Latency Distribution
     50%   16.46ms
     75%   16.72ms
     90%   17.06ms
     99%   68.11ms
  346765 requests in 30.14s, 79.70MB read
Requests/sec:  11504.10
Transfer/sec:      2.64MB
wrk -t4 -c200 -d30s --latency -s wrk/test_sub.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    18.22ms    8.97ms 100.32ms   95.91%
    Req/Sec     2.92k   456.83     3.41k    89.67%
  Latency Distribution
     50%   16.37ms
     75%   16.56ms
     90%   16.82ms
     99%   75.92ms
  348618 requests in 30.05s, 111.38MB read
Requests/sec:  11600.56
Transfer/sec:      3.71MB
wrk -t4 -c200 -d30s --latency -s wrk/test_mul.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    19.72ms   10.19ms  95.27ms   93.05%
    Req/Sec     2.72k   551.56     8.50k    81.62%
  Latency Distribution
     50%   16.78ms
     75%   16.99ms
     90%   22.38ms
     99%   66.28ms
  325180 requests in 30.13s, 74.74MB read
Requests/sec:  10792.04
Transfer/sec:      2.48MB
wrk -t4 -c200 -d30s --latency -s wrk/test_div.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    22.36ms    9.86ms  90.98ms   93.12%
    Req/Sec     2.35k   459.87     3.50k    78.66%
  Latency Distribution
     50%   19.65ms
     75%   19.89ms
     90%   23.31ms
     99%   68.93ms
  280699 requests in 30.10s, 64.51MB read
Requests/sec:   9326.66
Transfer/sec:      2.14MB
```

### Multi-Worker over 10GbE

This test was running 4 workers registering the same procedure and round-robin balancing.

```console
[oberstet@brummer2 ~/scm/crossbarexamples/rest/caller_performance]$ make test_shared
Testing over 10GbE TCP with single client and sequential requests
wrk -t1 -c1 -d30s --latency -s wrk/test_add.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   551.81us    3.31ms  46.11ms   98.52%
    Req/Sec     5.15k   439.65     5.39k    96.05%
  Latency Distribution
     50%  176.00us
     75%  201.00us
     90%  209.00us
     99%   17.44ms
  155677 requests in 30.41s, 35.78MB read
Requests/sec:   5119.75
Transfer/sec:      1.18MB
Testing over 10GbE TCP with multiple clients and concurrent requests
wrk -t4 -c200 -d30s --latency -s wrk/test_add.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    19.30ms    9.73ms 153.75ms   91.95%
    Req/Sec     2.74k   559.31     5.47k    77.02%
  Latency Distribution
     50%   16.86ms
     75%   17.49ms
     90%   22.73ms
     99%   61.21ms
  328175 requests in 30.15s, 75.43MB read
Requests/sec:  10883.73
Transfer/sec:      2.50MB
```
