# Crossbar.io DevOps Center API

The public API is used by clients of the Crossbar DevOps Center (CDC). Calls to the CDC may result in private API calls.

Since this API may be used by clients other than our own, it should be stable.

All calls are within the management realm to which the session issuing the calls is connected.

## Full list

* `crossbario.cdc.api.get_now`
* `crossbario.cdc.api.get_nodes`
* `crossbario.cdc.api.get_node_info`
* `crossbario.cdc.api.get_controller_info`
* `crossbario.cdc.api.get_controller_stats`
* `crossbario.cdc.api.shutdown_node`
* `crossbario.cdc.api.get_nodes`
* `crossbario.cdc.api.get_node_workers`
* `crossbario.cdc.api.get_worker_log`
* `crossbario.cdc.api.start_router_worker`
* `crossbario.cdc.api.start_container_worker`
* `crossbario.cdc.api.start_guest_worker`
* `crossbario.cdc.api.shutdown_worker`
* `crossbario.cdc.api.get_worker_cpu_count`
* `crossbario.cdc.api.get_worker_cpu_affinity`
* `crossbario.cdc.api.set_worker_cpu_affinity`
* `crossbario.cdc.api.get_worker_pythonpath`
* `crossbario.cdc.api.add_worker_pythonpath`
* `crossbario.cdc.api.get_worker_profilers`
* `crossbario.cdc.api.start_worker_profiler`
* `crossbario.cdc.api.get_worker_profile`
* `crossbario.cdc.api.get_router_realms`
* `crossbario.cdc.api.start_router_realm`
* `crossbario.cdc.api.stop_router_realm`
* `crossbario.cdc.api.get_realm_roles`
* `crossbario.cdc.api.start_realm_role`
* `crossbario.cdc.api.stop_realm_role`
* `crossbario.cdc.api.get_router_components`
* `crossbario.cdc.api.start_router_component`
* `crossbario.cdc.api.get_router_transports`
* `crossbario.cdc.api.start_router_transport`
* `crossbario.cdc.api.stop_router_transport`


## CDC-related

### Get Time

* **Procedure** `crossbario.cdc.api.get_now`

Get the current time (as UTC) of the CDC. (Implemented mostly to check whether contact to the CDC is working.)

## Node-related

### List Nodes

* **Procedure** `crossbario.cdc.api.get_nodes`

List all Crossbar.io nodes on the management realm connected to.


### List Workers

* **Procedure** `io.crossbar.cdc.list_workers`

List all workers created for the given node.

Arguments:

   * `node_id` - *string* - the ID of the node to list the workers for (*required*)


### Create Node

* **Procedure** `io.crossbar.cdc.create_node`

Create a new node.

Arguments:

   * `node_id` - *string* - an ID for the node to be created (*required*)
   * `node_config` - *dictionary* - the node configuration (*required*)


### List Node Workers

* **Procedure** `io.crossbar.cdc.list_node_workers`

List all workers created on the given node.

Arguments:

   * `node_id`- *string* - the id of the node for which to list workers (*required*)

## Router-related

* `get_router`
* `create_router`
* `modify_router`
* `delete_router`
* `start_router`
* `stop_router`
* `reload_router`


### Get Router

* **Procedure** `io.crossbar.cdc.get_router`

Get configuration and status of existing router.

Arguments:

   * `node_id` - *string* - the id of the node which hosts the router (*required*)
   * `router_id` - *string* - the id of the router (*required*)


### Create Router

* **Procedure** `io.crossbar.cdc.create_router`

Create a router on a node.

> Note: This directly only creates a database entry with the set configuration. To actually start the router, the start router procedure needs to be called.

Arguments:

   * `node_id` - *string* - the id of the node on which the router is to be created (*required*)
   * `router_id` - *string* - an ID for the router to be created (*required*)
   * `router_config` - *dictionary* - the configuration for the router (*required*)


### Modify Router

* **Procedure** `io.crossbar.cdc.modify_router`

Modify a router worker configuration on a given node.

> Note: This directly only changes the database entry. To actually apply changes to a running router worker, the worker needs to be reloaded or restarted.

Arguments:

   * `node_id` - *string* - the id of the node on which the router is hosted (*required*)
   * `router_id` - *string* - the id of the router to be modified (*required*)
   * `router_config` - *dictionary* - the configuration change set for the router (*required*)


### Delete Router

* **Procedure** `io.crossbar.cdc.delete_router`

Delete a router worker configuration on a given node. A router worker configuration can only be deleted when the respective router worker is currently stopped!

Arguments:

   * `node_id` - *string* - the id of the node on which the router is hosted (*required*)
   * `router_id` - *string* - the id of the router to be deleted (*required*)


### Start Router

* **Procedure** `io.crossbar.cdc.start_router`

Start a previously created router. The router worker will be started with the currently active configuration.

Arguments:

   * `node_id` - *string* - the id of the node on which the router is hosted (*required*)
   * `router_id` - *string* - the id of the router to be started (*required*)


### Stop Router

* **Procedure** `io.crossbar.cdc.stop_router`

Stop a running router worker.

Arguments:

   * `node_id` - *string* - the id of the node on which the router is hosted (*required*)
   * `router_id` - *string* - the id of the router to be stopped (*required*)


### Reload Router

* **Procedure** `io.crossbar.cdc.reload_router`

Reload the configuration of a currently running router worker. When a router configuration has changed, the changes will only be applied once this procedure is called (or the router is restarted).

Arguments:

   * `node_id` - *string* - the id of the node on which the router is hosted (*required*)
   * `router_id` - *string* - the id of the router to be reloaded (*required*)
   * `restart_if_required' - *boolean* - Restart the router if one or more configuration changes cannot be applied without a restart. An exception is raised if this is `false` and a restart would be required in order to apply all changes. (*optional*)


## Worker-related

* `profile_worker`
* `get_stats`

### Profile Worker

Get a profile of the processor usage within a worker.

Arguments:

   * `node_id` - *string* - the id of the node on which the worker is hosted (*required*)
   * `worker_id` - *string* - the id of the worker on which to run the profile (*required*)
   * `profiler` - *string* - the profiler to start (currently only 'vmprof' is supported - (*optional* - default: `vmprof`)
   * `runtime` - *integer* - the duration in seconds for which to enable profiling and generate a profile (*optional* - default: 10)
   * `profiler` - *integer* - prune % (*optional* - default: 5)
   * `profiler` - *integer* - prune level (*optional* - default: 1000)

### Get Stats

Get the generic worker statistics (e.g. cpu affinity, uptime) for a specific worker.

Arguments:

   * `node_id` - *string* - the id of the node on which the worker is hosted (*required*)
   * `worker_id` - *string* - the id of the worker for which to receive the stats (*required*)
