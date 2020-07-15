# web clusters

```console
crossbarfx shell --realm default list webclusters
crossbarfx shell --realm default create webcluster cluster1
crossbarfx shell --realm default create webcluster cluster1 --config='{"tcp_port": 8080}'
crossbarfx shell --realm default show webcluster cluster1

crossbarfx shell --realm default show node
crossbarfx shell --realm default show node node-949b8510
crossbarfx shell --realm default show node node-070acca4
crossbarfx shell --realm default list webcluster-nodes cluster1

crossbarfx shell --realm default add webcluster-node cluster1 node-949b8510 --config '{"webcluster_oid": "494e78fa-084c-4230-8128-9e88d51f63ed"}'
crossbarfx shell --realm default add webcluster-node cluster1 node-070acca4 --config '{"webcluster_oid": "494e78fa-084c-4230-8128-9e88d51f63ed", "parallel": 4}'

crossbarfx shell --realm default list webcluster-nodes cluster1
crossbarfx shell --realm default show webcluster-node cluster1 node-070acca4

crossbarfx shell --realm default list webcluster-services cluster1
crossbarfx shell --realm default add webcluster-service cluster1 "/" --config '{"type": "json", "value": [1, 2, 3]}'
crossbarfx shell --realm default show webcluster-service cluster1 "/"

crossbarfx shell --realm default start webcluster cluster1
```


crossbarfx shell --realm default create webcluster cluster1
crossbarfx shell --realm default add webcluster-node cluster1 node-74a814e7 --config '{"webcluster_oid": "b4077496-ad81-45e2-ad23-8e08d6910e2c"}'
crossbarfx shell --realm default add webcluster-node cluster1 node-ccad35c5 --config '{"webcluster_oid": "b4077496-ad81-45e2-ad23-8e08d6910e2c", "parallel": 4}'
crossbarfx shell --realm default add webcluster-service cluster1 "/" --config '{"type": "json", "value": [1, 2, 3]}'

crossbarfx shell --realm default start webcluster cluster1


crossbarfx shell --realm default show node
crossbarfx shell --realm default create webcluster cluster1 --config='{"tcp_port": 8080, "tcp_shared": true}'

crossbarfx shell --realm default add webcluster-node cluster1 node-2df6044d --config '{"webcluster_oid": "2fd28a96-91d2-47bc-a0de-0d45acc12e75", "parallel": 4}'
crossbarfx shell --realm default add webcluster-service cluster1 "/" --config '{"type": "static", "directory": "..", "options": {"enable_directory_listing": true}}'
crossbarfx shell --realm default add webcluster-service cluster1 "info" --config '{"type": "nodeinfo"}'
crossbarfx shell --realm default add webcluster-service cluster1 "settings" --config '{"type": "json", "value": [1, 2, 3]}'
crossbarfx shell --realm default start webcluster cluster1
