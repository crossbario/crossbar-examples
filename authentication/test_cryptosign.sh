#!/bin/sh

########################################################################################
##
## WAMP-Cryptosign static (using Twisted with authid)
##
crossbar start --cbdir=./cryptosign/static/.crossbar &
sleep 5

python ./cryptosign/static/client_tx.py --realm devices --authid client01@example.com --key ./cryptosign/static/.keys/client01.key
wamp_cryptosign_static_tx_good=$?

python ./cryptosign/static/client_tx.py --realm devices --authid client01@example.com --key ./cryptosign/static/.keys/client03.key
wamp_cryptosign_static_tx_bad=$?

crossbar stop  --cbdir=./cryptosign/static/.crossbar || true

########################################################################################
##
## WAMP-Cryptosign static (using Twisted and NO authid)
##
crossbar start --cbdir=./cryptosign/static/.crossbar &
sleep 5

python ./cryptosign/static/client_tx.py --realm devices --key ./cryptosign/static/.keys/client01.key
wamp_cryptosign_static_tx_noauthid_good=$?

python ./cryptosign/static/client_tx.py --realm devices --key ./cryptosign/static/.keys/client03.key
wamp_cryptosign_static_tx_noauthid_bad=$?

crossbar stop  --cbdir=./cryptosign/static/.crossbar || true

########################################################################################
##
## WAMP-Cryptosign static (using asyncio with authid)
##
crossbar start --cbdir=./cryptosign/static/.crossbar &
sleep 5

python ./cryptosign/static/client_aio.py --realm devices --authid client01@example.com --key ./cryptosign/static/.keys/client01.key
wamp_cryptosign_static_aio_good=$?

python ./cryptosign/static/client_aio.py --realm devices --authid client01@example.com --key ./cryptosign/static/.keys/client03.key
wamp_cryptosign_static_aio_bad=$?

crossbar stop  --cbdir=./cryptosign/static/.crossbar || true

########################################################################################
##
## WAMP-Cryptosign static (using asyncio and NO authid)
##
crossbar start --cbdir=./cryptosign/static/.crossbar &
sleep 5

python ./cryptosign/static/client_aio.py --realm devices --key ./cryptosign/static/.keys/client01.key
wamp_cryptosign_static_aio_noauthid_good=$?

python ./cryptosign/static/client_aio.py --realm devices --key ./cryptosign/static/.keys/client03.key
wamp_cryptosign_static_aio_noauthid_bad=$?

crossbar stop  --cbdir=./cryptosign/static/.crossbar || true


########################################################################################
##
## WAMP-Cryptosign with-TLS (using Twisted with no channel binding)
##
crossbar start --cbdir=./cryptosign/tls/.crossbar &
sleep 5

python ./cryptosign/tls/client_tx.py --url wss://localhost:8080 --key ./cryptosign/tls/.keys/client01.key
wamp_cryptosign_tls_tx_cnlbind_none_good=$?

python ./cryptosign/tls/client_tx.py --url wss://localhost:8080 --key ./cryptosign/tls/.keys/client03.key
wamp_cryptosign_tls_tx_cnlbind_none_bad=$?

crossbar stop  --cbdir=./cryptosign/tls/.crossbar || true

########################################################################################
##
## WAMP-Cryptosign with-TLS (using Twisted with channel binding "tls-unique")
##
crossbar start --cbdir=./cryptosign/tls/.crossbar &
sleep 5

python ./cryptosign/tls/client_tx.py --url wss://localhost:8080 --key ./cryptosign/tls/.keys/client01.key --channel_binding="tls-unique"
wamp_cryptosign_tls_tx_cnlbind_unique_good=$?

python ./cryptosign/tls/client_tx.py --url wss://localhost:8080 --key ./cryptosign/tls/.keys/client03.key --channel_binding="tls-unique"
wamp_cryptosign_tls_tx_cnlbind_unique_bad=$?

crossbar stop  --cbdir=./cryptosign/tls/.crossbar || true

# FIXME: ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain

# ########################################################################################
# ##
# ## WAMP-Cryptosign with-TLS (using asyncio with no channel binding)
# ##
# crossbar start --cbdir=./cryptosign/tls/.crossbar &
# sleep 5

# python ./cryptosign/tls/client_aio.py --url wss://localhost:8080 --key ./cryptosign/tls/.keys/client01.key
# wamp_cryptosign_tls_aio_cnlbind_none_good=$?

# python ./cryptosign/tls/client_aio.py --url wss://localhost:8080 --key ./cryptosign/tls/.keys/client03.key
# wamp_cryptosign_tls_aio_cnlbind_none_bad=$?

# crossbar stop  --cbdir=./cryptosign/tls/.crossbar || true

# ########################################################################################
# ##
# ## WAMP-Cryptosign with-TLS (using asyncio with channel binding "tls-unique")
# ##
# crossbar start --cbdir=./cryptosign/tls/.crossbar &
# sleep 5

# python ./cryptosign/tls/client_aio.py --url wss://localhost:8080 --key ./cryptosign/tls/.keys/client01.key --channel_binding="tls-unique"
# wamp_cryptosign_tls_aio_cnlbind_unique_good=$?

# python ./cryptosign/tls/client_aio.py --url wss://localhost:8080 --key ./cryptosign/tls/.keys/client03.key --channel_binding="tls-unique"
# wamp_cryptosign_tls_aio_cnlbind_unique_bad=$?

# crossbar stop  --cbdir=./cryptosign/tls/.crossbar || true


########################################################################################
##
## Test Summary
##

echo ""
echo "Test results:"
echo "============="
echo ""

exec >> test.log

[ $wamp_cryptosign_static_tx_good              -eq 0 ] && echo "wamp-cryptosign-static-tx-good:              OK" || echo "wamp-cryptosign-static-tx-good:               FAIL"
[ $wamp_cryptosign_static_tx_bad               -eq 1 ] && echo "wamp-cryptosign-static-tx-bad:               OK" || echo "wamp-cryptosign-static-tx-bad:                FAIL"
[ $wamp_cryptosign_static_tx_noauthid_good     -eq 0 ] && echo "wamp-cryptosign-static-tx-noauthid-good:     OK" || echo "wamp-cryptosign-static-tx-no-authid-good:     FAIL"
[ $wamp_cryptosign_static_tx_noauthid_bad      -eq 1 ] && echo "wamp-cryptosign-static-tx-noauthid-bad:      OK" || echo "wamp-cryptosign-static-tx-no-authid-bad:      FAIL"
[ $wamp_cryptosign_static_aio_good             -eq 0 ] && echo "wamp-cryptosign-static-aio-good:             OK" || echo "wamp-cryptosign-static-aio-good:              FAIL"
[ $wamp_cryptosign_static_aio_bad              -eq 1 ] && echo "wamp-cryptosign-static-aio-bad:              OK" || echo "wamp-cryptosign-static-aio-bad:               FAIL"
[ $wamp_cryptosign_static_aio_noauthid_good    -eq 0 ] && echo "wamp-cryptosign-static-aio-noauthid-good:    OK" || echo "wamp-cryptosign-static-aio-no-authid-good:    FAIL"
[ $wamp_cryptosign_static_aio_noauthid_bad     -eq 1 ] && echo "wamp-cryptosign-static-aio-noauthid-bad:     OK" || echo "wamp-cryptosign-static-aio-no-authid-bad:     FAIL"

[ $wamp_cryptosign_tls_tx_cnlbind_none_good    -eq 0 ] && echo "wamp-cryptosign-tls-tx-cnlbin-none-good:     OK" || echo "wamp-cryptosign-tls-tx-cnlbin-none-good:      FAIL"
[ $wamp_cryptosign_tls_tx_cnlbind_none_bad     -eq 1 ] && echo "wamp-cryptosign-tls-tx-cnlbin-none-bad:      OK" || echo "wamp-cryptosign-tls-tx-cnlbin-none-bad:       FAIL"
[ $wamp_cryptosign_tls_tx_cnlbind_unique_good  -eq 0 ] && echo "wamp-cryptosign-tls-tx-cnlbin-unique-good:   OK" || echo "wamp-cryptosign-tls-tx-cnlbin-unique-good:    FAIL"
[ $wamp_cryptosign_tls_tx_cnlbind_unique_bad   -eq 1 ] && echo "wamp-cryptosign-tls-tx-cnlbin-unique-bad:    OK" || echo "wamp-cryptosign-tls-tx-cnlbin-unique-bad:     FAIL"

# FIXME: ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain
# [ $wamp_cryptosign_tls_aio_cnlbind_none_good   -eq 0 ] && echo "wamp-cryptosign-tls-aio-cnlbin-none-good:      OK" || echo "wamp-cryptosign-tls-aio-cnlbin-none-good:      FAIL"
# [ $wamp_cryptosign_tls_aio_cnlbind_none_bad    -eq 1 ] && echo "wamp-cryptosign-tls-aio-cnlbin-none-bad:       OK" || echo "wamp-cryptosign-tls-aio-cnlbin-none-bad:       FAIL"
# [ $wamp_cryptosign_tls_aio_cnlbind_unique_good -eq 0 ] && echo "wamp-cryptosign-tls-aio-cnlbin-unique-good:    OK" || echo "wamp-cryptosign-tls-aio-cnlbin-unique-good:    FAIL"
# [ $wamp_cryptosign_tls_aio_cnlbind_unique_bad  -eq 1 ] && echo "wamp-cryptosign-tls-aio-cnlbin-unique-bad:     OK" || echo "wamp-cryptosign-tls-aio-cnlbin-unique-bad:     FAIL"