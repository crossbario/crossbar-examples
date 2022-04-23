#!/bin/sh

########################################################################################
##
## WAMP-CRA+Ticket static + file-store
##
rm -f ./cookie/.crossbar/cookies.dat
MYSECRET="secret123" crossbar start --cbdir=./cookie/.crossbar &
sleep 10

MYSECRET="secret123"     python ./cookie/client.py client1
wamp_cookie_file_good=$?

MYSECRET="wrongpassword" python ./cookie/client.py client1
wamp_cookie_file_bad=$?

crossbar stop --cbdir=./cookie/.crossbar || true

########################################################################################
##
## WAMP-CRA+Ticket static + database-store
##
rm -rf ./cookie/.crossbar/.cookies
MYSECRET="secret123" crossbar start --cbdir=./cookie/.crossbar --config=config-database.json &
sleep 10

MYSECRET="secret123"     python ./cookie/client.py client1
wamp_cookie_db_good=$?

MYSECRET="wrongpassword" python ./cookie/client.py client1
wamp_cookie_db_bad=$?

crossbar stop --cbdir=./cookie/.crossbar || true

########################################################################################
##
## WAMP-CRA+Ticket static + proxy-router + database-store
##
rm -rf ./cookie/.crossbar/.cookies
MYSECRET="secret123" crossbar start --cbdir=./cookie/.crossbar --config=config-rtrpxy-database.json &
sleep 15

MYSECRET="secret123"     python ./cookie/client.py client1
wamp_cookie_rtrpxy_db_good=$?

MYSECRET="wrongpassword" python ./cookie/client.py client1
wamp_cookie_rtrpxy_db_bad=$?

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

[ $wamp_cookie_file_good      -eq 0 ] && echo "wamp-cookie-file-good:                       OK" || echo "wamp-cookie-file-good:                       FAIL"
[ $wamp_cookie_file_bad       -eq 1 ] && echo "wamp-cookie-file-bad:                        OK" || echo "wamp-cookie-file-bad:                        FAIL"
[ $wamp_cookie_db_good        -eq 0 ] && echo "wamp-cookie-db-good:                         OK" || echo "wamp-cookie-db-good:                         FAIL"
[ $wamp_cookie_db_bad         -eq 1 ] && echo "wamp-cookie-db-bad:                          OK" || echo "wamp-cookie-db-bad:                          FAIL"
[ $wamp_cookie_rtrpxy_db_good -eq 0 ] && echo "wamp-cookie-rtrpxy-db-good:                  OK" || echo "wamp-cookie-rtrpxy-db-good:                  FAIL"
[ $wamp_cookie_rtrpxy_db_bad  -eq 1 ] && echo "wamp-cookie-rtrpxy-db-bad:                   OK" || echo "wamp-cookie-rtrpxy-db-bad:                   FAIL"
