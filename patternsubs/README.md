# Shared Registrations

This example illustrates *shared registrations*.

With shared registrations, multiple components can register the same procedure. While registering, the component can specify an *invocation policy*. We use "round-robin" in this example. With this policy, incoming calls will be forwarded in round-robin fashion to all components that have registered for the respective procedure. Essentially, this can be used for load-balancing calls to multiple instances of a component.

The example will start 8 instances of the same Python-based backend component:

* two instances running side-by-side with a router worker (which is possible, since the component is written in AutobahnPython/Twisted)
* two instances running in a first (native) container, and
* two more instances running in another container, and
* two more instances running in a guest worker each

## How to run this

You need to have Crossbar.io installed.

Then in this directory just do

`crossbar start`

and open 

`http://localhost:8080`

in your browser.

Open the JavaScript console to get logging output.