# Event Retention

## tl;dr

* `PublishOptions.retain`: set to `true` to publish an event that should be retained
* `SubscribeOptions.get_retained`: subscribe and immediately receive retained events (if any)
* `EventDetails.retained`: in an event received, this flags signal if the event was retained, or an event normally dispatched


## Background

When a client subscribes to a topic, it will receive all events published to that topic _after_ it has subscribed. Events published _before_ a client has subscribed to a topic are missed.

There are different ways for a client to get at events it missed:

* event history
* acknowledged delivery
* retained events

Here, we are discussing **event retention**.

For example, imagine a sensor publishing a new sensor reading every 60s. When a subscriber of that sensors connects, it often wishes to immediately process *the last event* published to the topic, and not wait until a new event is eventually published to the topic.

Usually, you would need to implement a remote procedure either in the sensor component or in a separate backend component that caches the last known good event published to the topic, and returns the event upon being called.

With **event retention**, Crossbar.io will remember the last know good event published to a topic and provide the event to new subscribers as if the event would have been in the moment the subscriber subscribes.


## Usage

To publish an event to be available as the retained event, set the `retain` flag to `true`. Eg in AutobahnJS:

```javascript
var publish_options = {
    acknowledge: true,
    exclude_me: false,
    retain: true
};

session.publish(sensor_topic, [sensor_value], null, publish_options).then(
    function (pub) {
        console.log('successfully published!');
    },
    function (err) {
        console.log('failed to publish: ' + err);
    }
);
```

Now, subscribers that wish to receive any retained events upon subscribing can use the `get_retained` flag:

```javascript
var subscribe_options = {
    match: 'exact',
    get_retained: true
};

session.subscribe(topic, on_event, subscribe_options).then(
    function (sub) {
        console.log("subscribed successfully", sub);
    },
    function (err) {
        console.log("failed to subscribed: " + err);
    }
);
```

Retained events, that is events being dispatched to a (new) subscriber upon being asked to return retained events, and not actual new events, have their `retained` flag set.
