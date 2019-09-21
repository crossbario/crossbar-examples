# Crossbar.io Examples

This repository contains example code and applications for Crossbar.io.The examples are self-contained and ready to run. Each of the example directories contains an Crossbar.io configuration. In order to run the example, just got to its directory and do `crossbar start`.

## Getting started
If you are new here, we recommend you to start with our [Getting started](https://crossbar.io/docs/Getting-Started/) page.

## Overview of Examples
This overview may not be complete - so check the repository listing if you're looking for something not listed here.


To give you a better idea of a small working WAMP application there is 

* [Hello](https://github.com/crossbario/crossbarexamples/tree/master/hello) with backends for the following languages/WAMP client libraries
   + [JavaScript (Node.js backend) - Autobahn|JS](https://github.com/crossbario/crossbarexamples/tree/master/hello/nodejs)
   + [JavaScript (browser backend) - Autobahn|JS](https://github.com/crossbario/crossbarexamples/tree/master/hello/browser)
   + [Python - Autobahn|Python](https://github.com/crossbario/crossbarexamples/tree/master/hello/python)
   + [C++ - Autobahn|Cpp](https://github.com/crossbario/crossbarexamples/tree/master/hello/cpp)
   + [PHP - Thruway](https://github.com/crossbario/crossbarexamples/tree/master/hello/php)
   + [C# - WampSharp](https://github.com/crossbario/crossbarexamples/tree/master/hello/csharp)
   + [Java - jawampa](https://github.com/crossbario/crossbarexamples/tree/master/hello/java)
   + [Erlang - Erwa](https://github.com/crossbario/crossbarexamples/tree/master/hello/erlang)

For a slightly more complex (and realistic) application:

* [Votes](https://github.com/crossbario/crossbar-examples/tree/master/demos/votes) - basic WAMP application using both PubSub and RPC, with a Web frontend. Comes with backends for 
   + [Python](https://github.com/crossbario/crossbar-examples/tree/master/demos/votes/python)
   + [Node.js](https://github.com/crossbario/crossbar-examples/tree/master/demos/votes/nodejs) 
   + [the browser](https://github.com/crossbario/crossbar-examples/tree/master/demos/votes/browser)
   + [Kivy framework](https://github.com/crossbario/crossbar-examples/tree/master/demos/votes/kivy)


The following examples cover **specific features** of WAMP/Crossbar.io

* [Authentication](https://github.com/crossbario/crossbar-examples/tree/master/authentication) and its [Documentation](https://crossbar.io/docs/Authentication/)

   + Ticket, both [static](https://github.com/crossbario/crossbar-examples/tree/master/authentication/ticket/static) and [dynamic](https://github.com/crossbario/crossbar-examples/tree/master/authentication/ticket/dynamic)
   + WAMP CRA, both [static](https://github.com/crossbario/crossbar-examples/tree/master/authentication/wampcra/static) and [dynamic](https://github.com/crossbario/crossbar-examples/tree/master/authentication/wampcra/dynamic)
   + TLS, both [static](https://github.com/crossbario/crossbar-examples/tree/master/authentication/tls/static) and [dynamic](https://github.com/crossbario/crossbar-examples/tree/master/authentication/tls/dynamic)
   + CryptoSign, both [static](https://github.com/crossbario/crossbar-examples/tree/master/authentication/cryptosign/static) and [dynamic](https://github.com/crossbario/crossbar-examples/tree/master/authentication/cryptosign/dynamic)
   + Anonymous, both [static](https://github.com/crossbario/crossbar-examples/tree/master/authentication/anonymous/static) and [dynamic](https://github.com/crossbario/crossbar-examples/tree/master/authentication/anonymous/dynamic)
   + [Cookie](https://github.com/crossbario/crossbar-examples/tree/master/authentication/cookie)
   + [Advanced](https://github.com/crossbario/crossbar-examples/tree/master/authentication/advanced)


* [Authorization](https://github.com/codelectron/crossbar-examples/tree/master/authorization) and its [Documentation](https://crossbar.io/docs/Authorization/)
   + Dynamic, both [container](https://github.com/crossbario/crossbar-examples/tree/master/authorization/dynamic/container) and [embedded](https://github.com/crossbario/crossbar-examples/tree/master/authorization/dynamic/embedded)
   + [Static](https://crossbar.io/docs/Authorization/#static-authorization)

* [Database](https://github.com/crossbario/crossbar-examples/tree/master/database) 
   + [Postgresql](https://github.com/crossbario/crossbar-examples/tree/master/database/postgresql) 
   + [Oracle](https://github.com/crossbario/crossbar-examples/tree/master/database/oracle/publisher) 
   
* [Payload Encryption](https://github.com/crossbario/crossbar-examples/tree/master/encryption/)
   + [Cryptobox](https://github.com/crossbario/crossbar-examples/tree/master/encryption/cryptobox)
   + [TLS](https://github.com/crossbario/crossbar-examples/tree/master/encryption/tls)
   
* [Event history](https://github.com/crossbario/crossbar-examples/tree/master/event-history)   Event history is a feature of the WAMP Advanced Profile and allows subscribers to catch up on missed events when reconnecting or to generally retrieve event history on subscriptions.
* [Exclude Subscribers](https://github.com/crossbario/crossbar-examples/tree/master/exclude_subscribers)   This example shows several ways to exclude subscribers from getting a subscription.
* [File upload with Crossbar](https://github.com/crossbario/crossbar-examples/tree/master/fileupload)  This example shows how to use Crossbar.io web server with file upload. 
* [Flash Fallback](https://github.com/crossbario/crossbarexamples/tree/master/flash) - How to use Flash fallback for older browsers without WebSocket support (mainly there for IE<10)
* [Longpoll](https://github.com/crossbario/crossbarexamples/tree/master/longpoll) - How to use the Longpoll fallback for older browsers without WebSocket support
* [Metaapi](https://github.com/crossbario/crossbarexamples/tree/master/metaapi) - How to subscribe to meta-events and use meta-procedures (get information about sessions, subscriptions and registrations)
* [Secure WebSockets (WSS)](https://github.com/crossbario/crossbarexamples/tree/master/wss/python)
* [MQTT](https://github.com/crossbario/crossbar-examples/tree/master/mqtt) 
* [Pattern-based Registrations](https://github.com/crossbario/crossbar-examples/tree/master/patternregs) - This example illustrates pattern-based registrations.
* [Pattern-based Registrations](https://github.com/crossbario/crossbar-examples/tree/master/patternsubs) - This example illustrates pattern-based subscriptions.
* [Payloadcodec](https://github.com/crossbario/crossbar-examples/tree/master/payloadcodec) - Setting up serialization of custom types in Crossbar.io
* [Prompt](https://github.com/crossbario/crossbar-examples/tree/master/prompt) - Getting user input asynchronously
* [REST](https://github.com/crossbario/crossbar-examples/tree/master/rest)
   + [Publisher](https://github.com/crossbario/crossbar-examples/tree/master/rest/publisher)
   + [Publisher TLS](https://github.com/crossbario/crossbar-examples/tree/master/rest/publisher_tls)
   + [Subscriber](https://github.com/crossbario/crossbar-examples/tree/master/rest/subscriber)
   + [Webhooks](https://github.com/crossbario/crossbar-examples/tree/master/rest/webhooks)
   + [Caller](https://github.com/crossbario/crossbar-examples/tree/master/rest/caller)
   + [Callee](https://github.com/crossbario/crossbar-examples/tree/master/rest/callee)
* [Scaling-Microservices](https://github.com/crossbario/crossbar-examples/tree/master/scaling-microservices) - Transparent scaling of microservices
* [Serializers](https://github.com/crossbario/crossbar-examples/tree/master/serializers) - Configuring serializers in Crossbar.io
* [Shared Registeration](https://github.com/crossbario/crossbar-examples/tree/master/sharedregs) - With shared registrations, multiple components can register the same procedure. 
* [Universal Transport](https://github.com/crossbario/crossbar-examples/tree/master/unitransport) - The universal transport allows to service multiple protocols on one listening endpoint, such as the default TLS listening port: WAMP-over-RawSocket,WAMP-over-WebSocket,Web Resources


And finally, there are examples using specific devices or technologies:

* [Raspberry Pi](https://github.com/codelectron/crossbar-examples/tree/master/iotcookbook/device/pi)
* [Tessel microcontroller](https://github.com/codelectron/crossbar-examples/tree/master/iotcookbook/device/tessel)
* [Django framework](https://github.com/codelectron/crossbar-examples/tree/master/django/realtimemonitor)
* [ExpressJS](https://github.com/codelectron/crossbar-examples/tree/master/expressjs)
* [ReactJS](https://github.com/crossbario/crossbar-examples/tree/master/reactjs)

## Adapting for other languages

Most of the examples are for Python and JavaScript, even though often what is shown would work with other languages and WAMP client libraries. This is purely due to lack of resources. We want you to use Crossbar.io with whatever language or languages you want.

Anybody is very welcome to adapt example code for other languages.

Similarly, you're welcome to add examples that you think provide value to other users.

To do either, just send us a pull request.

## Keeping things up to date

As you'll probably notice sooner or later, Crossbar.io is a work in progress. Core functionality is stable, but there is a lot of development going on around it. We try to keep these examples working. If you find that something is broken, then please file an issue (or fix it and send us a pull request).

## Additional Examples

For historic reasons, the [Autobahn|Python repository](https://github.com/crossbario/autobahn-python) also contains some examples for using WAMP. The most relevant to the general Crossbar.io user can be found in [this directory](https://github.com/tavendo/AutobahnPython/tree/master/examples/twisted/wamp). These are almost always for both Python and JavaScript (using Autobahn|JS).

Some of the instructions here still assume a basic router in Autobahn|Python which has since been removed, but in principle they should run with Crossbar.io. The chance of running across an outdated example here are higher, however. Should you find such an example, please file an issue (or fix it and send us a pull request). 
 
