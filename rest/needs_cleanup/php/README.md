WebMQ Connect for PHP
=====================

[Tavendo WebMQ Web Message Broker](http://www.tavendo.de/webmq) extends existing Web applications to the Real-time Web.

This module provides the connector to integrate PHP-based Web applications with Tavendo WebMQ.

Using this connector, you can push events from your Web app to *Tavendo WebMQ* which will then forward the event to all real-time clients connected and subscribed to the topic you push to.


Requirements
------------

The only requirement is having **cURL** enabled in your PHP installation.


Getting started with PHP on Windows
-----------------------------------

1. Download [PHP for Windows](http://windows.php.net/download/)

2. Unpack PHP to `C:/php543`

3. Copy `C:/php543/php.ini-development` to `C:/php543/php.ini`

4. Edit `C:/php543/php.ini` for:

        extension_dir = "ext"
        extension=php_curl.dll

5. Clone the repository (or download a [zipped archive](https://github.com/tavendo/WebMQConnectPHP/zipball/master) ):

        git clone git://github.com/tavendo/WebMQConnectPHP.git      

6. Start the basic example:

        cd WebMQConnectPHP/examples/basic
        php -S localhost:8000

7. Goto `http://localhost:8000` in your browser and open the *Real-time client* and the *User Form* from there.

8. Submit data in the *User Form* and see how data arrives immediately in the *Real-time Client*

How it works
------------

The *Real-time Client* connects to *Tavendo WebMQ* via WebSocket/WAMP and subscribes to a specific topic.

When a user submits the *User Form*, the HTTP/POST containing the form data is received by PHP. From there, the form data is pushed to *Tavendo WebMQ* again via a (outgoing) HTTP/POST.

*Tavendo WebMQ* receives the pushed data and dispatches the event under the specified topic. Connected clients subscribed to that topic will immediately receive the event.
