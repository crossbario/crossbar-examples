# Using MQTT with Pattern-based Subscriptions

MQTT allows to subscribe to prefix- and wildcard-based topic patterns.

For example:

1. Prefix-pattern: `mqtt/test/mytopic/#`
2. Wildcard pattern: `mqtt/+/mytopic/+`

MQTT pattern-based subscribes are automatically transformed by Crossbar.io into regular WAMP pattern-based subscriptions.

The MQTT pattern above are converted to:

1. `mqtt.test.mytopic.` with `match=prefix`
2. `mqtt..mytopic.` with `match=wildcard`
