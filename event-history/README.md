# Event History

This example demonstrates **event history** with Crossbar.io. Event history is a feature of the WAMP Advanced Profile and allows subscribers to catch up on missed events when reconnecting or to generally retrieve event history on subscriptions.

Here are two browser clients both subscribing to a topic, and each publishing to the topic periodically. The client on the right side just reconnected, and retrieved an initial event history of length 12:

![](shot1.png)

## Try yourself

To try yourself, go to this directory and start Crossbar.io

    crossbar start

Then open two browser tabs at [http://localhost:8080](http://localhost:8080) and press F12 to open the JavaScript console. Hit F5 to reload a browser tab and look at the initial event history retrieved.
