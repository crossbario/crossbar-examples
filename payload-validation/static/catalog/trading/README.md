# PyDeFi Trading API Catalog

The **PyDeFi Trading API Catalog** contains WAMP API definitions for use in cryptocurrency
trading applications.

## Build

To build the API catalog, run

```
make clean build
```

This will produce a catalog archive file `./build/pydefi-trading.zip`.

## Publish

Use your Infura IPFS project credentials

```
export INFURA_IPFS_PROJECT_ID=28qKY...
export INFURA_IPFS_PROJECT_SECRET=5cc4...
export INFURA_IPFS_ENDPOINT=https://ipfs.infura.io:5001
```

Use the [Infura IPFS Client tool](https://blog.infura.io/post/ipfs-file-upload-client-tool)

```
make setup_ipfs_client_tool
```

Then publish to IPFS:

```
make publish
```

You should see the IPFS CID of the uploaded file:

```
/ipfs/QmdaWNrsnsQcYxLxMP6bjP2wj5Mjtd7aez8RnnJWZ4uzyJ
```

And you should see the file in the [Infura IPFS explorer](https://infura.io/dashboard/explorer).

## Usage

To use the API catalog, run Crossbar.io and add a `inventory` configuration item in
your node configuration:

```json
{
    "version": 2,
    "workers": [
        {
            "type": "router",
            "realms": [
                {
                    "name": "realm1",
                    "inventory": {
                        "type": "wamp.eth",
                        "catalogs": [
                            {
                                "name": "pydefi-trading",
                                "filename": "./build/pydefi-trading.zip"
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
```
