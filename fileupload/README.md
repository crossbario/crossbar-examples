# File upload with Crossbar

This example shows how to use Crossbar.io web server with file upload. The file upload resource in crossbar accepts chunked file POSTs and publishes progress on a configurable topic. Crossbar also provides a GET response on the same resource which tells the client if a chunk has been downloaded already. So the client can easily implement resumable uploads. The demo here uses [http://www.resumablejs.com/](http://www.resumablejs.com/) for that.

## Prerequisites

To install the Web dependencies using [Bower](http://bower.io/):

```console
bower install
```

> To install Bower on Debian/Ubuntu, do `sudo npm install -g bower`.


## Running the Demo

Start Crossbar.io

```console
crossbar start
```

Now open [http://localhost:8080](http://localhost:8080) in your browser.

Also open the developer console to watch whats going on while you upload.
You will see a *very* simple web page with a link that opens the file browser menu of your browser. 

If you want to see the published file upload progress, open another browser at the same adress and open the dev console. 

## How it works

The Crossbar.io node configuration included with the demo will start a Crossbar.io node providing a file upload resource under `http://<hostname>:8080/upload`.

The JavaScript uploader POSTs requests against the upload ressource when you pick a file for upload. The request is a multipart form data request which encodes its key/values in the content part of the message. 

The JavaScript code also connects to a crossbar realm and subscribes to the 're.upload' topic. Now the client will get any event regarding uploads on this topic. The events are published by the crossbar web server and not by the client. 
