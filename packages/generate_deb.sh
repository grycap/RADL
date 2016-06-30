#!/bin/bash

apt update
apt install -y dh-make python-stdeb
python setup.py --command-packages=stdeb.command sdist_dsc --depends "python-ply" bdist_deb
mkdir dist_pkg
cp deb_dist/*.deb dist_pkg