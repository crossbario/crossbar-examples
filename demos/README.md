The demos folder contains small WAMP/Crossbar.io applications with a bit more polish than the general examples.

The general examples are there to illustrate a particular feature of WAMP or Crossbar.io, and only contain the parts necessary to do so.

The demos go beyond that in that they are mini-applications with graphical frontends (though they may not always do something useful).

Each demo is self-contained. In the base directory of a demo, just do

```
crossbar start
```

and then open a browser to

```
http://localhost:8080
```

to see the frontend.

For some demos, you need to install dependencies or go through a (simple) setup process. See the respective readmes.

Additionally, there's an overview page from which you can launch any of the demos, which is located in the `overview` folder. Here you also start crossbar and then open your browser as above.

> Note: A lot of these demos got started long ago for a precursor to Crossbar.io. This means first of all that they mainly only do PubSub. It also means that we wouldn't necessarily implement them precisely like this anymore - so be aware of this when you look over the sources! If you think something is iffy code, then there's every possibility it is. (Cleaning up things here is definitely on our to-do list - it's just not a priority.)
