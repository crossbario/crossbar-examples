#!/bin/bash

openssl req -nodes -new -x509 -keyout ./.crossbar/server.key \
        -subj '/C=DE/ST=Bavaria/L=Erlangen/O=Crossbar/CN=localhost/' \
        -out ./.crossbar/server.crt
