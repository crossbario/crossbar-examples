# Web and router clusters

## Get up and running

Add the following to a projet `Makefile' for easy access:

```console
CROSSBAR=${PWD}/.test/bin/crossbarfx
CROSSBAR_FABRIC_SUPERUSER=${HOME}/.crossbarfx/default.pub
CROSSBAR_FABRIC_URL=ws://localhost:9000/ws
CROSSBARFX_WATCH_TO_PAIR=${PWD}/.test/nodes

install_crossbar:
	mkdir -p ${PWD}/.test/bin
	curl https://download.crossbario.com/crossbarfx/linux-amd64/crossbarfx-latest -o crossbarfx
	chmod +x crossbarfx
	mv crossbarfx ${PWD}/.test/bin

init_shell:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} shell init --yes

run_master:
	CROSSBAR_FABRIC_SUPERUSER=${CROSSBAR_FABRIC_SUPERUSER} \
	CROSSBARFX_WATCH_TO_PAIR=${CROSSBARFX_WATCH_TO_PAIR} \
	${CROSSBAR} master start --cbdir=${PWD}/.test/master

run_node1:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node1

run_node2:
	CROSSBAR_FABRIC_URL=${CROSSBAR_FABRIC_URL} \
	${CROSSBAR} edge start --cbdir=${PWD}/.test/nodes/node2
```

## General

Show master node status:

```console
crossbarfx shell show status
```

List all management realms defined:

```console
crossbarfx shell list mrealms
```

Show details about management realm "default"

```console
crossbarfx shell show mrealm default
```

> A management realm named "default" is always created by default when
the master node boots the first time - unless a option to deactivate is set.

List all nodes currently paired in the default management realm:

```console
crossbarfx shell --realm default list nodes
```

Show details about all paired nodes

```console
crossbarfx shell --realm default show node all
```

> To show details about a specific node, use `crossbarfx shell --realm default show node <node_name>` or `crossbarfx shell --realm default show node <node_oid>`


## Web clusters

Create a new webcluster named "cluster1" (in the management realm "default"):

```console
crossbarfx shell --realm default create webcluster cluster1 \
    --config='{"tcp_port": 8080, "tcp_shared": true}'
```

Show details about webcluster "cluster1":

```console
crossbarfx shell --realm default show webcluster cluster1
```

List webclusters:

```console
crossbarfx shell --realm default list webclusters
```

Start the webcluster "cluster1":

```console
crossbarfx shell --realm default start webcluster cluster1
```

Stop the webcluster "cluster1":

```console
crossbarfx shell --realm default stop webcluster cluster1
```

### Web cluster nodes

Add all nodes (currently paired in the default management realm) to
the webcluster "cluster1", with a per-node parallel degree of two:

```console
crossbarfx shell --realm default add webcluster-node cluster1 all \
    --config '{"parallel": 2}'
```

List nodes currently added to webcluster "cluster1":

```console
crossbarfx shell --realm default list webcluster-nodes cluster1
```

Show details about a node added to a cluster:

```console
crossbarfx shell --realm default show webcluster-node cluster1 node-e907435a
```

### Web cluster services

Add a webservice serving static Web files to the webcluster "cluster1":

```console
crossbarfx shell --realm default add webcluster-service cluster1 "/" \
    --config '{"type": "static", "directory": "..", "options": {"enable_directory_listing": true}}'
```

Add a webservice rendering a node info Web page to the webcluster "cluster1":

```console
crossbarfx shell --realm default add webcluster-service cluster1 "info" \
    --config '{"type": "nodeinfo"}'
```

Add a webservice serving a arbitrary literal JSON value via HTTP to the webcluster "cluster1":

```console
crossbarfx shell --realm default add webcluster-service cluster1 "settings" \
    --config '{"type": "json", "value": [1, 2, 3]}'
```

Add a webservice providing a WAMP-WebSocket endpoint to the webcluster "cluster1":

```console
crossbarfx shell --realm default add webcluster-service cluster1 "ws" \
    --config '{"type": "websocket"}'
```

List webservices currently added to webcluster "cluster1":

```console
crossbarfx shell --realm default list webcluster-services cluster1
```

Show details about a webservice added to a cluster:

```console
crossbarfx shell --realm default show webcluster-service cluster1 "settings"
```

## Router clusters

Create a new router cluster named "cluster2" (in the management realm "default"):


```console
crossbarfx shell --realm default create routercluster cluster2
```

Show details about router cluster "cluster2":

```console
crossbarfx shell --realm default show routercluster cluster2
```

List router clusters:

```console
crossbarfx shell --realm default list routerclusters
```

Start the router cluster "cluster2":

```console
crossbarfx shell --realm default start routercluster cluster2
```

Stop the webcluster "cluster2":

```console
crossbarfx shell --realm default stop routercluster cluster2
```

### Router cluster nodes

Add all nodes (currently paired in the default management realm) to
the router cluster "cluster2", with given soft-/hardlimits per node:

```console
crossbarfx shell --realm default add routercluster-node cluster2 all \
    --config '{"softlimit": 4, "hardlimit": 8}'
```

List nodes currently added to webcluster "cluster2" (*NOT YET IMPLEMENTED*):

```console
crossbarfx shell --realm default list routercluster-nodes cluster2
```

Show details about a node added to a cluster (*NOT YET IMPLEMENTED*):

```console
crossbarfx shell --realm default show routercluster-node cluster2 node-e907435a
```

### Router cluster worker groups

Add a router worker group (able to host application realms) to the router cluster "cluster2":

```console
crossbarfx shell --realm default add routercluster-workergroup cluster2 mygroup1 \
    --config '{}'
```

Show details about a router worker group added to a router cluster:

```console
crossbarfx shell --realm default show routercluster-workergroup cluster2 mygroup1
```

List webservices currently added to router cluster "cluster2" (*NOT YET IMPLEMENTED*):

```console
crossbarfx shell --realm default list routercluster-workergroups cluster2
```

### Router roles

Create a new role for use with application routers:

```console
crossbarfx shell --realm default create role myrole1 \
    --config='{}'
```

List all roles defined in the management realm "default" (*NOT YET IMPLEMENTED*):

```console
crossbarfx shell --realm default list roles
```

Show details about a role defined:

```console
crossbarfx shell --realm default show role myrole1
```

#### Role permissions

Add a WAMP-level routing permission to a previously defined role:

```console
crossbarfx shell --realm default add role-permission myrole1 "com.example." \
    --config='{"match": "prefix", "allow_call": true, "allow_register": true, "allow_publish": true, "allow_subscribe": true, "disclose_caller": true, "disclose_publisher": true, "cache": true}'
```

List all permissions added to a role (*NOT YET IMPLEMENTED*):

```console
crossbarfx shell --realm default list role-permissions myrole1
```

Show details about a permission (*NOT YET IMPLEMENTED*):

```console
crossbarfx shell --realm default show role-permission myrole1 "com.example."
```

### Application realms

Create a new application realm for WAMP routing:

```console
crossbarfx shell --realm default create arealm myrealm1 --config='{"enable_meta_api": true, "bridge_meta_api": true}'
```

Show details about an application realm:

```console
crossbarfx shell --realm default show arealm myrealm1
```

List all application realms defined (*NOT YET IMPLEMENTED*):

```console
crossbarfx shell --realm default list arealms
```

Start an application realm on the given router cluster, router worker group and web cluster:

```console
crossbarfx shell --realm default start arealm myrealm1 cluster2 mygroup1 cluster1
```

Stop an application realm:

```console
crossbarfx shell --realm default stop arealm myrealm1
```

#### Application Realms and Roles

Attach the given role to the application realm:

```console
crossbarfx shell --realm default add arealm-role myrealm1 myrole1 --config='{"authmethod": "anonymous"}'
```

Show details about a role attached to an application realm:

```console
crossbarfx shell --realm default show arealm-role myrealm1 myrole1
```
