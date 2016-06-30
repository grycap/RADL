#!/bin/bash

apt update
apt install -y dh-make python-stdeb fakeroot python-all git python-setuptools
mkdir /tmp/debs

git clone https://github.com/grycap/radl
cd radl
python setup.py --command-packages=stdeb.command sdist_dsc --depends "python-ply" bdist_deb
cp deb_dist/*.deb /tmp/debs
