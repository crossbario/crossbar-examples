A very basic WAMP application which shows both RPC and PubSub, provided in examples for multiple languages & WAMP client libraries.

These can also be set up directly from Crossbar.io by doing 

```sh
crossbar init --template hello:language --appdir myappdir
```

where `language` is one of 'browser', 'cpp', 'csharp', 'erlang', 'java', 'nodejs', 'php', 'python' or 'tessel'.

Then just go to the appdir and do 

```sh
crossbar start
```

and open 

```
http://localhost:8080
```

in your browser to see the minimalist frontend.