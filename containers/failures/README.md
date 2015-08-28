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

