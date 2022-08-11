import os
from pprint import pprint
from autobahn.xbr import EIP712AuthorityCertificate
import web3

for fn in ['relay_ep1.crt', 'relay_ca1.crt', 'root_ca1.crt']:
    cert = EIP712AuthorityCertificate.load(os.path.join('.crossbar', fn))
    print('load certificate by issuer {} with {} signatures'.format(web3.Web3.toChecksumAddress(cert.issuer), len(cert.signatures) if cert.signatures else 'no'))
    pprint(cert.marshal())
