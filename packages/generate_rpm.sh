#!/bin/bash

yum -y install rpm-build python-setuptools
mkdir /tmp/rpms
echo "%_unpackaged_files_terminate_build 0" > ~/.rpmmacros

python setup.py bdist_rpm --requires="python-ply"
cp dist/*.noarch.rpm /tmp/rpms