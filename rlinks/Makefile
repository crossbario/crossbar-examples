default:
	@echo "Targets:"
	@echo ""
	@echo ""
	@echo ""
	@echo ""
	@echo ""
	@echo ""
	@echo ""
	@echo ""


install:
	sudo apt update && sudo apt install -y haproxy haproxyctl
	pip3 install -r requirements.txt

run_haproxy:
	haproxy -f haproxy.conf

run_ha_node1:
	crossbar start --cbdir ./ha_setup/node1/.crossbar

run_ha_node2:
	crossbar start --cbdir ./ha_setup/node2/.crossbar

run_ha_node3:
	crossbar start --cbdir ./ha_setup/node3/.crossbar

run_ha_node4:
	crossbar start --cbdir ./ha_setup/node4/.crossbar


run_test:
	python main.py \
		--url ws://localhost:8080/ws --realm realm1 \
		--duration 5 --period 1 --clients 1 --connections 1 --loops 1 --rate 1 --stride 1 --size 512




run_smp_node1:
	crossbar --debug-lifecycle start --vmprof --cbdir ./smp_setup/node1/.crossbar


run_benchmark:
	python main.py --config client.ini \
		--duration 300 --period 1 --clients 1 --connections 1 --loops 1 --rate 0.25 --stride 1 --size 512

run_benchmark_single:
	python main.py --config client_single.ini \
		--duration 300 --period 1 --clients 1 --connections 1 --loops 1 --rate 0.25 --stride 1 --size 512

run_benchmark_haproxy:
	python main.py --config client_haproxy.ini \
		--duration 300 --period 1 --clients 1 --connections 40 --loops 1 --rate 0.5 --stride 1 --size 512




run_all:
	crossbar --debug-lifecycle start --vmprof --cbdir ./smp_setup/node1/.crossbar &
	sleep 30
	python main.py
	crossbar stop --cbdir ./smp_setup/node1/.crossbar


clean:
	find . -name ".vmprof-*.dat" -exec rm -f {} \;
	find . -name "autobahn.zip" -exec rm -f {} \;
