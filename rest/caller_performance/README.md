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
```

### Sequential Requests over 10GbE

```console
```

### Concurrent Requests over 10GbE

```console
```



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

### 10GbE TCP / PyPy 2.6 / FreeBSD

```console
[oberstet@brummer2 ~/scm/crossbarexamples/rest/caller_performance]$ make test_network        
Testing over 10GbE TCP with single client and sequential requests
wrk -t1 -c1 -d30s --latency -s wrk/test_add.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   701.17us    4.15ms  48.95ms   97.88%
    Req/Sec     6.46k   647.13     6.73k    93.02%
  Latency Distribution
     50%  135.00us
     75%  139.00us
     90%  180.00us
     99%   27.19ms
  193544 requests in 30.11s, 44.48MB read
Requests/sec:   6428.92
Transfer/sec:      1.48MB
wrk -t1 -c1 -d30s --latency -s wrk/test_sub.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   717.03us    3.85ms  49.27ms   98.18%
    Req/Sec     4.01k   384.28     4.19k    93.36%
  Latency Distribution
     50%  222.00us
     75%  255.00us
     90%  301.00us
     99%   24.01ms
  120101 requests in 30.11s, 27.72MB read
Requests/sec:   3989.34
Transfer/sec:      0.92MB
wrk -t1 -c1 -d30s --latency -s wrk/test_mul.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   534.75us    3.30ms  50.04ms   98.69%
    Req/Sec     5.05k   401.23     5.28k    94.70%
  Latency Distribution
     50%  179.00us
     75%  201.00us
     90%  213.00us
     99%   14.41ms
  151816 requests in 30.21s, 34.89MB read
Requests/sec:   5025.78
Transfer/sec:      1.16MB
wrk -t1 -c1 -d30s --latency -s wrk/test_div.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   638.38us    3.63ms  48.65ms   98.33%
    Req/Sec     4.59k   419.62     4.78k    95.02%
  Latency Distribution
     50%  196.00us
     75%  225.00us
     90%  237.00us
     99%   21.45ms
  137595 requests in 30.11s, 31.62MB read
Requests/sec:   4570.29
Transfer/sec:      1.05MB
Testing over 10GbE TCP with multiple clients and concurrent requests
wrk -t4 -c200 -d30s --latency -s wrk/test_add.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    18.20ms    8.10ms  99.85ms   93.85%
    Req/Sec     2.89k   499.77     9.96k    87.68%
  Latency Distribution
     50%   16.45ms
     75%   16.69ms
     90%   17.00ms
     99%   63.72ms
  345365 requests in 30.13s, 79.38MB read
Requests/sec:  11464.12
Transfer/sec:      2.63MB
wrk -t4 -c200 -d30s --latency -s wrk/test_sub.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    23.96ms    9.16ms 108.59ms   92.12%
    Req/Sec     2.16k   447.32     6.57k    84.07%
  Latency Distribution
     50%   21.50ms
     75%   21.72ms
     90%   22.53ms
     99%   67.71ms
  257992 requests in 30.10s, 59.54MB read
Requests/sec:   8571.14
Transfer/sec:      1.98MB
wrk -t4 -c200 -d30s --latency -s wrk/test_mul.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    19.50ms    9.41ms 112.25ms   93.00%
    Req/Sec     2.72k   505.29     6.37k    82.46%
  Latency Distribution
     50%   16.79ms
     75%   16.99ms
     90%   24.91ms
     99%   63.45ms
  325594 requests in 30.14s, 74.83MB read
Requests/sec:  10802.76
Transfer/sec:      2.48MB
wrk -t4 -c200 -d30s --latency -s wrk/test_div.lua http://10.0.1.2:8080
Running 30s test @ http://10.0.1.2:8080
  4 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    22.35ms   10.37ms 149.13ms   92.36%
    Req/Sec     2.35k   475.02     5.00k    75.55%
  Latency Distribution
     50%   19.60ms
     75%   19.83ms
     90%   22.44ms
     99%   66.73ms
  280643 requests in 30.10s, 64.50MB read
Requests/sec:   9323.22
Transfer/sec:      2.14MB
```
