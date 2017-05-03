# Crossbar.io and MQTT

* [basic](basic) - Basic integration services and configuration
* pattern/wildcard subscriptions
* last will messages
* QoS levels


## Limitations

### MQTT Topics and WAMP URIs

MQTT Topics and Topic Filters have these restrictions:

1. cannot exceed 65535 octets when UTF8 encoded (MQTT Spec 1.5.3)
2. must not contain certain codepoints (such as the null character U+0000)


### MQTT Keep-alive

MQTT keep-alive / heartbeat messaging is not yet implemented.


### MQTT QoS 2

Crossbar.io [does not support](https://github.com/crossbario/crossbar/issues/1046) QoS 2 for publishers nor for subscribers.


### MQTT Session Resumption

Crossbar.io [does not support](https://github.com/crossbario/crossbar/issues/892) resuming a session after a loss of transport. That is, the MQTT CONNECT message cannot have its `clean_session=0` flag unset (a new session is always started).


### MQTT Client Identifier
