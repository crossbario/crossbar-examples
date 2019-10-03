# XBR Teststack

## Setup the stack

Stop the stack and scratch all data:

```
make stop
make clean
```

Start a blockchain:

```
make run_blockchain
```

Now deploy the XBR smart contracts to the blockchain.


Initialize some data in the blockchain:

```
make init_blockchain
```

Start the master, wait a couple of seconds and the initialize master configuration:

```
make run_master
make init_master
```

Start an edge node and watch log output

```
make run_edge1
make logs_edge1
```

You should ultimately see a line like the following in the log:

```
2019-10-02T16:25:12+0000 [XBRMrktMkr     19] _process_Network_ChannelCreated processing block 97 / txn 0x35894d8f888439d99105075ebca65195f583bfc1be814366b921163f34dfccec with args AttributeDict({'marketId': b'\xa1\xb8\xd6t\x1a\xe8I \x17\xfa\xfd\x8dO\x8bg\xa2', 'sender': '0x3E5e9111Ae8eB78Fe1CC3bb8915d5D461F3Ef9A9', 'delegate': '0x64E078A8Aa15A41B85890265648e965De686bAE6', 'recipient': '0x855FA758c77D68a04990E992aA4dcdeF899F654A', 'channel': '0xE5E0804039b59173996Edcc97c8FA4c46dfDa755', 'channelType': 2})
2019-10-02T16:25:12+0000 [XBRMrktMkr     19] _process_Network_ChannelCreated running:
2019-10-02T16:25:12+0000 [XBRMrktMkr     19] <Channel>(channel=0xe5e0804039b59173996edcc97c8fa4c46dfda755) already stored (type=2)
2019-10-02T16:25:12+0000 [XBRMrktMkr     19] Processed blockchain block 97: processed 9 XBR events
```

## Run a seller

To run a seller:

```
make run_seller1
```

The seller should start reporting its current active channel ("Delegate has currently active paying channel address 0x157.."):

```
seller1_1     | 2019-10-02T16:25:38+0000 connecting once using transport type "websocket" over endpoint "tcp"
seller1_1     | 2019-10-02T16:25:38+0000 Starting factory <autobahn.twisted.websocket.WampWebSocketClientFactory object at 0x0000000007f1f830>
seller1_1     | 2019-10-02T16:25:38+0000 Seller session joined
seller1_1     | 2019-10-02T16:25:38+0000 SessionDetails(realm=<realm1>,
seller1_1     | 2019-10-02T16:25:38+0000                session=7044206154901848,
seller1_1     | 2019-10-02T16:25:38+0000                authid=<A6X7-R566-LUAF-SMHM-7NR4-JTC5>,
seller1_1     | 2019-10-02T16:25:38+0000                authrole=<anonymous>,
seller1_1     | 2019-10-02T16:25:38+0000                authmethod=anonymous,
seller1_1     | 2019-10-02T16:25:38+0000                authprovider=static,
seller1_1     | 2019-10-02T16:25:38+0000                authextra={'x_cb_node_id': None, 'x_cb_peer': 'tcp4:172.21.0.6:41918', 'x_cb_pid': 12},
seller1_1     | 2019-10-02T16:25:38+0000                serializer=<cbor>,
seller1_1     | 2019-10-02T16:25:38+0000                resumed=None,
seller1_1     | 2019-10-02T16:25:38+0000                resumable=None,
seller1_1     | 2019-10-02T16:25:38+0000                resume_token=None)
seller1_1     | 2019-10-02T16:25:38+0000 Using market maker adr: b'>^\x91\x11\xae\x8e\xb7\x8f\xe1\xcc;\xb8\x91]]F\x1f>\xf9\xa9'
seller1_1     | 2019-10-02T16:25:38+0000 Created new key series <autobahn.twisted.xbr.KeySeries object at 0x0000000007f57e50>
seller1_1     | 2019-10-02T16:25:38+0000 Start selling from seller delegate address None (public key 0x925b36d9c2b031d0f6c2..)
seller1_1     | 2019-10-02T16:25:38+0000 Starting key rotation every 10 seconds for api_id="627f1b5c-58c2-43b1-8422-a34f7d3f5a04" ..
seller1_1     | 2019-10-02T16:25:38+0000 XBR ROTATE key "5bfb8216-c79a-8a0b-abc0-f9b8bde5fe74" rotated [api_id="627f1b5c-58c2-43b1-8422-a34f7d3f5a04"]
seller1_1     | 2019-10-02T16:25:38+0000 XBR OFFER  key "5bfb8216-c79a-8a0b-abc0-f9b8bde5fe74" offered for 35 XBR [api_id=627f1b5c-58c2-43b1-8422-a34f7d3f5a04, prefix="io.crossbar.example", delegate="d03ea8624c8c5987235048901fb614fdca89b117"]
seller1_1     | 2019-10-02T16:25:38+0000 Delegate has currently active paying channel address 0x157e0c3c638908724ede057f9d35837c4e8e595e
seller1_1     | 2019-10-02T16:25:38+0000 Remaining balance: 1000 XBR
seller1_1     | 2019-10-02T16:25:38+0000 Published event 527986028227277: {'data': 'py-seller', 'counter': 1}
seller1_1     | 2019-10-02T16:25:38+0000 SimpleSeller.sell() - XBR SELL   key "5bfb8216-c79a-8a0b-abc0-f9b8bde5fe74" sold for 35 XBR - balance is 965 XBR [caller=2460010567399088, caller_authid="MFXW-GPHX-W7CJ-HAEN-NNK4-99HT", buyer_pubkey="1671b508b23b017c5be6c14f6c079971598e7141147180d581da230db0069249"]
seller1_1     | 2019-10-02T16:25:39+0000 Published event 8171091349830335: {'data': 'py-seller', 'counter': 2}
seller1_1     | 2019-10-02T16:25:40+0000 Published event 4090354682485433: {'data': 'py-seller', 'counter': 3}
seller1_1     | 2019-10-02T16:25:41+0000 Published event 8661809597638821: {'data': 'py-seller', 'counter': 4}

...

seller1_1     | 2019-10-02T16:19:48+0000 Published event 7179135521535007: {'data': 'py-seller', 'counter': 292}
seller1_1     | 2019-10-02T16:19:49+0000 Published event 7792300949915635: {'data': 'py-seller', 'counter': 293}
seller1_1     | 2019-10-02T16:19:49+0000 SimpleSeller.close_channel() - XBR CLOSE   closing channel d2d98a3c14926e641b4490a0e04e260fd8b48e95, closing balance 20 XBR, closing sequence 29 [caller=1441236914224879, caller_authid="J9EN-FXUG-4Q4S-5QPJ-AWP3-QCUS"]
seller1_1     | 2019-10-02T16:19:49+0000 Session.onUserError(): "xbr.error.unexpected_channel_adr: SimpleSeller.sell() - unexpected paying channel address: expected 0xd2d98a3c14926e641b4490a0e04e260fd8b48e95, but got 0x9da91ec19889622e49ca0d0ef0c801f54354e826"
seller1_1     | 2019-10-02T16:19:49+0000 session leaving 'wamp.close.normal'
seller1_1     | 2019-10-02T16:19:49+0000 Seller session left CloseDetails(reason=<wamp.close.normal>, message='None')
seller1_1     | 2019-10-02T16:19:49+0000 Stopping factory <autobahn.twisted.websocket.WampWebSocketClientFactory object at 0x000000000676fe50>
seller1_1     | 2019-10-02T16:19:49+0000 Main loop terminated.

```

### Run a buyer

To run a buyer:

```
make run_buyer1
```

The buyer should start reporting its current active channel ("Delegate has current payment channel address 0x332... (remaining balance 500... at sequence 1)"):

```
buyer1_1      | 2019-10-02T16:28:03+0000 connecting once using transport type "websocket" over endpoint "tcp"
buyer1_1      | 2019-10-02T16:28:03+0000 Starting factory <autobahn.twisted.websocket.WampWebSocketClientFactory object at 0x00000000060ca4b8>
buyer1_1      | 2019-10-02T16:28:03+0000 Buyer session joined
buyer1_1      | 2019-10-02T16:28:03+0000 SessionDetails(realm=<realm1>,
buyer1_1      | 2019-10-02T16:28:03+0000                session=7151701763728529,
buyer1_1      | 2019-10-02T16:28:03+0000                authid=<AWMS-RL4J-7ATV-WU5V-NWJP-UAVE>,
buyer1_1      | 2019-10-02T16:28:03+0000                authrole=<anonymous>,
buyer1_1      | 2019-10-02T16:28:03+0000                authmethod=anonymous,
buyer1_1      | 2019-10-02T16:28:03+0000                authprovider=static,
buyer1_1      | 2019-10-02T16:28:03+0000                authextra={'x_cb_node_id': None, 'x_cb_peer': 'tcp4:172.21.0.5:59272', 'x_cb_pid': 12},
buyer1_1      | 2019-10-02T16:28:03+0000                serializer=<cbor>,
buyer1_1      | 2019-10-02T16:28:03+0000                resumed=None,
buyer1_1      | 2019-10-02T16:28:03+0000                resumable=None,
buyer1_1      | 2019-10-02T16:28:03+0000                resume_token=None)
buyer1_1      | 2019-10-02T16:28:03+0000 Using market maker adr: 0x3e5e9111ae8eb78fe1cc3bb8915d5d461f3ef9a9
buyer1_1      | 2019-10-02T16:28:03+0000 Start buying from consumer delegate address None (public key 0xc41cbfc96c0784c87fc6..)
buyer1_1      | 2019-10-02T16:28:03+0000 Delegate has current payment channel address 0x332280007303d5942dd60a945169b2b303320686 (remaining balance 500000000000000000000 at sequence 1)
buyer1_1      | 2019-10-02T16:28:03+0000 Remaining balance: 500 XBR
buyer1_1      | 2019-10-02T16:28:03+0000 Received encrypted event 5824722202809910 ..
buyer1_1      | 2019-10-02T16:28:03+0000 Key 51aee504-57f8-9d85-d292-ce4c914f6cd8 not yet in key store - buying key ..
buyer1_1      | 2019-10-02T16:28:03+0000 Key 51aee504-57f8-9d85-d292-ce4c914f6cd8 has current price quote 35
buyer1_1      | 2019-10-02T16:28:04+0000 SimpleBuyer.unwrap() - XBR BUY    key 51aee504-57f8-9d85-d292-ce4c914f6cd8 bought for 35 XBR [payment_channel=332280007303d5942dd60a945169b2b303320686, remaining=465, inflight=0, buyer_pubkey=dbc1bb7488a9a9ca1d2709dc240885eac4ef021e44e40d50fdf82b6e1f99617d, transactions={'complete': 1, 'pending': 0}]
buyer1_1      | 2019-10-02T16:28:04+0000 Decrypted event 5824722202809910 payload: {'data': 'py-seller', 'counter': 145}
buyer1_1      | 2019-10-02T16:28:04+0000 Received encrypted event 3233369522137220 ..
buyer1_1      | 2019-10-02T16:28:04+0000 Key 51aee504-57f8-9d85-d292-ce4c914f6cd8 already in key store (or currently being bought).
buyer1_1      | 2019-10-02T16:28:04+0000 Decrypted event 3233369522137220 payload: {'data': 'py-seller', 'counter': 146}
buyer1_1      | 2019-10-02T16:28:05+0000 Received encrypted event 7091132170734107 ..
buyer1_1      | 2019-10-02T16:28:05+0000 Key 51aee504-57f8-9d85-d292-ce4c914f6cd8 already in key store (or currently being bought).
buyer1_1      | 2019-10-02T16:28:05+0000 Decrypted event 7091132170734107 payload: {'data': 'py-seller', 'counter': 147}
buyer1_1      | 2019-10-02T16:28:06+0000 Received encrypted event 590950999348081 ..
buyer1_1      | 2019-10-02T16:28:07+0000 Key 51aee504-57f8-9d85-d292-ce4c914f6cd8 already in key store (or currently being bought).
buyer1_1      | 2019-10-02T16:28:07+0000 Decrypted event 590950999348081 payload: {'data': 'py-seller', 'counter': 148}
buyer1_1      | 2019-10-02T16:28:08+0000 Received encrypted event 2897336584577186 ..
buyer1_1      | 2019-10-02T16:28:08+0000 Key 51aee504-57f8-9d85-d292-ce4c914f6cd8 already in key store (or currently being bought).
buyer1_1      | 2019-10-02T16:28:08+0000 Decrypted event 2897336584577186 payload: {'data': 'py-seller', 'counter': 149}
buyer1_1      | 2019-10-02T16:28:09+0000 Received encrypted event 1692138999384653 ..
buyer1_1      | 2019-10-02T16:28:09+0000 Key 1757c66a-0f68-ff3f-8321-27ac60e71c97 not yet in key store - buying key ..
buyer1_1      | 2019-10-02T16:28:09+0000 Key 1757c66a-0f68-ff3f-8321-27ac60e71c97 has current price quote 35
buyer1_1      | 2019-10-02T16:28:09+0000 SimpleBuyer.unwrap() - XBR BUY    key 1757c66a-0f68-ff3f-8321-27ac60e71c97 bought for 35 XBR [payment_channel=332280007303d5942dd60a945169b2b303320686, remaining=430, inflight=0, buyer_pubkey=dbc1bb7488a9a9ca1d2709dc240885eac4ef021e44e40d50fdf82b6e1f99617d, transactions={'complete': 2, 'pending': 0}]
buyer1_1      | 2019-10-02T16:28:09+0000 Decrypted event 1692138999384653 payload: {'data': 'py-seller', 'counter': 150}
buyer1_1      | 2019-10-02T16:28:10+0000 Received encrypted event 82507613257254 ..
buyer1_1      | 2019-10-02T16:28:10+0000 Key 1757c66a-0f68-ff3f-8321-27ac60e71c97 already in key store (or currently being bought).
buyer1_1      | 2019-10-02T16:28:10+0000 Decrypted event 82507613257254 payload: {'data': 'py-seller', 'counter': 151}
buyer1_1      | 2019-10-02T16:28:11+0000 Received encrypted event 162132504528531 ..
buyer1_1      | 2019-10-02T16:28:11+0000 Key 1757c66a-0f68-ff3f-8321-27ac60e71c97 already in key store (or currently being bought).
buyer1_1      | 2019-10-02T16:28:11+0000 Decrypted event 162132504528531 payload: {'data': 'py-seller', 'counter': 152}
buyer1_1      | 2019-10-02T16:28:12+0000 Received encrypted event 4331986255451925 ..

...

buyer1_1      | 2019-10-02T16:17:23+0000 Received encrypted event 8179134960162043 ..
buyer1_1      | 2019-10-02T16:17:23+0000 Key 4e82a1e8-102f-0a37-6991-89eaa48084ce already in key store (or currently being bought).
buyer1_1      | 2019-10-02T16:17:23+0000 Decrypted event 8179134960162043 payload: {'data': 'py-seller', 'counter': 149}
buyer1_1      | 2019-10-02T16:17:24+0000 Received encrypted event 8355955307392820 ..
buyer1_1      | 2019-10-02T16:17:24+0000 Key 069fc0c2-34b4-5f11-eb70-e90afbabb628 not yet in key store - buying key ..
buyer1_1      | 2019-10-02T16:17:24+0000 Key 069fc0c2-34b4-5f11-eb70-e90afbabb628 has current price quote 35
buyer1_1      | 2019-10-02T16:17:24+0000 auto-closing payment channel 05678a3797bf8dc4de0c6b0fd13c3c455629e02f [close_seq=15, close_balance=10, close_is_final=True]
buyer1_1      | 2019-10-02T16:17:24+0000 ApplicationError(error=<xbr.error.channel_closed>, args=['SimpleBuyer.unwrap() - key 069fc0c2-34b4-5f11-eb70-e90afbabb628 cannot be bought: payment channel 0x05678a3797bf8dc4de0c6b0fd13c3c455629e02f ran empty and we initiated close at remaining balance of 10'], kwargs={}, enc_algo=None, callee=None, callee_authid=None, callee_authrole=None, forward_for=None)
buyer1_1      | 2019-10-02T16:17:24+0000 session leaving 'wamp.close.normal'
buyer1_1      | 2019-10-02T16:17:24+0000 Stopping factory <autobahn.twisted.websocket.WampWebSocketClientFactory object at 0x0000000006c1a5d0>
buyer1_1      | 2019-10-02T16:17:24+0000 Main loop terminated.
```

## Workbench

```python
import zlmdb
import cfxdb

db = zlmdb.Database('xbrdb-transactions', maxsize=2**30, readonly=False)
xbr = cfxdb.xbr.Schema.attach(db)


with db.begin() as txn:
    cnt = xbr.offers.count(txn)
    print('{} data encryption key offers so far so far'.format(cnt))
```
