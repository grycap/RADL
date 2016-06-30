#!/bin/bash

apt update
apt install -y dh-make python-stdeb fakeroot python-all python-setuptools
python setup.py --command-packages=stdeb.command sdist_dsc --depends "python-ply" bdist_deb
cp deb_dist/*.deb dist/