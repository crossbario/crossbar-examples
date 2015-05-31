# Live Visitors Counter Web Component

This is a demo of a live visitors counter for a Web site, implemented as a Web component, and using WAMP/Crossbar.io.

## Usage

* To start the demo, you need Crossbar.io installed - see [the Quick Start instructions](http://crossbar.io/docs/Quick-Start/). 
* The backend is run in Node.js, so you also need that. Crossbar.io tries to determine the location of the Node.js executable, but on some systems you may need to help out. Open `config.json` in the `.crossbar` directory, and look for `"executable": "node"`. E.g. on Ubuntu, you'll need to replace this with `"executable": "nodejs"` (or you can just give an absolute path to the executable).
* The node backend relies on Autobahn|JS and bower. Install these by doing `npm install`
* The widget uses the standardized Web components syntax. However, the Polymer polyfills are always loaded. Install these by doing `bower install`.
* The URL of the computer running your Crossbar.io instance needs to be set in `index.html`, as part of   
```
<crossbar-visitors data-config='{ "routerUrl": "ws://192.168.1.134:8080/ws", "label": "Current Visitors" }'></crossbar-visitors>
```
* Now start Crossbar.io with `crossbar start`. This starts Crossbar, the backend component running in Node.js, and the static Web server which serves `index.html`.
* Open `http://localhost:8080` in a browser on the machine you're running Crossbar on. This displays the index page with the visitors widget. Open more pages to see the count increase, close them to see a decrease.

