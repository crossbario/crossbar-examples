Accelerating Ext.Direct - Unlimited Concurrency
===============================================

*Tavendo WebMQ* is able to forward standard WAMP RPCs to any server exposing an Ext.Direct compatible API.

This requires no change to the backend server.

Compared to i.e. direct Ajax calls, this has a number of advantages:

 1. Unlimited concurrency
 2. Calls to *different* servers (without cross-domains hacks, security issues)
 3. Reduced overhead: only consumes 1 TCP connection
 4. Reduced wire traffic: good for i.e. mobile environments
 5. Access from any WAMP client

Unlimited concurrency means that RPCs are executed not only asynchronously, but concurrently. RPCs that take a long time on the backend (for example, because running a database query) will not block subsequently issued RPCs. Results for RPCs will be delivered as soon as available.

Since *Tavendo WebMQ* uses *WebSocket*, it is possible to establish multiple connections to different servers on different domains from within the same HTML/JS. Ext.Direct Standard is only able to do this using JSONP, which has security implications when used cross-domain (and generally is a hack).

Further, with *Tavendo WebMQ*, only a single TCP connection is consumed per session. This reduces the load on browser, the network and the backend servers.

Since WebSocket has very low overhead compared to HTTP requests (which can result in between 400 bytes to 2k per call), the wire traffic is greatly reduced, which is especially desirable on mobile connections and data plans.

Since *Tavendo WebMQ* is based on WAMP, Ext.Direct servers can be accessed via RPC from any WAMP compatible client, which includes *AutobahnAndroid*. The latter allows to write native Android apps that issues RPCs onto Ext.Direct servers.


Ext.Direct Standard RPCs
------------------------

As can be seen from the following log, doing RPCs via standard Ext.Direct means hitting concurrency limits of the underlying mechanism.

The results for `TestAction.add` and `TestAction.doEcho` only arrive after seconds, since they are blocked by the previously issued calls to `TestAction.doEchoSlow`.

    Ext.Direct initialized.
    Starting with concurrency 8
         0 calling TestAction.square
         2 calling TestAction.doEchoSlow
         3 calling TestAction.doEchoSlow
         4 calling TestAction.doEchoSlow
         4 calling TestAction.doEchoSlow
         5 calling TestAction.doEchoSlow
         6 calling TestAction.doEchoSlow
         6 calling TestAction.doEchoSlow
         7 calling TestAction.doEchoSlow
         8 calling TestAction.doEcho
         9 calling TestAction.add
        12  result TestAction.square
      3010  result TestAction.doEchoSlow
      3011  result TestAction.doEchoSlow
      3011  result TestAction.doEchoSlow
      3011  result TestAction.doEchoSlow
      3011  result TestAction.doEchoSlow
      3011  result TestAction.doEchoSlow
      3011  result TestAction.add
      3011  result TestAction.doEcho
      6011  result TestAction.doEchoSlow
      6012  result TestAction.doEchoSlow
    
Ext.Direct standard RPCs use HTTP/Ajax (via XmlHttpRequest object) and is limited by the number of concurrent connections a browser opens to a specific host.

That limit is built into browsers and fixed. The limit applies to *all* HTTP connections over *all* tabs a browser will open to a specific host, not only for `XMLHttpRequest`, but also for all other resource downloads (like for images, JS, CSS, etc).

The limit is most often **6 concurrent connections**. Actual limits for various browsers can be found [here](http://www.browserscope.org/?category=network).


Ext.Direct RPCs with Tavendo WebMQ
----------------------------------

Regarding concurrency, WAMP is able to issue multiple RPCs not only asynchronously, but also concurrently. That means that RPCs that run slow will not block subsequent RPCs.

This can be seen from the following log. Other that with standard Ext.Direct, doing RPCs via *Tavendo WebMQ*, the results for the calls to `TestAction.add` and `TestAction.doEcho` are not blocked by the slow running RPCs on `TestAction.doEchoSlow`:

    Connected to ws://192.168.1.141:9000
    Starting with concurrency 8
         0 calling TestAction.square
         1 calling TestAction.doEchoSlow
         1 calling TestAction.doEchoSlow
         1 calling TestAction.doEchoSlow
         1 calling TestAction.doEchoSlow
         1 calling TestAction.doEchoSlow
         1 calling TestAction.doEchoSlow
         1 calling TestAction.doEchoSlow
         1 calling TestAction.doEchoSlow
         1 calling TestAction.doEcho
         1 calling TestAction.add
         1  result TestAction.square
        19  result TestAction.doEcho
        20  result TestAction.add
      3001  result TestAction.doEchoSlow
      3001  result TestAction.doEchoSlow
      3001  result TestAction.doEchoSlow
      3001  result TestAction.doEchoSlow
      3001  result TestAction.doEchoSlow
      3017  result TestAction.doEchoSlow
      3017  result TestAction.doEchoSlow
      3017  result TestAction.doEchoSlow
    

