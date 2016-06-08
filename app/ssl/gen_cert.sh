#!/bin/bash

# Helper script for creating a self-signed certificate

# To list available curves:
#   openssl ecparam -list_curves

# https://wiki.openssl.org/index.php/Command_Line_Elliptic_Curve_Operations
openssl ecparam -name secp256k1 -out secp256k1.pem

# Options:
#   -nodes           don't encrypt the output key
#   -newkey rsa:bits generate a new RSA key of 'bits' in size
#   -newkey dsa:file generate a new DSA key, parameters taken from CA in 'file'
#   -newkey ec:file  generate a new EC key, parameters taken from CA in 'file'

openssl req \
    -new \
    -newkey ec:secp256k1.pem \
    -days 365 \
    -nodes \
    -x509 \
    -subj "/C=US/ST=FL/L=Gainesville/O=UF/CN=olass.com" \
    -keyout server.key \
    -out server.crt

rm secp256k1.pem
openssl x509 -noout -text -in server.crt

# generate a private key
#  openssl genrsa -aes256 -out server.key 4096
#  
#  # generate the csr
#  openssl req -new -nodes -key server.key -out server.csr
#  
#  # remove passphrase
#  cp server.key server.key.org && openssl rsa -in server.key.org -out server.key
#  
#  # sign the cert
#  openssl x509 -sha512 -req -days 365 -in server.csr -signkey server.key -out server.crt
#  
#  # result
#  openssl x509 -in server.crt -noout -text | grep 'Signature Algorithm' | head -1 | cut -d: -f2
#  
#  # cleanup
#  rm server.csr server.key.org
