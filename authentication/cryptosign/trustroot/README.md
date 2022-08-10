# WAMP-cryptosign with certificates and trustroot

## Test Accounts Setup

All key pairs, both WAMP-Cryptosign and Ethereum, for this demo are generated from one seedphrase defined in the [Makefile](Makefile)

```python
seedphrase = "avocado style uncover thrive same grace crunch want essay reduce current edge"
```

From this seedphrase, an in-memory security module with multiple Ethereum and WAMP-Cryptosign keys can be created:

```python
sm: SecurityModuleMemory = SecurityModuleMemory.from_seedphrase(seedphrase, num_eth_keys=10, num_cs_keys=6)
await sm.open()
```

The 16 keys (asymmetric key pairs of private and public keys) generated in the security module for this demo are 10 Ethereum keys and 6 Cryptosign keys:

| Key No.     | Key Type    | Variable            | Usage                     | Authority
|-------------|-------------|---------------------|---------------------------|------------------
| 0           | Ethereum    | -                   | *unused*                  | -
| 1           | Ethereum    | `root_ca1_ekey`     | Root CA Owner             | **User 1**
| 2           | Ethereum    | `relay_ca1_ekey`    | Relay CA Owner            | User 2
| 3           | Ethereum    | `relay_ca2_ekey`    | Relay CA Owner            | User 3
| 4           | Ethereum    | `gateway_ca1_ekey`  | Gateway CA Owner          | User 4
| 5           | Ethereum    | `gateway_ca2_ekey`  | Gateway CA Owner          | User 5
| 6           | Ethereum    | `relay_ep1_ekey`    | Relay Endpoint            | User 2
| 7           | Ethereum    | `relay_ep2_ekey`    | Relay Endpoint            | User 3
| 8           | Ethereum    | `gateway_ep1_ekey`  | Gateway Endpoint          | User 4
| 9           | Ethereum    | `gateway_ep2_ekey`  | Gateway Endpoint          | User 5
| 10          | Cryptosign  | `relay_ep1_ckey`    | Relay Node                | User 2
| 11          | Cryptosign  | `relay_ep2_ckey`    | Relay Node                | User 3
| 12          | Cryptosign  | `gateway_ep1_ckey`  | Gateway Node              | User 4
| 13          | Cryptosign  | `gateway_ep2_ckey`  | Gateway Node              | User 5
| 14          | Cryptosign  | -                   | *unused*                  | -
| 15          | Cryptosign  | -                   | *unused*                  | -

The keys can be accessed from the security module using the *Key No.*:

```python
# Ethereum key pair used to sign the root CA certificate with
root_ca1_ekey: EthereumKey = sm[1]
```

and used to sign certificates

```python
# create and sign root CA certificate
certificate = EIP712AuthorityCertificate(...)
signature = await cert.sign(root_ca1_ekey, binary=True)
```

## Root CA Certificate

To create a new self-signed *Root CA Certificate* you can use the included script [gen_ca_cert.py](gen_ca_cert.py)

```console
python gen_ca_cert.py --debug \
    --seedphrase=$(SEEDPHRASE) \
    --verifyingContract=0x163D58cE482560B7826b4612f40aa2A7d53310C4 \
    --realm=0x72b3486d38E9f49215b487CeAaDF27D6acf22115 \
    --keyno=0 \
    --certfile=./.crossbar/root_ca_cert_realm1.crt \
```

This will use the provided BIP-39 seedphrase ("Mnemonic") to generate security module keys from (both Ethereum and Cryptosign).
The index within these auto-generated (Ethereum) key which we will use is specified using `--keyno=0`.
The certificate will have an `issuer` with address matching this key, and since we generate a Root CA certificate, the
certificate will be self-signed, and hence `subject` will match that same address.


## Standalone Trustroots

A complete Crossbar.io node configuration using *Standalone Trustroots* can be found [here](.crossbar/config-standalone-trustroot.json).

This example configures two realms

* `realm1`
* `realm2`

and a WebSocket listening transport with an authentication item `auth` for *WAMP-Cryptosign*

```json
{
    "cryptosign": {
        "type": "static",
        "trustroots": {
            "realm1": {
                "certificate": "root_ca_cert_realm1.crt"
            },
            "realm2": {
                "certificate": "root_ca_cert_realm2.crt"
            }
        }
    }
}
```

The `trustroots` item for `cryptosign` configures a map from realm names (here `realm1` and `realm2`) to files with WAMP EIP712  *Root CA Certificates*

* `root_ca_cert_realm1.crt`
* `root_ca_cert_realm2.crt`

These certificate filenames are relative to the Crossbar.io node directory (`.crossbar`), and are binary files which contain the CBOR serialized certificate and signature `[certificate, signature]`.


## Shared Trustroots

Write me.
