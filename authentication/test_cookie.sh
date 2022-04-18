#!/bin/sh

########################################################################################
##
## WAMP-CRA+Ticket static
##
MYSECRET="secret123" crossbar start --cbdir=./cookie/.crossbar &
sleep 10

MYSECRET="secret123"     python ./cookie/client.py client1
wamp_cra_cookie_good=$?

MYSECRET="wrongpassword" python ./cookie/client.py client1
wamp_cra_cookie_bad=$?

crossbar stop --cbdir=./cookie/.crossbar || true

########################################################################################
##
## Test Summary
##

echo ""
echo "Test results:"
echo "============="
echo ""

exec >> test.log

[ $wamp_cra_cookie_good   -eq 0 ] && echo "wamp-cra-cookie-good:                        OK" || echo "wamp-cra-cookie-good:                         FAIL"
[ $wamp_cra_cookie_bad    -eq 1 ] && echo "wamp-cra-cookie-bad:                         OK" || echo "wamp-cra-cookie-bad:                          FAIL"
