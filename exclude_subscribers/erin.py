
import random
from os import environ, urandom
from os.path import exists
from functools import partial

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp import cryptosign
from autobahn.wamp.types import PublishOptions


if not exists('erin.priv'):
    with open('erin.priv', 'wb') as f:
        f.write(urandom(32))


class Component(ApplicationSession):
    """
    """
    key = cryptosign.CryptosignKey.from_file('erin.priv')

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")
        print("  authid: {}".format(details.authid))
        print("authrole: {}".format(details.authrole))

        def got_heartbeat(name, counter):
            print("hearbeat: {}: {}".format(name, counter))

        for name in ['erin', 'bob', 'carol', 'dave', 'erin']:
            yield self.subscribe(
                partial(got_heartbeat, name),
                'public.heartbeat.{}'.format(name),
            )

        counter = 0
        topic = 'public.heartbeat.erin'
        while True:
            print("publish '{}'".format(topic))
            self.publish(
                topic, '{}: to alice, bob, dave'.format(counter),
                options=PublishOptions(
                    eligible_authid=['alice', 'bob', 'dave'],
                ),
            )
            if counter % 2:
                self.publish(
                    topic, '{}: "beta" role'.format(counter),
                    options=PublishOptions(
                        eligible_authrole="beta",
                        exclude_me=False,
                    ),
                )
            counter += 1
            yield sleep(3)

    def onConnect(self):
        extra = {
            'pubkey': self.key.public_key(),
            'channel_binding': 'tls-unique'
        }

        # now request to join ..
        self.join(self.config.realm,
                  authmethods=['cryptosign'],
                  authid='erin',
                  authextra=extra)

    def onChallenge(self, challenge):
        self.log.info("authentication challenge received: {challenge}", challenge=challenge)
        # alright, we've got a challenge from the router.

        # not yet implemented. check the trustchain the router provided against
        # our trustroot, and check the signature provided by the
        # router for our previous challenge. if both are ok, everything
        # is fine - the router is authentic wrt our trustroot.

        # sign the challenge with our private key.
        signed_challenge = self.key.sign_challenge(self, challenge)

        # send back the signed challenge for verification
        return signed_challenge


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", "ws://127.0.0.1:8080/ws"),
        "crossbardemo",
    )
    print("Erin pubkey: {}".format(Component.key.public_key()))
    runner.run(Component)
