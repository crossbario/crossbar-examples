# File upload with Crossbar

This example shows how to use Crossbar.io web server with file upload. The file upload resource in crossbar accepts chunked file POSTs and publishes progress on a configurable topic. Crossbar also provides a GET response on the same resource which tells the client if a chunk has been downloaded already. So the client can easily implement resumable uploads. The demo here uses [www.resumablejs.com](www.resumablejs.com) for that.

## Prerequisites

You need to have Crossbar.io installed. 

	pip install crossbar


## Running the Demo

The demo folder `fileupload_node` is a working crossbar node folder. Just go inside and start Crossbar.io by doing

	cd fileupload_node
	crossbar start

Now open [http://localhost:8089](http://localhost:8089) in your browser.

Also open the developer console to watch whats going on while you upload.
You will see a *very* simple web page with a link that opens the file browser menu of your browser. 

If you want to see the published file upload progress, open another browser at the same adress and open the dev console. 

## How it works

The Crossbar.io node configuration included with the demo will start a Crossbar.io node providing a file upload resource under 127.0.0.1:8089/upload.

The javascript uploader POSTs requests against the upload ressource when you pick a file for upload. The request is a multipart form data request which encodes its key/values in the content part of the message. 

The Javascript code also connects to a crossbar realm and subscribes to the 're.upload' topic. Now the client will get any event regarding uploads on this topic. The events are published by the crossbar web server and not by the client. 







