#!/bin/bash

#
# following along from https://jamielinux.com/docs/openssl-certificate-authority/
# which is a great guide to creating your own CA, etc etc
#

mkdir -p ./ca
mkdir -p ./ca/certs
mkdir -p ./ca/newcerts
mkdir -p ./ca/private/rand
touch ./ca/index.txt
echo 1000 > ./ca/serial
echo 1000 > ./ca/crlnumber

echo "creating root CA's key (private/ca.key.pem)"
echo "  (password is 'xyzzy')"
openssl genrsa -aes256 -out ./ca/private/ca.key.pem -passout pass:xyzzy 4096

echo "creating root CA's certificate (certs/ca.cert.pem)"
openssl req -config openssl.cnf \
      -passin pass:xyzzy \
      -key ./ca/private/ca.key.pem \
      -new -x509 -days 7300 -sha256 -extensions v3_ca \
      -out ./ca/certs/ca.cert.pem \
      -subj '/C=DE/ST=Bavaria/L=Erlangen/O=Tavendo/CN=root_ca/'
openssl x509 -noout -text -in ./ca/certs/ca.cert.pem > /dev/null || exit $?

# XXX could make an intermediate CA here, but we'll just use the root
# for that. Might provide a "more realistic" example/environment to
# make an intermediate...

# okay, fuckit, making an intermediate
mkdir ./ca/intermediate
pushd ./ca/intermediate
mkdir certs crl csr newcerts private
touch index.txt
echo 1000 > serial
echo 1000 > crlnumber
popd

echo "creating intermediate CA's keypair"
openssl genrsa -aes256 \
      -passout pass:xyzzy \
      -out ./ca/intermediate/private/intermediate.key.pem 2048 || exit $?

echo "creating intermediate CA's cert"
openssl req -config openssl-intermediate.cnf -new -sha256 \
      -passin pass:xyzzy \
      -key ./ca/intermediate/private/intermediate.key.pem \
      -out ./ca/intermediate/csr/intermediate.csr.pem \
      -subj '/C=DE/ST=Bavaria/L=Erlangen/O=Tavendo/CN=intermediate_ca/' || exit $?

echo "signing intermediate CA with root CA"
openssl ca -config openssl.cnf -extensions v3_intermediate_ca \
      -passin pass:xyzzy -batch \
      -days 3650 -notext -md sha256 \
      -in ./ca/intermediate/csr/intermediate.csr.pem \
      -out ./ca/intermediate/certs/intermediate.cert.pem

echo 'checking intermediate certs; should see ..pem: OK'
openssl x509 -noout -text -in ./ca/intermediate/certs/intermediate.cert.pem > /dev/null || exit $?
openssl verify -CAfile ./ca/certs/ca.cert.pem ./ca/intermediate/certs/intermediate.cert.pem
cat ./ca/intermediate/certs/intermediate.cert.pem ./ca/certs/ca.cert.pem > ./ca/intermediate/certs/ca-chain.cert.pem


echo
echo "Whew!! We've made a CA, and an intermediate CA!"
echo "...and there was much rejoicing."
echo "Now, to make a server cert."
echo

echo "server_0: keypair"
openssl genrsa -aes256 \
      -passout pass:xyzzy -out ./ca/intermediate/private/server_0.key.pem 2048

echo "server_0: certificate signing request (CSR)"
openssl req -config openssl-intermediate.cnf \
      -passin pass:xyzzy -key ./ca/intermediate/private/server_0.key.pem \
      -new -sha256 -out ./ca/intermediate/csr/server_0.csr.pem \
      -subj '/C=DE/ST=Bavaria/L=Erlangen/O=Tavendo/CN=localhost/'

echo "server_0: actually signing CSR"
openssl ca -config openssl-intermediate.cnf \
      -passin pass:xyzzy -batch \
      -extensions server_cert -days 375 -notext -md sha256 \
      -in ./ca/intermediate/csr/server_0.csr.pem \
      -out ./ca/intermediate/certs/server_0.cert.pem
# should contain 1 entry, for the cert we just made ^^
cat ./ca/intermediate/index.txt

openssl x509 -noout -text -in ./ca/intermediate/certs/server_0.cert.pem > /dev/null || exit $?
openssl verify -CAfile ./ca/intermediate/certs/ca-chain.cert.pem \
      ./ca/intermediate/certs/server_0.cert.pem || exit $?

# Note: only difference for the client-certificate is "-extensions
# usr_cert" instead of "-extensions server_cert"
echo
echo "certaing a client-side certificate"
echo

echo "client_0: keypair"
openssl genrsa -aes256 \
      -passout pass:xyzzy -out ./ca/intermediate/private/client_0.key.pem 2048

echo "client_0: certificate signing request (CSR)"
openssl req -config openssl-intermediate.cnf \
      -passin pass:xyzzy -key ./ca/intermediate/private/client_0.key.pem \
      -new -sha256 -out ./ca/intermediate/csr/client_0.csr.pem \
      -subj '/C=DE/ST=Bavaria/L=Erlangen/O=Tavendo/CN=client_0/'

echo "client_0: actually signing CSR"
openssl ca -config openssl-intermediate.cnf \
      -passin pass:xyzzy -batch \
      -extensions usr_cert -days 375 -notext -md sha256 \
      -in ./ca/intermediate/csr/client_0.csr.pem \
      -out ./ca/intermediate/certs/client_0.cert.pem
# should contain 1 entry, for the cert we just made ^^
cat ./ca/intermediate/index.txt

openssl x509 -noout -text -in ./ca/intermediate/certs/client_0.cert.pem > /dev/null || exit $?
openssl verify -CAfile ./ca/intermediate/certs/ca-chain.cert.pem \
      ./ca/intermediate/certs/client_0.cert.pem || exit $?

#
# "deployment"; put our keys in the right spots
#

# redundant, but "nice" to see if you're running it...
openssl verify -CAfile ./ca/intermediate/certs/ca-chain.cert.pem \
      ./ca/intermediate/certs/server_0.cert.pem || exit $?

echo "Deploying private keys and certificates (into ./.crossbar/{server,client}.{key,crt})"
cp ./ca/intermediate/private/server_0.key.pem .crossbar/server.key
cp ./ca/intermediate/certs/server_0.cert.pem .crossbar/server.crt

cp ./ca/intermediate/private/client_0.key.pem .crossbar/client.key
cp ./ca/intermediate/certs/client_0.cert.pem .crossbar/client.crt

echo "Deploying intermediate and root CA certs"

cp ./ca/certs/ca.cert.pem .crossbar/ca.cert.pem
cp ./ca/intermediate/certs/intermediate.cert.pem .crossbar/intermediate.cert.pem

echo "removing passphrases from keys"

pushd ./.crossbar
openssl rsa -passin pass:xyzzy -in server.key -out server.new.key
mv server.new.key server.key

openssl rsa -passin pass:xyzzy -in client.key -out client.new.key
mv client.new.key client.key

echo "creating dhparam file"
openssl dhparam -outform PEM -out ./.crossbar/dhparam 2048
