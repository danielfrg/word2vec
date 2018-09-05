#!/usr/bin/env bash

mkdir -p $HOME/data
pushd $HOME/data
wget http://mattmahoney.net/dc/text8.zip -O text8.zip
unzip text8.zip
head -c 1000000 text8 > text8-1M
popd
