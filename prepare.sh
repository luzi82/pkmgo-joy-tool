#!/bin/bash

set -e

rm -rf tmp/pgoencrypt.tar.gz
rm -rf third-party/pgoencrypt

mkdir -p tmp
pushd tmp
wget http://pgoapi.com/pgoencrypt.tar.gz
popd

mkdir -p third-party
pushd third-party
tar -xzf ../tmp/pgoencrypt.tar.gz
pushd pgoencrypt/src
make
popd
popd
