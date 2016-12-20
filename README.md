 Resource and Application Description Language (RADL) parser.
============================

* Version ![PyPI](https://img.shields.io/pypi/v/radl.svg)
* PyPI ![PypI](https://img.shields.io/pypi/dm/RADL.svg)
* Build [![Build Status](http://jenkins.i3m.upv.es/buildStatus/icon?job=radl-parser)](http://jenkins.i3m.upv.es/job/radl-parser/)

The main purpose of the Resource and Application description Language (RADL) is to specify 
the requirements of the scientific applications needed to be deployed in a virtualized 
computational infrastructure (cloud).Using a declarative scheme RADL considers distinct 
features related to:

* hardware, like CPU number, CPU architecture, and RAM size;
* software, like applications, libraries and data base systems;
* network, like network interface and DNS configuration; and
* contextualization, extra steps to set up an adequate environment for the application.

RADL is intended to be more abstract that other standards to specify virtual appliances, like OVF, 
and easily extensible with other tools, like contextualization languages such as Ansible.

Read the documentation at http://imdocs.readthedocs.org/en/latest/radl.html.

1. INSTALLATION
===============

1.1 REQUISITES
--------------

RADL is based on python, so Python 2.6 or higher runtime and standard library must
be installed in the system.

If you will use pip to install the IM, all the requisites will be installed.
You must install them if you will install RADL from sources.

It is also required to install the Python Lex & Yacc library (http://www.dabeaz.com/ply/).
It is available in all of the main distributions as 'python-ply' package.


1.2 INSTALLING
--------------

### 1.2.1 FROM PIP

You only have to call the install command of the pip tool with the RADL package.

```
pip install RADL
```

### 1.2.2 FROM SOURCE

Select a proper path where to install the RADL parser (i.e. /usr/local/radl, 
/opt/radl or other).

```
$ tar xvzf RADL-X.XX.tar.gz
$ chown -R root:root RADL-X.XX
$ mv RADL-X.XX /usr/local
```
