`ipfs-upload-client` is a minimal CLI tool to upload files or directories to Infura's IPFS or another API endpoint.

## Example

`ipfs-upload-client --id xxxxx --secret yyyyy /path/to/data`

## Options
```
  --id string       your Infura ProjectID
  --pin             whether or not to pin the data (default true)
  --secret string   your Infura ProjectSecret
  --url string      the API URL (default "https://ipfs.infura.io:5001")
```