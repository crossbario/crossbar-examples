Detecting WebSocket Support with WebMQ Connect for PHP
======================================================

With *Tavendo WebMQ*, there are 4 cases regarding browser support:

 1. browser supports native RFC6455/Hybi-10+ WebSocket
 2. browser support only Hixie-76 WebSocket
 3. browser supports WebSocket only via Flash polyfill
 4. browser does not support WebSocket

The example here shows how to detect the case in server-side PHP.

Using the detection, you can then i.e. only include the Flash polyfill for browsers that actually need it, and avoid including the polyfill for browsers that don't need it and would thus download the respective files with any need.

You can also redirect the user to a specific page when WebSocket isn't supported at all.


