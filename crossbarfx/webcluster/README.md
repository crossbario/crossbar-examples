# Web and router clusters

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
```

Show details about a node added to a cluster:

```console
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
```

Show details about a webservice added to a cluster:

```console
```
