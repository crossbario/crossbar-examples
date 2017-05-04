# Setting up serialization of custom types in Crossbar.io

Crossbar.io has a feature called "payload transparency" which allows you to send and receive
arbitrarily encoded payloads among all parties that understand how to decode them. This allows you
to use the full scope of features of any particular serializer, including hooks for (de)serializing
custom types.

This example demonstrates how to set up a *payload codec* using the [cbor2](https://pypi.org/project/cbor2/)
serializer to transparently serialize instances of the custom `Company` and `Employee` classes.
The two custom classes here are set up so that a Company contains a list of Employees, but an
Employee also contains a reference to its Company. This is called a *cyclic reference*, and most
serializers would raise an exception (or just outright crash the interpreter) trying to serialize
a loop like this. To make this work, the `value_sharing` option of the cbor2 serializer is turned
on here, and the hooks are written in a specific way to make this work.

It should be noted that since the payload output from the serializer is binary, you will need a
binary capable main serializer too. This excludes the JSON codec, at least on Python 2.

To test, start Crossbar.io in a first terminal (from this directory):

```console
crossbar start
```

Then, in a second terminal, start a test client connecting to Crossbar.io:

```console
(cpy351_1) oberstet@corei7ub1310:~/scm/crossbario/crossbarexamples/payloadcodec$ python cbor2_codec.py
2017-05-04T15:04:24+0300 session joined: SessionDetails(realm=<realm1>, session=7183809543185723, authid=<JYAT-793N-4G9P-LEU7-RKSG-S65R>, authrole=<anonymous>, authmethod=anonymous, authprovider=static, authextra=None, resumed=None, resumable=None, resume_token=None)
2017-05-04T15:04:24+0300 subscribed to topic test.mytopic1: registration=Subscription(id=8312284639856442, is_active=True)
2017-05-04T15:04:24+0300 event published: publication=Publication(id=494029740371525, was_encrypted=True)
2017-05-04T15:04:24+0300 received company event: Company(name=Crossbar.io GmbH, employees=[Employee(name=Tobias Oberstein, title=CEO), Employee(name=Alexander Goedde, title=CFO)])
```
