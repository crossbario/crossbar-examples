#!/bin/sh

########################################################################################
##
## WAMP-CRA static
##
MYSECRET="secret123" crossbar start --cbdir=./wampcra/static/.crossbar &
sleep 5

MYSECRET="secret123"     python ./wampcra/static/client.py client1
wamp_cra_static_good=$?

MYSECRET="wrongpassword" python ./wampcra/static/client.py client1
wamp_cra_static_bad=$?

crossbar stop  --cbdir=./wampcra/static/.crossbar || true

########################################################################################
##
## WAMP-CRA dynamic
##
MYSECRET="secret123" crossbar start --cbdir=./wampcra/dynamic/python/.crossbar &
sleep 5

MYSECRET="secret123"     python ./wampcra/dynamic/python/client.py client1
wamp_cra_dynamic_good=$?

MYSECRET="wrongpassword" python ./wampcra/dynamic/python/client.py client1
wamp_cra_dynamic_bad=$?

crossbar stop  --cbdir=./wampcra/dynamic/python/.crossbar || true


# crossbar stop  --cbdir=./tls/static/.crossbar || true
# crossbar start --cbdir=./tls/static/.crossbar --config=config.json &
# sleep 5
# crossbar stop  --cbdir=./tls/static/.crossbar || true


########################################################################################
##
## Test Summary
##
echo ""
echo "Test results:"
echo "============="
echo ""
[ $wamp_cra_static_good  -eq 0 ] && echo "wamp-cra-static-good:      OK" || echo "wamp-cra-static-good:      FAIL"
[ $wamp_cra_static_bad   -eq 1 ] && echo "wamp-cra-static-bad:       OK" || echo "wamp-cra-static-bad:       FAIL"
[ $wamp_cra_dynamic_good -eq 0 ] && echo "wamp-cra-dynamic-good:     OK" || echo "wamp-cra-dynamic-good:     FAIL"
[ $wamp_cra_dynamic_bad  -eq 1 ] && echo "wamp-cra-dynamic-bad:      OK" || echo "wamp-cra-dynamic-bad:      FAIL"
