#!/bin/sh

########################################################################################
##
## WAMP-CRA+Ticket static + file-store
##
rm -f ./cookie/.crossbar/cookies.dat
MYSECRET="secret123" crossbar start --cbdir=./cookie/.crossbar &
sleep 10

MYSECRET="secret123"     python ./cookie/client.py client1
wamp_cra_cookie_static_file_good=$?

MYSECRET="wrongpassword" python ./cookie/client.py client1
wamp_cra_cookie_static_file_bad=$?

crossbar stop --cbdir=./cookie/.crossbar || true

########################################################################################
##
## WAMP-CRA+Ticket static + database-store
##
rm -rf ./cookie/.crossbar/.cookies
MYSECRET="secret123" crossbar start --cbdir=./cookie/.crossbar --config=config-database.json &
sleep 10

MYSECRET="secret123"     python ./cookie/client.py client1
wamp_cra_cookie_static_db_good=$?

MYSECRET="wrongpassword" python ./cookie/client.py client1
wamp_cra_cookie_static_db_bad=$?

crossbar stop --cbdir=./cookie/.crossbar || true

########################################################################################
##
## WAMP-CRA+Ticket static + proxy-router + database-store
##
rm -rf ./cookie/.crossbar/.cookies
MYSECRET="secret123" crossbar start --cbdir=./cookie/.crossbar --config=config-rtrpxy-database.json &
sleep 15

MYSECRET="secret123"     python ./cookie/client.py client1
wamp_cra_cookie_rtrpxy_static_db_good=$?

MYSECRET="wrongpassword" python ./cookie/client.py client1
wamp_cra_cookie_rtrpxy_static_db_bad=$?

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

[ $wamp_cra_cookie_static_file_good      -eq 0 ] && echo "wamp-cra-cookie-static-file-good:            OK" || echo "wamp-cra-cookie-static-file-good:            FAIL"
[ $wamp_cra_cookie_static_file_bad       -eq 1 ] && echo "wamp-cra-cookie-static-file-bad:             OK" || echo "wamp-cra-cookie-static-file-bad:             FAIL"
[ $wamp_cra_cookie_static_db_good        -eq 0 ] && echo "wamp-cra-cookie-static-db-good:              OK" || echo "wamp-cra-cookie-static-db-good:              FAIL"
[ $wamp_cra_cookie_static_db_bad         -eq 1 ] && echo "wamp-cra-cookie-static-db-bad:               OK" || echo "wamp-cra-cookie-static-db-bad:               FAIL"
[ $wamp_cra_cookie_rtrpxy_static_db_good -eq 0 ] && echo "wamp-cra-cookie-rtrpxy-static-db-good:       OK" || echo "wamp-cra-cookie-rtrpxy-static-db-good:       FAIL"
[ $wamp_cra_cookie_rtrpxy_static_db_bad  -eq 1 ] && echo "wamp-cra-cookie-rtrpxy-static-db-bad:        OK" || echo "wamp-cra-cookie-rtrpxy-static-db-bad:        FAIL"
