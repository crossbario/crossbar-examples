# WAMP Remote Control for Reveal.js


This allows you to remote control a Reveal.js presentation remotely via WAMP.

## Try it out

Do 

```
crossbar start
```

in this example's base directory.

This will serve a demo page with some sample controls at

```
localhost:8080
```

Then open the provided sample presentation using the link in the first line of the control page.


## Using it

Remote control requires loading two additional JavaScript files in your Reveal.js presentation:

* AutobahnJS
* revealremote.js

AutobahnJS provides the WAMP connectivity, while `revealremote.js` actually establishes the WAMP connection, subscribes to control events and issues commands to Reveal.js.

This presently contains just basic navigation commands plus setup for autoplay, but can be trivially extended to support the entire Reveal.js API.

## Links

* [What's this WAMP?](http://wamp.ws)
* [Reveal.js](https://github.com/hakimel/reveal.js/)
* [remote control webpage content via WAMP](https://github.com/crossbario/crossbarexamples/tree/master/browserremote) - combine this with the reveal control to e.g. do playlists of presentations, or presentations with other web content 
