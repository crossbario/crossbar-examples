# run this on 10.0.1.2
crossbar:
	crossbar start --personality=community

curl:
	curl -H "Content-Type: application/json" \
		-d '{"procedure": "com.example.add2", "args": [1, 2]}' \
		http://127.0.0.1:8080/call

test:
	python test.py

# run this on 10.0.1.3
load_add_single:
	wrk -t1 -c1 -d30s --latency -s test_add.lua http://10.0.1.2:8080

# run this on 10.0.1.3
load_add_concurrent:
	wrk -t4 -c200 -d30s --latency -s test_add.lua http://10.0.1.2:8080

# run this on 10.0.1.3
load_mul_single:
	wrk -t1 -c1 -d30s --latency -s test_mul.lua http://10.0.1.2:8080

# run this on 10.0.1.3
load_mul_concurrent:
	wrk -t4 -c200 -d30s --latency -s test_mul.lua http://10.0.1.2:8080
