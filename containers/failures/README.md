# Container startup failures

To run, type:

```
make test
```

Please see [here](https://gist.github.com/oberstet/4b9d2d898e4f0ba42d6d) for a complete log.


## Working

The working case.

## Module not found (Failure 1)

Crossbar.io can't load the user's application component, since the Python module can't be found.

Usually, the fix is to modify the Python module search path using the `options.pythonpath` configuration parameter.

## Class not found (Failure 2)

Crossbar.io can't load the user's application component, since while the Python module can be found, there is no class (or factory) within that module.

Usually, the fix is to use the correct class/factory name in the node configuration and/or Python module.

## Class instantiation failed (Failure 3)

The module and class configured was found, but calling the class constructor (or the factory) failed.

Usually, an exception escapes the class constructor or factory. You need to fix that.

## A callback raises an exception (Failure 4)

In this example, a user callback invoked by Autobahn (here, `onJoin`) raises an exception. This is fatal.

The fix is: don't let escape exceptions from callbacks.

## The component exits (Failure 5)

Here, we call the `leave()` method on the session to leave the realm, the disconnect the underlying transport. The component goes away, with it the container, and with it the whole node.

## The component exits (Failure 6)

The same as above, but we end only after some seconds.

## The transport cannot be established (Failure 7)

The transport from the container to the router worker could not be estabished. In this case, wrong port.

## The transport cannot be established (Failure 8)

The transport from the container to the router worker could not be estabished. In this case, wrong WebSocket URL (the trailing `ws` is missing to fit hte router configuration).
