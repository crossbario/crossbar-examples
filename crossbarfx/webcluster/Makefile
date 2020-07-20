#CROSSBAR=${PWD}/.test/bin/crossbarfx
CROSSBAR=crossbarfx

CROSSBAR_FABRIC_SUPERUSER=${HOME}/.crossbarfx/default.pub
CROSSBAR_FABRIC_URL=ws://localhost:9000/ws
CROSSBARFX_WATCH_TO_PAIR=${PWD}/.test/nodes

# see screenshots docs/shot1.png
install_crossbar:
	mkdir -p ${PWD}/.test/bin
	curl https://download.crossbario.com/crossbarfx/linux-amd64/crossbarfx-latest -o crossbarfx
	chmod +x crossbarfx
	mv crossbarfx ${PWD}/.test/bin

init_shell:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} shell init --yes

# see screenshots docs/shot2.png
run_master:
	CROSSBAR_FABRIC_SUPERUSER=${CROSSBAR_FABRIC_SUPERUSER} \
	CROSSBARFX_WATCH_TO_PAIR=${CROSSBARFX_WATCH_TO_PAIR} \
	${CROSSBAR} master start --cbdir=${PWD}/.test/master

# see screenshots docs/shot3.png and docs/shot4.png
run_node1:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node1

# see screenshots docs/shot5.png
run_node2:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node2

# see screenshots docs/shot6.png
status_master:
	${CROSSBAR} shell show status
	${CROSSBAR} shell list mrealms
	${CROSSBAR} shell show mrealm default
	${CROSSBAR} shell --realm default list nodes
	${CROSSBAR} shell --realm default show node

configure_clusters: configure_cluster1 configure_cluster2

start_clusters: start_cluster1 start_cluster2 start_cluster2_arealm

show_clusters: show_cluster1 show_cluster2


configure_cluster1:
	crossbarfx shell --realm default create webcluster cluster1 --config='{"tcp_port": 8080, "tcp_shared": true}'
	crossbarfx shell --realm default add webcluster-node cluster1 all --config '{"parallel": 2}'
	crossbarfx shell --realm default add webcluster-service cluster1 "/" --config '{"type": "static", "directory": "..", "options": {"enable_directory_listing": true}}'
	crossbarfx shell --realm default add webcluster-service cluster1 "info" --config '{"type": "nodeinfo"}'
	crossbarfx shell --realm default add webcluster-service cluster1 "settings" --config '{"type": "json", "value": [1, 2, 3]}'

# docs/shot7.png, docs/shot8.png
start_cluster1:
	crossbarfx shell --realm default start webcluster cluster1

stop_cluster1:
	crossbarfx shell --realm default stop webcluster cluster1

show_cluster1:
	crossbarfx shell --realm default show webcluster cluster1

configure_cluster1_add1:
	crossbarfx shell --realm default add webcluster-service cluster1 "other" --config '{"type": "json", "value": {"contents": "settings2"}}'


configure_cluster2: configure_cluster2_cluster configure_cluster2_role configure_cluster2_arealm

configure_cluster2_cluster:
	crossbarfx shell --realm default create routercluster cluster2
	crossbarfx shell --realm default add routercluster-node cluster2 all --config '{"softlimit": 4, "hardlimit": 8}'
	crossbarfx shell --realm default add routercluster-workergroup cluster2 mygroup1 --config '{}'

configure_cluster2_role:
	crossbarfx shell --realm default create role myrole1 --config='{}'
	crossbarfx shell --realm default add role-permission myrole1 "com.example." --config='{"match": "prefix", "allow_call": true, "allow_register": true, "allow_publish": true, "allow_subscribe": true, "disclose_caller": true, "disclose_publisher": true, "cache": true}'

configure_cluster2_arealm:
	crossbarfx shell --realm default create arealm myrealm1 --config='{"enable_meta_api": true, "bridge_meta_api": true}'
	crossbarfx shell --realm default add arealm-role myrealm1 myrole1 --config='{"authmethod": "anonymous"}'


start_cluster2:
	crossbarfx shell --realm default start routercluster cluster2

stop_cluster2:
	crossbarfx shell --realm default stop routercluster cluster2


start_cluster2_arealm:
	crossbarfx shell --realm default start arealm myrealm1 cluster2 mygroup1 cluster1

stop_cluster2_arealm:
	crossbarfx shell --realm default stop arealm myrealm1


show_cluster2: show_cluster2_role show_cluster2_arealm
	crossbarfx shell --realm default show routercluster cluster2

show_cluster2_role:
	crossbarfx shell --realm default show role myrole1

show_cluster2_arealm:
	crossbarfx shell --realm default show arealm myrealm1
	crossbarfx shell --realm default show arealm-role myrealm1 myrole1

############################################################################################################

status_nodes:
	${CROSSBAR} shell --realm default show node
	find ${PWD}/.test/nodes -name key.pub -print -exec sh -c "grep 'public-key' {} && crossbarfx edge status --cbdir={}" \;

find_nodes:
	find ${PWD}/.test/nodes -name key.activate -print -exec cat {} \;

run_node1_unmanaged:
	CROSSBAR_FABRIC_URL="" \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node1

run_node3:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node3

run_node4:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node4

run_node5:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node5

# WARNING: this will destroy your current CLI config & user profiles folder immediately
# and create a fresh one from scratch!
clean_shell:
	rm -rf ${HOME}/.crossbarfx

clean_master:
	rm -rf ${PWD}/.test/master
	mkdir -p ${PWD}/.test/master

clean_nodes:
	rm -rf ${PWD}/.test/nodes
	mkdir -p ${PWD}/.test/nodes

clean_bin:
	rm -rf ${PWD}/.test/bin
	mkdir -p ${PWD}/.test/bin

clean_profile:
	rm -rf ${HOME}/.crossbarfx

clean: clean_master clean_nodes

clean_all: clean clean_bin clean_profile
