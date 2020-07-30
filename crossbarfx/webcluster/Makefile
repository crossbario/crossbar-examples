#CROSSBAR=${PWD}/.test/bin/crossbarfx
CROSSBAR=crossbarfx

CROSSBAR_FABRIC_SUPERUSER=${HOME}/.crossbarfx/default.pub
CROSSBAR_FABRIC_URL=ws://localhost:9000/ws
CROSSBARFX_WATCH_TO_PAIR=${PWD}/.test/nodes

install_crossbar:
	mkdir -p ${PWD}/.test/bin
	curl https://download.crossbario.com/crossbarfx/linux-amd64/crossbarfx-latest -o crossbarfx
	chmod +x crossbarfx
	mv crossbarfx ${PWD}/.test/bin

version_crossbar:
	${CROSSBAR} version

clean_bin:
	rm -rf ${PWD}/.test/bin
	mkdir -p ${PWD}/.test/bin

clean: clean_master clean_nodes

clean_all: clean clean_bin clean_profile


init_shell:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} shell init --yes

# WARNING: this will destroy your current CLI config & user profiles folder immediately
# and create a fresh one from scratch!
clean_shell:
	rm -rf ${HOME}/.crossbarfx


monitor_master:
	${CROSSBAR} shell monitor

run_master:
	CROSSBAR_FABRIC_SUPERUSER=${CROSSBAR_FABRIC_SUPERUSER} \
	CROSSBARFX_WATCH_TO_PAIR=${CROSSBARFX_WATCH_TO_PAIR} \
	${CROSSBAR} master start --cbdir=${PWD}/.test/master

run_master_nowatch:
	CROSSBAR_FABRIC_SUPERUSER=${CROSSBAR_FABRIC_SUPERUSER} \
	${CROSSBAR} master start --cbdir=${PWD}/.test/master

clean_master:
	rm -rf ${PWD}/.test/master
	mkdir -p ${PWD}/.test/master

status_master:
	${CROSSBAR} shell show status
	${CROSSBAR} shell list mrealms
	${CROSSBAR} shell show mrealm default
	${CROSSBAR} shell --realm default list nodes
	${CROSSBAR} shell --realm default show node


init_nodes:
	${CROSSBAR} edge keys --cbdir=${PWD}/.test/nodes/node1
	${CROSSBAR} edge keys --cbdir=${PWD}/.test/nodes/node2
	${CROSSBAR} edge keys --cbdir=${PWD}/.test/nodes/node3
	find ${PWD}/.test/nodes

pair_nodes:
	${CROSSBAR} shell pair node .test/nodes/node1/key.pub default node1
	${CROSSBAR} shell pair node .test/nodes/node2/key.pub default node2
	${CROSSBAR} shell pair node .test/nodes/node3/key.pub default node3
	${CROSSBAR} shell --realm default list nodes
	${CROSSBAR} shell --realm default show node

clean_nodes:
	rm -rf ${PWD}/.test/nodes
	mkdir -p ${PWD}/.test/nodes

# see screenshots docs/shot3.png and docs/shot4.png
run_node1:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node1

# see screenshots docs/shot5.png
run_node2:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node2

run_node3:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node3

status_nodes:
	${CROSSBAR} shell --realm default show node
	netstat -ltne | awk '{ print $4 }' | sort
	find ${PWD}/.test/nodes -name key.pub -print -exec sh -c "grep 'public-key' {} && ${CROSSBAR} edge status --cbdir={}" \;

find_nodes:
	find ${PWD}/.test/nodes -name key.activate -print -exec cat {} \;

run_node1_unmanaged:
	CROSSBAR_FABRIC_URL="" \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node1


############################################################################################################


configure_clusters: configure_cluster1 configure_cluster2

start_clusters: start_cluster1 start_cluster2 start_cluster2_arealm

show_clusters: show_cluster1 show_cluster2

configure_cluster1:
	${CROSSBAR} shell --realm default create webcluster cluster1 --config='{"tcp_port": 8080, "tcp_shared": true}'
	${CROSSBAR} shell --realm default add webcluster-node cluster1 all --config '{"parallel": 2}'
	${CROSSBAR} shell --realm default add webcluster-service cluster1 "/" --config '{"type": "static", "directory": "..", "options": {"enable_directory_listing": true}}'
	${CROSSBAR} shell --realm default add webcluster-service cluster1 "info" --config '{"type": "nodeinfo"}'
	${CROSSBAR} shell --realm default add webcluster-service cluster1 "settings" --config '{"type": "json", "value": [1, 2, 3]}'
	${CROSSBAR} shell --realm default add webcluster-service cluster1 "ws" --config '{"type": "websocket"}'

start_cluster1:
	${CROSSBAR} shell --realm default start webcluster cluster1

stop_cluster1:
	${CROSSBAR} shell --realm default stop webcluster cluster1

show_cluster1:
	${CROSSBAR} shell --realm default show webcluster cluster1

configure_cluster1_add1:
	${CROSSBAR} shell --realm default add webcluster-service cluster1 "other" --config '{"type": "json", "value": {"contents": "settings2"}}'


configure_cluster2: configure_cluster2_cluster configure_cluster2_role configure_cluster2_arealm

configure_cluster2_cluster:
	${CROSSBAR} shell --realm default create routercluster cluster2
	${CROSSBAR} shell --realm default add routercluster-node cluster2 all --config '{"softlimit": 4, "hardlimit": 8}'
	#${CROSSBAR} shell --realm default add routercluster-workergroup cluster2 mygroup1 --config '{}'
	${CROSSBAR} shell --realm default add routercluster-workergroup cluster2 mygroup1 --config '{"scale": 1}'
	#${CROSSBAR} shell --realm default add routercluster-workergroup cluster2 mygroup1 --config '{"scale": 3}'
	${CROSSBAR} shell --realm default add routercluster-workergroup cluster2 mygroup2 --config '{}'
	${CROSSBAR} shell --realm default add routercluster-workergroup cluster2 mygroup3 --config '{}'

configure_cluster2_role:
	${CROSSBAR} shell --realm default create role myrole1 --config='{}'
	${CROSSBAR} shell --realm default add role-permission myrole1 "com.example." --config='{"match": "prefix", "allow_call": true, "allow_register": true, "allow_publish": true, "allow_subscribe": true, "disclose_caller": true, "disclose_publisher": true, "cache": true}'
	${CROSSBAR} shell --realm default create role myrole2 --config='{}'
	${CROSSBAR} shell --realm default add role-permission myrole2 "foobar." --config='{"match": "prefix", "allow_call": true, "allow_register": true, "allow_publish": true, "allow_subscribe": true, "disclose_caller": true, "disclose_publisher": true, "cache": true}'

configure_cluster2_arealm:
	${CROSSBAR} shell --realm default create arealm myrealm1 --config='{"enable_meta_api": true, "bridge_meta_api": true}'
	${CROSSBAR} shell --realm default add arealm-role myrealm1 myrole1 --config='{"authmethod": "anonymous"}'
	${CROSSBAR} shell --realm default create arealm myrealm2 --config='{"enable_meta_api": true, "bridge_meta_api": true}'
	${CROSSBAR} shell --realm default add arealm-role myrealm2 myrole1 --config='{"authmethod": "anonymous"}'
	${CROSSBAR} shell --realm default create arealm myrealm3 --config='{"enable_meta_api": true, "bridge_meta_api": true}'
	${CROSSBAR} shell --realm default add arealm-role myrealm3 myrole2 --config='{"authmethod": "anonymous"}'
	${CROSSBAR} shell --realm default create arealm myrealm4 --config='{"enable_meta_api": true, "bridge_meta_api": true}'
	${CROSSBAR} shell --realm default add arealm-role myrealm4 myrole1 --config='{"authmethod": "anonymous"}'

start_cluster2:
	${CROSSBAR} shell --realm default start routercluster cluster2

stop_cluster2:
	${CROSSBAR} shell --realm default stop routercluster cluster2

start_cluster2_arealm:
	${CROSSBAR} shell --realm default start arealm myrealm1 cluster2 mygroup1 cluster1
	${CROSSBAR} shell --realm default start arealm myrealm2 cluster2 mygroup2 cluster1
	${CROSSBAR} shell --realm default start arealm myrealm3 cluster2 mygroup3 cluster1
	${CROSSBAR} shell --realm default start arealm myrealm4 cluster2 mygroup3 cluster1

stop_cluster2_arealm:
	${CROSSBAR} shell --realm default stop arealm myrealm1
	${CROSSBAR} shell --realm default stop arealm myrealm2
	${CROSSBAR} shell --realm default stop arealm myrealm3
	${CROSSBAR} shell --realm default stop arealm myrealm4

show_cluster2: show_cluster2_role show_cluster2_arealm
	${CROSSBAR} shell --realm default show routercluster cluster2

show_cluster2_role:
	${CROSSBAR} shell --realm default show role myrole1
	${CROSSBAR} shell --realm default show role myrole2

show_cluster2_arealm:
	${CROSSBAR} shell --realm default show arealm myrealm1
	${CROSSBAR} shell --realm default show arealm-role myrealm1 myrole1
	${CROSSBAR} shell --realm default show arealm myrealm2
	${CROSSBAR} shell --realm default show arealm-role myrealm2 myrole1
	${CROSSBAR} shell --realm default show arealm myrealm3
	${CROSSBAR} shell --realm default show arealm-role myrealm3 myrole2
	${CROSSBAR} shell --realm default show arealm myrealm4
	${CROSSBAR} shell --realm default show arealm-role myrealm4 myrole1


run_subscribe_ws_cbor:
	python client-subscribe.py websocket-cbor

run_subscribe_rs_cbor:
	python client-subscribe.py rawsocket-cbor

run_subscribe_ws_json:
	python client-subscribe.py websocket-json

run_subscribe_rs_json:
	python client-subscribe.py rawsocket-json


run_publish_ws_cbor:
	python client-publish.py websocket-cbor

run_publish_rs_cbor:
	python client-publish.py rawsocket-cbor

run_publish_ws_json:
	python client-publish.py websocket-json

run_publish_rs_json:
	python client-publish.py rawsocket-json

