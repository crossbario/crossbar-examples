#
# Example WAMP client, using cbor2 as a payload codec
#
# Requires packages: cbor2, umsgpack
#
# Note that the example is slightly verbose, to show more
# features and with extensive logging
#

import cbor2
import txaio
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.exception import SerializationError
from autobahn.wamp.interfaces import IPayloadCodec
from autobahn.wamp.serializer import MsgPackSerializer
from autobahn.wamp.types import PublishOptions, EncodedPayload
from twisted.internet.defer import inlineCallbacks

# topic we publish and subscribe to
TOPIC = u'test.mytopic1'

# the chosen encoding algorithm (totally arbitrary beyond the mandatory "x_" prefix)
ENC_ALGO = u'x_cbor2_custom'

# arbitrarily chosen CBOR tag number
CBOR_TAGNUM = 9000


class Company(object):
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, name, rank):
        employee = Employee(name, rank, self)
        self.employees.append(employee)
        return employee

    def __repr__(self):
        return 'Company(name={self.name}, employees={self.employees})'.format(self=self)


class Employee(object):
    def __init__(self, name, title, company):
        self.name = name
        self.title = title
        self.company = company

    def __repr__(self):
        return 'Employee(name={self.name}, title={self.title})'.format(self=self)


@cbor2.shareable_encoder
def default_encoder(encoder, obj):
    if not isinstance(obj, (Company, Employee)):
        raise Exception('cannot serialize type %s' % obj.__class__)

    serialized_state = encoder.encode_to_bytes(obj.__dict__)
    wrapped_state = [obj.__class__.__name__, serialized_state]
    with encoder.disable_value_sharing():
        encoder.encode(cbor2.CBORTag(CBOR_TAGNUM, wrapped_state))


def tag_decoder(decoder, tag, shareable_index=None):
    if tag.tag != CBOR_TAGNUM:
        return tag

    classname, serialized_state = tag.value
    cls = Company if classname == 'Company' else Employee

    # This is required for cyclic references to work
    obj = cls.__new__(cls)
    if shareable_index:
        decoder.set_shareable(shareable_index, obj)

    # Restore the object's state
    state = decoder.decode_from_bytes(serialized_state)
    obj.__dict__.update(state)
    return obj


class CBORCodec(object):
    """
    Our codec to encode/decode our custom binary payload. This is needed
    in "payload transparency mode" (a WAMP AP / Crossbar.io feature), so
    the app code is shielded, so you can write your code as usual in Autobahn/WAMP.
    """

    def encode(self, is_originating, uri, args=None, kwargs=None):
        # Value sharing is optional (but required in this example!).
        # It allows for more efficient serialization of repeated structures and makes it possible
        # to serialize cyclic structures (at the cost of some extra line overhead)
        payload = cbor2.dumps([args, kwargs], value_sharing=True, default=default_encoder)
        return EncodedPayload(payload, ENC_ALGO)

    def decode(self, is_originating, uri, encoded_payload):
        # Autobahn has received a custom payload.
        # convert it into a tuple: (uri, args, kwargs)
        if encoded_payload.enc_algo != ENC_ALGO:
            raise SerializationError(u'Unrecognized payload encoding algorithm: %s' % encoded_payload.enc_algo)

        args, kwargs = cbor2.loads(encoded_payload.payload, tag_hook=tag_decoder)
        return uri, args, kwargs

# we need to register our codec!
IPayloadCodec.register(CBORCodec)


class MySession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('session joined: {details}', details=details)

        # this is the one and only line of code that is different from a regular
        # WAMP app session: we set our codec, and everything else is transparent (!)
        self.set_payload_codec(CBORCodec())

        def on_event(company):
            self.log.info('received company event: {company}', company=company)

            # Check that the cyclic references have been restored
            for employee in company.employees:
                assert employee.company is company

        reg = yield self.subscribe(on_event, TOPIC)

        self.log.info('subscribed to topic {topic}: registration={reg}', topic=TOPIC, reg=reg)

        company = Company(u'Crossbar.io GmbH')
        company.add_employee(u'Tobias Oberstein', u'CEO')
        company.add_employee(u'Alexander Goedde', u'CFO')
        pub = yield self.publish(
            TOPIC, company,
            options=PublishOptions(acknowledge=True, exclude_me=False),
        )
        self.log.info('event published: publication={pub}', pub=pub)


if __name__ == '__main__':
    txaio.use_twisted()
    txaio.start_logging(level='info')
    msgpack = MsgPackSerializer()  # required to send binary on Python 2
    runner = ApplicationRunner(u'ws://localhost:8080/ws', u'realm1', serializers=[msgpack])
    runner.run(MySession)
