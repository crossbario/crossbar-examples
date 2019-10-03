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
	docker-compose up -d blockchain

run_master:
	docker-compose up -d master

run_edge1:
	docker-compose up -d edge1

run_workbench:
	docker-compose up workbench

run_seller1:
	docker-compose up seller1

run_seller2:
	docker-compose up seller2

run_buyer1:
	docker-compose up buyer1

run_buyer2:
	docker-compose up buyer2


init: init_blockchain init_master init_edge1

init_master:
	cp ${HOME}/.crossbarfx/default.pub master/
	$(CROSSBARFX) shell create mrealm mrealm1
	$(CROSSBARFX) shell pair node ./edge1/.crossbar/key.pub mrealm1 node1

init_edge1:
	@echo "nothing to init"

init_blockchain:
	python -u ./_init/init_blockchain_1.py --gateway http://localhost:1545
	python -u ./_init/init_blockchain_2_buyer.py --gateway http://localhost:1545
	python -u ./_init/init_blockchain_2_seller.py --gateway http://localhost:1545


clean: clean_blockchain clean_master clean_edge1

clean_master:
	-docker-compose stop master
	-docker rm teststack_master_1
	-rm -rf ${PWD}/master/.crossbar/.db-controller
	-rm -rf ${PWD}/master/.crossbar/.change-engine
	-rm -rf ${PWD}/master/.crossbar/.db-mrealm-*
	-ls -la ${PWD}/master/.crossbar/

clean_edge1:
	-docker-compose stop edge1
	-docker rm teststack_edge1_1
	-rm -f ${PWD}/edge1/.crossbar/autobahn.zip
	-rm -rf ${PWD}/edge1/.xbrdb-transactions
	-rm -rf ${PWD}/edge1/.testdb
	-ls -la ${PWD}/edge1/.crossbar/

clean_blockchain:
	-docker-compose stop blockchain
	-docker rm teststack_blockchain_1
	-rm -rf ./blockchain/.data
	mkdir -p ./blockchain/.data


stop: stop_edge1 stop_master stop_blockchain

stop_master:
	-docker-compose stop master
	-docker rm teststack_master_1

stop_edge1:
	-docker-compose stop edge1
	-docker rm teststack_edge1_1

stop_blockchain:
	-docker-compose stop blockchain
	-docker rm teststack_blockchain_1
