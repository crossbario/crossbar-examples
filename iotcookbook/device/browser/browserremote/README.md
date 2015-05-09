# WAMP browser remote control

Control your browser remotely via WAMP.

* reloading the current page
* navigating to another page
* displaying a page in a second tab

**Reload** enables you to refresh content which is displayed remotely.

**Navigating to another page** allows you to chain content, if you can modify all pages to load this control code.

**Displaying a page in a second tab** enables you to sequence arbitrary web pages for display. (This requires allowing pop-ups for the domain the controlled page is served from.)

These features are just a basic set, and can be easily extended to other control should you need this. For example, you could navigate the browser history or even modify page content.

## Try it out

Do 

```
crossbar start
```

in this example's base directory.

This will serve a demo page with the sample controls at

```
localhost:8080
```

Then launch the page to control using the provided link.


## Using it

Browser remote control requires that you load two JavaScript files in your page:

* AutobahnJS
* remote.js

AutobahnJS provides the WAMP connectivity, while `remote.js` actually establishes the WAMP connection, subscribes to control events and issues commands to the browser.

> Note: Here AutobahnJS is loaded from our S3 storage. This is provided for development purposes only, and some restrictions regarding download IPs apply. For production, please host your own version!

* [What's this WAMP?](http://wamp.ws)
* [Remote control Reveal.js presentations via WAMP](https://github.com/crossbario/crossbarexamples/tree/master/revealremote)