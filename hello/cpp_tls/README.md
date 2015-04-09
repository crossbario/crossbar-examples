# Hello WAMP in C++11

A [C++11](http://en.wikipedia.org/wiki/C%2B%2B11) / [AutobahnCpp](https://github.com/tavendo/AutobahnCpp) based "Hello world!" example WAMP application.

**This is running RawSocket over TLS**.

Here are some pointers:

* http://www.boost.org/doc/libs/1_57_0/doc/html/boost_asio/overview/ssl.html


**See: [Getting started with C++](https://github.com/crossbario/crossbar/wiki/Getting-started-with-C--)**

## How to run

Build the app using [SCons](http://scons.org/):

```shell
scons
```

Start Crossbar by doing:

```shell
crossbar start
```

Open [`http://localhost:8080/`](http://localhost:8080/) (or wherever Crossbar runs) in your browser.

## How to hack

All C++ backend code is in `hello.cpp`. All JavaScript frontend code is in `./web/index.html`.
