# Resource and Application Description Language (RADL) parser

[![PyPI](https://img.shields.io/pypi/v/radl.svg)](https://pypi.org/project/radl)
[![Tests](https://github.com/grycap/RADL/actions/workflows/main.yaml/badge.svg)](https://github.com/grycap/RADL/actions/workflows/main.yaml)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9f9c0257b8b84a6daff76fbe09a9ce18)](https://www.codacy.com/app/micafer/radl)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/9f9c0257b8b84a6daff76fbe09a9ce18)](https://www.codacy.com/app/micafer/radl)
[![License](https://img.shields.io/badge/license-GPL%20v3.0-brightgreen.svg)](LICENSE)

The main purpose of the Resource and Application description Language (RADL) is to specify 
the requirements of the scientific applications needed to be deployed in a virtualized 
computational infrastructure (cloud).Using a declarative scheme RADL considers distinct 
features related to:

*   hardware, like CPU number, CPU architecture, and RAM size;
*   software, like applications, libraries and data base systems;
*   network, like network interface and DNS configuration; and
*   contextualization, extra steps to set up an adequate environment for the application.

RADL is intended to be more abstract that other standards to specify virtual appliances, like OVF, 
and easily extensible with other tools, like contextualization languages such as Ansible.

Read the documentation at <http://imdocs.readthedocs.org/en/latest/radl.html>.
 
## 1 INSTALLATION

### 1.1 REQUISITES

RADL is based on python, so Python 2.6 or higher runtime and standard library must
be installed in the system. It is compatible with both Python 2 and Python 3.

If you will use pip to install the IM, all the requisites will be installed.
You must install them if you will install RADL from sources.

It is also required to install the Python Lex & Yacc library (<http://www.dabeaz.com/ply/>).
It is available in all of the main distributions as 'python-ply' package or 'ply' using pip.

### 1.2 INSTALLING

#### 1.2.1 FROM PIP

You only have to call the install command of the pip tool with the RADL package.

```sh
pip install RADL
```

#### 1.2.2 FROM SOURCE

Select a proper path where to install the RADL parser (i.e. /usr/local/radl, 
/opt/radl or other).

```sh
tar xvzf RADL-X.XX.tar.gz
chown -R root:root RADL-X.XX
mv RADL-X.XX /usr/local
```
