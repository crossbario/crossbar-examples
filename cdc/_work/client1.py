import os

import txaio
#txaio.use_asyncio()
txaio.use_twisted()

from autobahn.wamp import cryptosign

#from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.defer import inlineCallbacks

class MyComponent(ApplicationSession):

    def onConnect(self):
        self.log.info("connected to router")

        # authentication extra information for wamp-cryptosign
        #
        extra = {
            # forward the client pubkey: this allows us to omit authid as
            # the router can identify us with the pubkey already
            u'pubkey': self.config.extra[u'key'].public_key(),

            # not yet implemented. a public key the router should provide
            # a trustchain for it's public key. the trustroot can eg be
            # hard-coded in the client, or come from a command line option.
            u'trustroot': None,

            # not yet implemented. for authenticating the router, this
            # challenge will need to be signed by the router and send back
            # in AUTHENTICATE for client to verify. A string with a hex
            # encoded 32 bytes random value.
            u'challenge': None,

            u'channel_binding': u'tls-unique'
        }

        # now request to join ..
        self.join(self.config.realm,
                  authmethods=[u'cryptosign'],
                  authextra=extra)

    def onChallenge(self, challenge):
        self.log.info("authentication challenge received: {challenge}", challenge=challenge)
        # alright, we've got a challenge from the router.

        # not yet implemented. check the trustchain the router provided against
        # our trustroot, and check the signature provided by the
        # router for our previous challenge. if both are ok, everything
        # is fine - the router is authentic wrt our trustroot.

        # sign the challenge with our private key.
        signed_challenge = self.config.extra[u'key'].sign_challenge(self, challenge)

        # send back the signed challenge for verification
        return signed_challenge

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info("session joined: {details}", details=details)
        self.log.info("*** Hooray! We've been successfully authenticated with WAMP-cryptosign using Ed25519! ***")

        try:
            now = yield self.call(u'com.crossbario.cdc.api.get_now')
        except:
            self.log.failure()
        else:
            self.log.info("Current time at CDC: {now}", now=now)

        try:
            node_id = u'node1'
            container_id = u'ctr01'
            node_info = yield self.call(u'com.crossbario.cdc.api.get_node_info', node_id)
            yield self.call(u'com.crossbario.cdc.api.start_container_worker', node_id, container_id)
        except:
            self.log.failure()
        else:
            self.log.info('Container "{container_id}" started on node "{node_id}"', node_id=node_id, container_id=container_id)

        try:
            nodes = yield self.call(u'com.crossbario.cdc.api.get_nodes')
            self.log.info("Nodes in management realm: {nodes}", nodes=nodes)
            for node in nodes:
                node_id = node[u'node_id']
                if node[u'status'] == u'running':
                    node_info = yield self.call(u'com.crossbario.cdc.api.get_node_info', node_id)
                    self.log.info('Node info for "{node_id}": {node_info}', node_id=node_id, node_info=node_info)

                    controller_info = yield self.call(u'com.crossbario.cdc.api.get_controller_info', node_id)
                    self.log.info('Controller info for "{node_id}": {controller_info}', node_id=node_id, controller_info=controller_info)

                    controller_stats = yield self.call(u'com.crossbario.cdc.api.get_controller_stats', node_id)
                    self.log.info('Controller stats for "{node_id}": {controller_stats}', node_id=node_id, controller_stats=controller_stats)

                    workers = yield self.call(u'com.crossbario.cdc.api.get_node_workers', node_id)
                    for worker in workers:
                        worker_id = worker[u'id']
                        self.log.info('Worker "{worker_id}" running on node "{node_id}": {worker}', node_id=node_id, worker_id=worker_id, worker=worker)
                        if worker[u'status'] == u'started':

                            worker_cpu_affinity = yield self.call(u'com.crossbario.cdc.api.get_worker_cpu_affinity', node_id, worker_id)
                            self.log.info('Worker "{worker_id}" CPU affinity is {cpu_affinity}', worker_id=worker_id, cpu_affinity=worker_cpu_affinity)

                            if worker[u'type'] == u'router':
                                router_realms = yield self.call(u'com.crossbario.cdc.api.get_router_realms', node_id, worker_id)
                                self.log.info('Realms on node "{node_id}" / router "{worker_id}": {router_realms}', node_id=node_id, worker_id=worker_id, router_realms=router_realms)

                            worker_log = yield self.call(u'com.crossbario.cdc.api.get_worker_log', node_id, worker_id, 20)
                            for line in worker_log:
                                self.log.info("{line}", line=line)
                            #self.log.info('Worker log: {worker_log}', worker_log=worker_log)
                else:
                    self.log.info('Node "{node_id}" is not running', node_id=node_id)
        except:
            self.log.failure()

        self.leave()

    def onLeave(self, details):
        self.log.info("session closed: {details}", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.info("connection to router closed")


if __name__ == '__main__':

    fn = os.path.join(os.path.expanduser('~'), '.ssh', 'id_ed25519')
    fn = 'oberstet'

    key = cryptosign.SigningKey.from_ssh_key(fn)
    extra = {
        u'key': key
    }

    runner = ApplicationRunner(
        u'ws://127.0.0.1:8080/ws',
        u'com.crossbario.cdc.mrealm-test1',
        extra=extra
    )
    runner.run(MyComponent)
