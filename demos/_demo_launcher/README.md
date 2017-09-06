# Demo Launcher

To start a Crossbar.io node with all the demos (exactly as on [https://demo.crossbar.io](https://demo.crossbar.io)), open a terminal, go to this folder and

```console
crossbar start
```

Now open [http://localhost:8080](http://localhost:8080) in your browser. You should see an overview page of the Crossbar.io demos, launchable from there.

> Note: This also runs the backends of any demos which require them.




```console
ubuntu@cb-eu1:~$ docker ps

CONTAINER ID        IMAGE                               COMMAND                  CREATED             STATUS              PORTS               NAMES
4aff8e204257        crossbario/crossbar-fabric:latest   "/usr/local/bin/cr..."   6 minutes ago       Up 2 minutes                            cbdemo
```


```
ubuntu@cb-eu1:~$ sudo systemctl status

* cb-eu1
    State: running
     Jobs: 0 queued
   Failed: 0 units
    Since: Wed 2017-09-06 17:46:14 UTC; 43s ago
   CGroup: /
           ├─docker
           │ └─4aff8e2042573e6ca93cb002d18d4642d411e2deecfb980d5a7e1a5dd8fa680b
           │   ├─1649 crossbar-controller
           │   └─1700 crossbar-worker [crossbarfabric.router.FabricRouterWorkerSession]
...
```
