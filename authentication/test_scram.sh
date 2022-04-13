#!/bin/bash -

########################################################################################
##
## WAMP-SCRAM static
##
crossbar start --cbdir=./scram/static/.crossbar &
sleep 5

python ./scram/static/client_tx.py --realm realm1 --authid foobar@example.com --password secret123
wamp_scram_tx_good=$?

python ./scram/static/client_tx.py --realm realm1 --authid foobar@example.com --password wrongpassword
wamp_scram_tx_bad=$?

crossbar stop  --cbdir=./scram/static/.crossbar || true


########################################################################################
##
## Test Summary
##

echo ""
echo "Test results:"
echo "============="
echo ""

exec >> test.log

[ $wamp_scram_tx_good   -eq 0 ] && echo "wamp-scram-tx-good:                          OK" || echo "wamp-scram-tx-good:                          FAIL"
[ $wamp_scram_tx_bad    -eq 1 ] && echo "wamp-scram-tx-bad:                           OK" || echo "wamp-scram-tx-bad:                           FAIL"
