#! /bin/bash

# requirements for cinder
sudo apt install libsqlite3-dev

# download and build cinder
git clone https://github.com/mrigankpawagi/cinder && cd cinder
./configure --enable-loadable-sqlite-extensions && make -j
cd ..

# create (and activate) venv with static-python
cinder/python -m venv env
source env/bin/activate
