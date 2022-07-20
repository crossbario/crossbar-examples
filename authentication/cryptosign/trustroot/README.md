# WAMP-cryptosign with certificates and trustroot

*Last tested: 2022/07/20 using Crossbar.io 22.7.1.dev1*

See [here](https://github.com/wamp-proto/wamp-proto/pull/413).

## Configuration

To configure the use of trustroots, add a configuration item for `cryptosign` authentication specifying a map `trustroots` with accepted Ethereum (checksummed) addresses mapping to the principals (realm, authrole and optional authextra) for authentication:

```
"auth": {
    "cryptosign": {
        "type": "static",
        "trustroots": {
            "0xf766Dc789CF04CD18aE75af2c5fAf2DA6650Ff57": {
                "realm": "realm1",
                "role": "user"
            }
        }
    }
}
```

If the client presents an EIP712 certificate chain starting with a delegate certificate for the client's own key, and ending with a self-signed root CA certificate for address `0xf766Dc789CF04CD18aE75af2c5fAf2DA6650Ff57`, grant access to the client on realm `"realm1"` with authrole `"user"`, and with the client's delegate address as authid .

## How to test

In a first terminal, start a [Crossbar.io node](.crossbar/config.json) with a TLS transport listening
on port 8080, and using a [self-signed certificate](.crossbar/client.crt):

```console
make crossbar
```

In a second terminal, start the clients

```console
make client_tx_cnlbind_unique
```

You should see the following message in the client logs:

```
...
********************************************************************************
2022-07-20T22:53:36+0200 OK, successfully authenticated with WAMP-cryptosign:

    realm="realm1"
    authrole="user"
    authid="0xf5173a6111B2A6B3C20fceD53B2A8405EC142bF6"

2022-07-20T22:53:36+0200 ********************************************************************************
...
```
