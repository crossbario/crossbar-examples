WebMQ Connect for Python
========================

[Tavendo WebMQ Web Message Broker](http://www.tavendo.de/webmq) extends existing Web applications to the Real-time Web.

This module provides the connector to integrate Python-based Web applications
written for popular frameworks like Django, Flask and others with Tavendo WebMQ.

Using this connector, you can push events from your Web app (or a plain Python script) to *Tavendo WebMQ* which will then forward the event to all real-time clients connected and subscribed to the topic you push to.


Installation
------------

The module has no external dependencies and has been tested on Python 2.7.

To install, the most convenient way is by using the Python package management
tools `easy_install` or `pip`.

For example:

    easy_install webmqconnect



Pushing
-------

Pushing from Python is as simple as 2 lines:


    import webmqconnect

    client = webmqconnect.Client("<Your WebMQ appliance Push endpoint>")
    client.push(topic = "<Your publication topic URI>",
                event = "Your awesome message!")


You create a client providing the Push endpoint of your WebMQ appliance. You can then use that client for pushing once or multiple times. Doing so, you provide the topic to publish under, and the event you want to publish.

The event can be any Python object that can be serialized to JSON:

    client.push(topic = "<Your publication topic URI>",
                event = {'field1': "Your published event.",
                         'field2': [1, 2, 3],
                         'field3': {'subfield1': 23
                                    'subfield2': "foobar"})


Signed Pushes
-------------

For production deployment, you might have configured your WebMQ appliance to only accept **signed pushes**.

To issue signed pushes, you need to provide an *authentication key* and a corresponding *authentication secret* when creating the push client:

    client = webmqconnect.Client("<Your WebMQ appliance Push endpoint>",
                                 authKey = "<Your Application Key>",
                                 authSecret = "<Your Application Secret>")


Pushes with Exclude and Eligible
--------------------------------

You can exclude specific WebSocket clients from receiving your pushed
message, even though they may be subscribed to the topic you are
pushing to:

    client.push(..., exclude = [<list of session IDs>])

You can also specify a whitelist of WebSocket clients

    client.push(..., eligible = [<list of session IDs>])

The session IDs are assigned to WAMP sessions by WebMQ and can be retrieved in WAMP clients.
