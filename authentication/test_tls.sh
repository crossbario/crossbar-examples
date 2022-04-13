#!/bin/sh

########################################################################################
##
## WAMP-TLS(-client-authentication) static
##
crossbar start --cbdir=./tls/static/.crossbar &
sleep 5

python ./tls/static/client_tx.py --url wss://localhost:8080/ws --key client0.key --cert client0.crt --channel_binding="tls-unique"
wamp_tls_tx_cnlbind_unique_good=$?

python ./tls/static/client_tx.py --url wss://localhost:8080/ws --key client1.key --cert client1.crt --channel_binding="tls-unique"
wamp_tls_tx_cnlbind_unique_bad=$?

crossbar stop  --cbdir=./cryptosign/tls/.crossbar || true


########################################################################################
##
## Test Summary
##

echo ""
echo "Test results:"
echo "============="
echo ""

[ $wamp_tls_tx_cnlbind_unique_good   -eq 0 ] && echo "wamp-tls-static-cnlbind-unique-good:                        OK" || echo "wamp-tls-static-cnlbind-unique-good:                         FAIL"
[ $wamp_tls_tx_cnlbind_unique_bad    -eq 1 ] && echo "wamp-tls-static-cnlbind-unique-bad:                         OK" || echo "wamp-tls-static-cnlbind-unique-bad:                          FAIL"
