## Running

Create and start a new Crossbar node with a HTTP Pusher service:

```shell
cd $HOME
mkdir test1
cd test1
crossbar init --template pusher
crossbar start
```

Start the Flask application:

```shell
python __init__.py
```

Open [http://localhost:5000](http://localhost:5000) in two browser tabs, submit form data in the first tab and watch submitted information immediately appear in the second tab.

For more information, please see [here](https://github.com/crossbario/crossbar/wiki/HTTP-Pusher-Service).
