# Adding Real-Time to Django Applications

This is the example code for the [Adding Real-Time to Django Applications tutorial](http://crossbar.io/docs/Adding-Real-Time-to-Django-Applications/) in the Crossbar.io documentation.

> Note: The SQLite database file `db.sqlite3` in the directory here is needed (for now), since it is preinitialized with necessary database tables already.


## Try

In addition to Crossbar.io, you will need Django and some other packages:

```console
pip install --upgrade django requests psutil
```

In a first terminal, start Crossbar.io:

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/django/realtimemonitor$ crossbar start
2016-02-12T12:14:28+0100 [Controller  25351] Automatically choosing optimal Twisted reactor
2016-02-12T12:14:28+0100 [Controller  25351] Running on Linux and optimal reactor (epoll) was installed.
2016-02-12T12:14:29+0100 [Controller  25351]      __  __  __  __  __  __      __     __
2016-02-12T12:14:29+0100 [Controller  25351]     /  `|__)/  \/__`/__`|__) /\ |__)  |/  \
2016-02-12T12:14:29+0100 [Controller  25351]     \__,|  \\__/.__/.__/|__)/~~\|  \. |\__/
2016-02-12T12:14:29+0100 [Controller  25351]
2016-02-12T12:14:29+0100 [Controller  25351]     Crossbar.io Version: 0.13.0
2016-02-12T12:14:29+0100 [Controller  25351]     Node Public Key: 4f65c4984f72b098319fc4bb9dcca85c1c526ebb591a0229457338c7dbd198d1
2016-02-12T12:14:29+0100 [Controller  25351]
2016-02-12T12:14:29+0100 [Controller  25351] Running from node directory '/home/oberstet/scm/crossbario/crossbarexamples/django/realtimemonitor/.crossbar'
2016-02-12T12:14:29+0100 [Controller  25351] Controller process starting (CPython-EPollReactor) ..
2016-02-12T12:14:29+0100 [Controller  25351] Node configuration loaded from 'config.json'
2016-02-12T12:14:29+0100 [Controller  25351] Node ID 'thinkpad-t430s' set from hostname
2016-02-12T12:14:29+0100 [Controller  25351] Using default node shutdown triggers [u'shutdown_on_worker_exit']
2016-02-12T12:14:29+0100 [Controller  25351] Joined realm 'crossbar' on node management router
2016-02-12T12:14:29+0100 [Controller  25351] Starting Router with ID 'worker1'...
2016-02-12T12:14:29+0100 [Router      25356] Worker process starting (CPython-EPollReactor) ..
2016-02-12T12:14:29+0100 [Controller  25351] Router with ID 'worker1' and PID 25356 started
2016-02-12T12:14:29+0100 [Router      25356] Realm 'realm1' started
2016-02-12T12:14:29+0100 [Controller  25351] Router 'worker1': realm 'realm1' (named 'realm1') started
2016-02-12T12:14:29+0100 [Controller  25351] Router 'worker1': role 'role1' (named 'anonymous') started on realm 'realm1'
2016-02-12T12:14:29+0100 [Router      25356] Site starting on 8080
2016-02-12T12:14:29+0100 [Controller  25351] Router 'worker1': transport 'transport1' started
2016-02-12T12:14:32+0100 [Router      25356] /home/oberstet/python279_1/lib/python2.7/site-packages/django/template/utils.py:37: RemovedInDjango110Warning: You haven't defined a TEMPLATES setting. You must do so before upgrading to Django 1.10. Otherwise Django will be unable to load templates.
2016-02-12T12:14:32+0100 [Router      25356]   "unable to load templates.", RemovedInDjango110Warning)
2016-02-12T12:14:32+0100 [Router      25356]
2016-02-12T12:14:32+0100 [Router      25356] /home/oberstet/scm/crossbario/crossbarexamples/django/realtimemonitor/django_project/urls.py:7: RemovedInDjango110Warning: Support for string view arguments to url() is deprecated and will be removed in Django 1.10 (got django_app.views.clients). Pass the callable instead.
2016-02-12T12:14:32+0100 [Router      25356]   url(r'^clients/', 'django_app.views.clients'),
2016-02-12T12:14:32+0100 [Router      25356]
2016-02-12T12:14:32+0100 [Router      25356] /home/oberstet/scm/crossbario/crossbarexamples/django/realtimemonitor/django_project/urls.py:8: RemovedInDjango110Warning: django.conf.urls.patterns() is deprecated and will be removed in Django 1.10. Update your urlpatterns to be a list of django.conf.urls.url() instances instead.
2016-02-12T12:14:32+0100 [Router      25356]   url(r'^$', TemplateView.as_view(template_name='dashboard.html')),
2016-02-12T12:14:32+0100 [Router      25356]
2016-02-12T12:14:32+0100 [Router      25356] Client config for retrieved for IP '10.200.202.66'
2016-02-12T12:15:56+0100 [Router      25356] Client config for retrieved for IP '10.200.202.66'
2016-02-12T12:16:44+0100 [Router      25356] Client config for retrieved for IP '10.200.202.66'
```

In a second terminal, start the monitoring client:

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/django/realtimemonitor$ python client.py
2016-02-12T12:16:44+0100 Connected
2016-02-12T12:16:44+0100 Entering stats loop ..
2016-02-12T12:16:44+0100 Tick
2016-02-12T12:16:44+0100 Stats published: {'memory': '7.59GiB/15.40GiB (21.2%)', 'ip': u'10.200.202.66', 'disks': {'/media/truecrypt12': '0.00GiB/0.00GiB (74.2%)', '/': '72.16GiB/453.85GiB (15.9%)'}, 'name': 'thinkpad-t430s', 'cpus': ('10.0%', '80.0%', '9.1%', '10.0%')}
2016-02-12T12:16:45+0100 Tick
2016-02-12T12:16:45+0100 Stats published: {'memory': '7.59GiB/15.40GiB (21.2%)', 'ip': u'10.200.202.66', 'disks': {'/media/truecrypt12': '0.00GiB/0.00GiB (74.2%)', '/': '72.16GiB/453.85GiB (15.9%)'}, 'name': 'thinkpad-t430s', 'cpus': ('4.0%', '2.0%', '3.0%', '4.0%')}
2016-02-12T12:16:46+0100 Tick
2016-02-12T12:16:46+0100 Stats published: {'memory': '7.60GiB/15.40GiB (21.2%)', 'ip': u'10.200.202.66', 'disks': {'/media/truecrypt12': '0.00GiB/0.00GiB (74.2%)', '/': '72.16GiB/453.85GiB (15.9%)'}, 'name': 'thinkpad-t430s', 'cpus': ('4.0%', '2.0%', '3.0%', '1.0%')}
2016-02-12T12:16:47+0100 Tick
...
```
