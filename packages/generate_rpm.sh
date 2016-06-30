#!/bin/bash

yum -y install rpm-build git python-setuptools
mkdir /tmp/rpms
echo "%_unpackaged_files_terminate_build 0" > ~/.rpmmacros

git clone https://github.com/grycap/radl
cd radl
python setup.py bdist_rpm --requires="python-ply"
cp dist/*.noarch.rpm /tmp/rpms

