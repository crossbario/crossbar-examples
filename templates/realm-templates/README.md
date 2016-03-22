# Realm templates

## Dynamic Realm Activation

When the authentication phase of WAMP has determined that a client session is to be attached to realm REALM under role ROLE, Crossbar.io will first lookup realm REALM.

If the realm is running, it'll continue looking for the role - see below.

However, if the realm is not running, that means it wasn't started statically from the node configuration at node start. It can only be started dynamically from matching against a realm template.

A realm template has a `"template"` attribute set to `true`, and a realm `"name"` attribute being a string with a regular expression for a realm.

When the realm matches, the template is instantiated, and a new realm is started according to the realm configuration instantiated. The name of the realm being started is the actual name being requested.

When the realm was successfully started, authentication will continue. The whole process of dynamically starting up a realm only when the first client is connecting is transparent to clients - including the very first client.

The only difference is that is takes a little longer to connect for the first client, as the realm needs to be started dynamically.


## How to try

This example demonstrates a Web client opening 10 WAMP connections to Crossbar.io sequentially, each joining a different realm. The realms are dynamically created by Crossbar.io on the fly.

Open a first terminal and start Crossbar.io

```console
crossbar start
```

Open [http://localhost:8080](http://localhost:8080) in your browser and look at the JavaScript console output (open the console by pressing F12 in your browser).

This should give you log output in the Crossbar.io terminal similar to

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/templates/realm-templates$ make
PYTHONPATH=../../../crossbar/ python -m crossbar.controller.cli start --loglevel=info
2016-03-22T19:22:11+0100 [Controller  27629] Automatically choosing optimal Twisted reactor
2016-03-22T19:22:11+0100 [Controller  27629] Running on Linux and optimal reactor (epoll) was installed.
2016-03-22T19:22:12+0100 [Controller  27629]      __  __  __  __  __  __      __     __
2016-03-22T19:22:12+0100 [Controller  27629]     /  `|__)/  \/__`/__`|__) /\ |__)  |/  \
2016-03-22T19:22:12+0100 [Controller  27629]     \__,|  \\__/.__/.__/|__)/~~\|  \. |\__/
2016-03-22T19:22:12+0100 [Controller  27629]
2016-03-22T19:22:12+0100 [Controller  27629]     Crossbar.io Version: 0.13.0
2016-03-22T19:22:12+0100 [Controller  27629]     Node Public Key: bb4d27e5e9a1f20d24a01ef249373fde77cd402e4a7af45bf08b5dec1c2ba72f
2016-03-22T19:22:12+0100 [Controller  27629]
2016-03-22T19:22:12+0100 [Controller  27629] Running from node directory '/home/oberstet/scm/crossbario/crossbarexamples/templates/realm-templates/.crossbar'
2016-03-22T19:22:12+0100 [Controller  27629] Controller process starting (CPython-EPollReactor) ..
2016-03-22T19:22:12+0100 [Controller  27629] Node configuration loaded from 'config.json'
2016-03-22T19:22:12+0100 [Controller  27629] Node ID 'thinkpad-t430s' set from hostname
2016-03-22T19:22:12+0100 [Controller  27629] Using default node shutdown triggers [u'shutdown_on_worker_exit']
2016-03-22T19:22:12+0100 [Controller  27629] Joined realm 'crossbar' on node management router
2016-03-22T19:22:12+0100 [Controller  27629] Starting Router with ID 'worker-001'...
2016-03-22T19:22:12+0100 [Router      27634] Worker process starting (CPython-EPollReactor) ..
2016-03-22T19:22:12+0100 [Controller  27629] Router with ID 'worker-001' and PID 27634 started
2016-03-22T19:22:12+0100 [Router      27634] Realm 'public' started
2016-03-22T19:22:12+0100 [Controller  27629] Router 'worker-001': realm 'realm-001' (named 'public') started
2016-03-22T19:22:12+0100 [Controller  27629] Router 'worker-001': role 'role-001' (named 'anonymous') started on realm 'realm-001'
2016-03-22T19:22:12+0100 [Router      27634] Site starting on 8080
2016-03-22T19:22:12+0100 [Controller  27629] Router 'worker-001': transport 'transport-001' started
2016-03-22T19:22:15+0100 [Router      27634] Auto starting realm 'realm-user1' ..
2016-03-22T19:22:15+0100 [Controller  27629] Processing activation request for realm 'realm-user1'
2016-03-22T19:22:15+0100 [Controller  27629] Realm 'realm-user1' matched from template '^realm-(?P<user>[a-z][a-z0-9_-]{2,8})$'
2016-03-22T19:22:15+0100 [Router      27634] Realm 'realm-user1' started
2016-03-22T19:22:15+0100 [Controller  27629] Router 'worker-001': realm 'realm-002' (named 'realm-user1') started
2016-03-22T19:22:15+0100 [Controller  27629] Router 'worker-001': role 'role-002' (named 'anonymous') started on realm 'realm-002'
2016-03-22T19:22:15+0100 [Router      27634] Realm 'realm-user1' auto started succeesfully
2016-03-22T19:22:15+0100 [Router      27634] Auto starting realm 'realm-user2' ..
2016-03-22T19:22:15+0100 [Controller  27629] Processing activation request for realm 'realm-user2'
2016-03-22T19:22:15+0100 [Controller  27629] Realm 'realm-user2' matched from template '^realm-(?P<user>[a-z][a-z0-9_-]{2,8})$'
2016-03-22T19:22:15+0100 [Router      27634] Realm 'realm-user2' started
2016-03-22T19:22:15+0100 [Controller  27629] Router 'worker-001': realm 'realm-003' (named 'realm-user2') started
2016-03-22T19:22:15+0100 [Controller  27629] Router 'worker-001': role 'role-003' (named 'anonymous') started on realm 'realm-003'
2016-03-22T19:22:15+0100 [Controller  27629] Processing activation request for realm 'realm-user3'
2016-03-22T19:22:15+0100 [Controller  27629] Realm 'realm-user3' matched from template '^realm-(?P<user>[a-z][a-z0-9_-]{2,8})$'
2016-03-22T19:22:15+0100 [Router      27634] Auto starting realm 'realm-user3' ..
2016-03-22T19:22:15+0100 [Router      27634] Realm 'realm-user2' auto started succeesfully
2016-03-22T19:22:15+0100 [Router      27634] Realm 'realm-user3' started
2016-03-22T19:22:15+0100 [Controller  27629] Router 'worker-001': realm 'realm-004' (named 'realm-user3') started
2016-03-22T19:22:15+0100 [Controller  27629] Router 'worker-001': role 'role-004' (named 'anonymous') started on realm 'realm-004'
2016-03-22T19:22:15+0100 [Router      27634] Realm 'realm-user3' auto started succeesfully
...
```



## Outlook

The idea with the regex stuff also is to allow to define catching, named groups in the regex, which a parsing out pieces from eg the realm being activated, and then the carved out piece can be used in the template, like eg in URIs.

Yeah, there will be race conditions I guess. The basic case seems to work fine .. the first client connecting to a realm matching will make the node controller create the realm (and the roles). And only then the client is connected. It's transparent even for the very first client - it only takes slightly longer.

Now, above PR is about realm templates and auto-activation of realms. What's probably missing is role templates and auto-activation of roles.

What's also missing is a way to automatically start workers, like containers with components, whenever a realm is started dynamically. Since up until now, we could manually define what containers and components to start, as the set of realms started was fixed too. But since the latter isn't any longer the case, we need a way to dynamically start workers, at least containers and guests too.

I am still thinking of how to do the latter best. Currently, I am leaning towards having a new attribute in a container/guest configuration item:

{
    "type": "container",
    "template": "realm",
    "realm": "^com.crossbario.cdc.mrealm-(?P<mrealm>[a-z][a-z0-9_-]{2,8})$"
}

When a matching realm is (dynamically) started, a new container worker is started (with the "realm" parameter replaced by the actual value). The container worker could run a component that connects back to a router under the respective realm. In result, whenever the realm is started, the backend component is started (in a separate container worker) too.

In a way, automatic realm templating and activation together with container/guest worker auto-start can provide a simple way of dynamically activating app services ... at least that was the idea here.
