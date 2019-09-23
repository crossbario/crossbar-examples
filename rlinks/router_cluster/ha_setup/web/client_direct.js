autobahn.util.http_get_json("/config").then(
    function (config) {
        console.log(config);

        transports = [];
        for (var i = 0; i < config.nodes.length; ++i) {
            transports.push(
                {
                    url: config.nodes[i],
                    type: 'websocket',
                    serializers: [ new autobahn.serializer.MsgpackSerializer() ]
                }
            );
        }

        // WAMP connection configuration
        var connection = new autobahn.Connection({
            realm: "realm1",
            transports: transports,
            initial_retry_delay: 0.01
        });

        // callback fired upon new WAMP session
        connection.onopen = function (session, details) {
            console.log("Connected to " + details.transport.url, details);
            console.log("Crossbar.io node (router worker PID):", details.authextra.x_cb_pid);
        };


        connection.onclose = function (reason, details) {
            console.log("Disconnected:", reason, details);
        };


        // open WAMP session
        console.log('Autobahn ' + autobahn.version);
        connection.open();
    },
    function (err) {
        console.log(err);
    }
);
