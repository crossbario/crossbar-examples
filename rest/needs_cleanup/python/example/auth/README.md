# WebMQ Authentication

This example shows how WebMQ WebSocket sessions can be authenticated via the user/password management that you likely already have in your Web application (in this case a Flask-based).

The advantage of this scheme is that WebMQ itself needs no *user* management itself, but only a per-application credential shared with the Web app.


# Test

Start WebMQ and add an application credential with key `foobar` and password `secret`.

> You can manage application credentials from the WebMQ management web console under *Home/Configuration/Authentication/Applications Credentials*.
> 

Start the Flask example server:

    cd WebMQConnectPython/examples/auth
    python __init__.py ws://127.0.0.1/ws

replacing `ws://127.0.0.1/ws` with the WebSocket URL of your WebMQ instance.

Open `http://localhost:8000` in your Web browser and login as `joe` with password `secret`.

Upon successful login you will be forwarded to a page that opens an authenticated WebSocket connection to WebMQ and see the following:

    "connected", "ws://127.0.0.1/ws"
    "authenticated", {"rpc":[{"call":true,"uri":"http://api.wamp.ws/procedure#ping"},{"call":true,"uri":"http://api.wamp.ws/procedure#echo"}],"pubsub":[]}
    

# How it works

A user authenticates via a plain old HTML form based login page (`login.html`). Upon successful login, a cookie is set, marking the Web session as authenticated and providing session storage.

The JavaScript within the page rendered after successful login (`index.html`) connects to WebMQ. 

During authentication of that connection, WebMQ sends a challenge to the client which needs to be signed using the password from the application credentials.

Since only the Flask server-side knows that, the client sends the WebMQ challenge to Flask via a plain old AJAX call (HTTP/POST) to get it signed.

When the user is logged in, Flask will sign the challenge, send it back to the client, and the client can provide the signature to WebMQ.
