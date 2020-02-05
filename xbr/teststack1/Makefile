CROSSBARFX=crossbarfx
#CROSSBARFX=./crossbarfx-linux-amd64-20181205-8fb98e0

status:
	-docker-compose images
	-docker-compose ps

logs_blockchain:
	docker logs -f teststack1_blockchain_1

logs_master:
	docker logs -f teststack1_master_1

logs_edge1:
	docker logs -f teststack1_edge1_1


run:
	docker-compose up -d blockchain master edge1

run_blockchain:
	docker-compose up blockchain

run_master:
	cp ${HOME}/.crossbarfx/default.pub master/
	docker-compose up master

run_edge1:
	docker-compose up edge1

run_edge1_host:
	CROSSBARFX_DISABLE_CE=1 \
	CE_DISABLE=1 \
	crossbarfx edge start --cbdir ./edge1/.crossbar --config=config.json --loglevel=info

run_workbench:
	docker-compose up workbench

run_seller1:
	docker-compose up seller1

run_seller1_host:
	XBR_INSTANCE=ws://localhost:8080/ws XBR_REALM=realm1 python ./python/seller.py

run_seller2:
	docker-compose up seller2

run_seller2_host:
	XBR_INSTANCE=ws://localhost:8080/ws XBR_REALM=realm1 node ./javascript/seller.js

run_buyer1:
	docker-compose up buyer1

run_buyer1_host:
	XBR_INSTANCE=ws://localhost:8080/ws XBR_REALM=realm1 python ./python/buyer.py

run_buyer2:
	docker-compose up buyer2

run_buyer2_host:
	XBR_INSTANCE=ws://localhost:8080/ws XBR_REALM=realm1 node ./javascript/buyer.js


status_master:
	$(CROSSBARFX) shell auth
	$(CROSSBARFX) shell show status
	$(CROSSBARFX) shell list mrealms


init: init_blockchain init_master init_edge1

init_master:
	$(CROSSBARFX) shell auth
	$(CROSSBARFX) shell create mrealm mrealm1
	$(CROSSBARFX) shell pair node ./edge1/.crossbar/key.pub mrealm1 node1

init_edge1:
	@echo "nothing to init"

init_blockchain:
	python -u ./_init/init_blockchain_1.py --gateway http://localhost:1545
	python -u ./_init/init_blockchain_2_buyer.py --gateway http://localhost:1545
	python -u ./_init/init_blockchain_2_seller.py --gateway http://localhost:1545


clean: clean_blockchain clean_master clean_edge1
	-docker rm teststack1_buyer1_1
	-docker rm teststack1_buyer2_1
	-docker rm teststack1_seller1_1
	-docker rm teststack1_seller2_1
	-docker rm teststack1_workbench_1

clean_master:
	-docker-compose stop master
	-docker rm teststack1_master_1
	-sudo rm -rf ${PWD}/master/.crossbar/.db-controller
	-sudo rm -rf ${PWD}/master/.crossbar/.change-engine
	-sudo rm -rf ${PWD}/master/.crossbar/.db-mrealm-*
	-ls -la ${PWD}/master/.crossbar/
	-ls -la ${PWD}/master/

clean_edge1:
	-docker-compose stop edge1
	-docker rm teststack1_edge1_1
	-sudo rm -f ${PWD}/edge1/.crossbar/autobahn.zip
	-sudo rm -rf ${PWD}/edge1/.xbrdb-transactions
	-sudo rm -rf ${PWD}/edge1/.testdb
	-ls -la ${PWD}/edge1/.crossbar/

clean_blockchain:
	-docker-compose stop blockchain
	-docker rm teststack1_blockchain_1
	-docker rm teststack1_blockchain_old_1
	-rm -rf ./blockchain/.data
	mkdir -p ./blockchain/.data

stop:
	-docker-compose stop
	-docker-compose ps

stop_master:
	-docker-compose stop master
	-docker rm teststack1_master_1

stop_edge1:
	-docker-compose stop edge1
	-docker rm teststack1_edge1_1

stop_blockchain:
	-docker-compose stop blockchain
	-docker rm teststack1_blockchain_1
