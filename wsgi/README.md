# WSGI Web service

See the docs [here](http://crossbar.io/docs/WSGI-Host-Service/).

> Note that the WSGI Web service is not yet supported on Python 3 (only on Python 2). See [here](https://github.com/crossbario/crossbar/issues/605). The reason is that Twisted does not yet (as of v15.5) support WSGI on Python 3. It will be in Twisted 16.0. See [here](https://twistedmatrix.com/trac/ticket/7993)

## Try

Install Flask:

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/wsgi$ pip install -U flask
Requirement already up-to-date: flask in /home/oberstet/python279_1/lib/python2.7/site-packages
Requirement already up-to-date: Werkzeug>=0.7 in /home/oberstet/python279_1/lib/python2.7/site-packages (from flask)
Requirement already up-to-date: Jinja2>=2.4 in /home/oberstet/python279_1/lib/python2.7/site-packages (from flask)
Requirement already up-to-date: itsdangerous>=0.21 in /home/oberstet/python279_1/lib/python2.7/site-packages (from flask)
Requirement already up-to-date: MarkupSafe in /home/oberstet/python279_1/lib/python2.7/site-packages (from Jinja2>=2.4->flask)
```

Start Crossbar.io:

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/wsgi$ crossbar start
2016-02-12T12:00:24+0100 [Controller  25153] Automatically choosing optimal Twisted reactor
2016-02-12T12:00:24+0100 [Controller  25153] Running on Linux and optimal reactor (epoll) was installed.
2016-02-12T12:00:24+0100 [Controller  25153]      __  __  __  __  __  __      __     __
2016-02-12T12:00:24+0100 [Controller  25153]     /  `|__)/  \/__`/__`|__) /\ |__)  |/  \
2016-02-12T12:00:24+0100 [Controller  25153]     \__,|  \\__/.__/.__/|__)/~~\|  \. |\__/
2016-02-12T12:00:24+0100 [Controller  25153]
2016-02-12T12:00:24+0100 [Controller  25153]     Crossbar.io Version: 0.13.0
2016-02-12T12:00:24+0100 [Controller  25153]     Node Public Key: 64b1dad0a5293c084e4b35589c67e95561d920b5972b75a3026fd7bd19cb591a
2016-02-12T12:00:24+0100 [Controller  25153]
2016-02-12T12:00:24+0100 [Controller  25153] Running from node directory '/home/oberstet/scm/crossbario/crossbarexamples/wsgi/.crossbar'
2016-02-12T12:00:24+0100 [Controller  25153] Controller process starting (CPython-EPollReactor) ..
2016-02-12T12:00:24+0100 [Controller  25153] Node configuration loaded from 'config.json'
2016-02-12T12:00:24+0100 [Controller  25153] Node ID 'thinkpad-t430s' set from hostname
2016-02-12T12:00:24+0100 [Controller  25153] Using default node shutdown triggers [u'shutdown_on_worker_exit']
2016-02-12T12:00:24+0100 [Controller  25153] Joined realm 'crossbar' on node management router
2016-02-12T12:00:24+0100 [Controller  25153] Starting Router with ID 'worker1'...
2016-02-12T12:00:25+0100 [Router      25158] Worker process starting (CPython-EPollReactor) ..
2016-02-12T12:00:25+0100 [Controller  25153] Router with ID 'worker1' and PID 25158 started
2016-02-12T12:00:25+0100 [Router      25158] Realm 'realm1' started
2016-02-12T12:00:25+0100 [Controller  25153] Router 'worker1': realm 'realm1' (named 'realm1') started
2016-02-12T12:00:25+0100 [Controller  25153] Router 'worker1': role 'role1' (named 'anonymous') started on realm 'realm1'
2016-02-12T12:00:25+0100 [Router      25158] Site starting on 8080
2016-02-12T12:00:25+0100 [Controller  25153] Router 'worker1': transport 'transport1' started
...
```

Now open [http://127.0.0.1:8080/](http://127.0.0.1:8080/) in your web browser. You should see an awesome message "Hello from Crossbar.io" being rendered. This message is rendered dynamically from a Flask/WSGI app using a Jinja2 template.
