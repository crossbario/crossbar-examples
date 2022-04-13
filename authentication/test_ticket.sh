#!/bin/sh

########################################################################################
##
## WAMP-Ticket static
##
MYTICKET="secret123" crossbar start --cbdir=./ticket/static/.crossbar &
sleep 5

MYTICKET="secret123"     python ./ticket/static/client.py client1
wamp_ticket_static_good=$?

MYTICKET="wrongpassword" python ./ticket/static/client.py client1
wamp_ticket_static_bad=$?

crossbar stop  --cbdir=./ticket/static/.crossbar || true

########################################################################################
##
## WAMP-Ticket dynamic
##
MYTICKET="secret123" crossbar start --cbdir=./ticket/dynamic/.crossbar &
sleep 5

MYTICKET="secret123"     python ./ticket/dynamic/client.py client1
wamp_ticket_dynamic_good=$?

MYTICKET="wrongpassword" python ./ticket/dynamic/client.py client1
wamp_ticket_dynamic_bad=$?

crossbar stop  --cbdir=./ticket/dynamic/.crossbar || true

########################################################################################
##
## WAMP-Ticket function-based
##
MYTICKET="secret123" crossbar start --cbdir=./ticket/function/.crossbar &
sleep 5

MYTICKET="secret123"     python ./ticket/function/client.py client1
wamp_ticket_function_good=$?

MYTICKET="wrongpassword" python ./ticket/function/client.py client1
wamp_ticket_function_bad=$?

crossbar stop  --cbdir=./ticket/function/.crossbar || true


########################################################################################
##
## Test Summary
##

echo ""
echo "Test results:"
echo "============="
echo ""

[ $wamp_ticket_static_good                        -eq 0 ] && echo "wamp-ticket-static-good:                        OK" || echo "wamp-ticket-static-good:                         FAIL"
[ $wamp_ticket_static_bad                         -eq 1 ] && echo "wamp-ticket-static-bad:                         OK" || echo "wamp-ticket-static-bad:                          FAIL"
[ $wamp_ticket_dynamic_good                       -eq 0 ] && echo "wamp-ticket-dynamic-good:                       OK" || echo "wamp-ticket-dynamic-good:                        FAIL"
[ $wamp_ticket_dynamic_bad                        -eq 1 ] && echo "wamp-ticket-dynamic-bad:                        OK" || echo "wamp-ticket-dynamic-bad:                         FAIL"
[ $wamp_ticket_function_good                      -eq 0 ] && echo "wamp-ticket-function-good:                      OK" || echo "wamp-ticket-function-good:                       FAIL"
[ $wamp_ticket_function_bad                       -eq 1 ] && echo "wamp-ticket-function-bad:                       OK" || echo "wamp-ticket-function-bad:                        FAIL"
