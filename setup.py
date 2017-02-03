#!/usr/bin/python
#
# IM - Infrastructure Manager
# Copyright (C) 2011 - GRyCAP - Universitat Politecnica de Valencia
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from radl import __version__ as version
from setuptools import setup

setup(  name="RADL", version=version, 
        author='GRyCAP - Universitat Politecnica de Valencia',
        author_email='micafer1@upv.es',
        url='https://github.com/grycap/RADL',
        packages=['radl'],
        license="GPL version 3, http://www.gnu.org/licenses/gpl-3.0.txt",
        long_description="The main purpose of the Resource and Application description Language (RADL) is to specify the requirements of the scientific applications needed to be deployed in a virtualized computational infrastructure (cloud). It is compatible with both Python 2 and Python 3",
        description="Resource and Application Description Language (RADL) parser.",
        platforms=["any"],
        install_requires=["ply"]
)
