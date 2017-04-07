#! /usr/bin/env python
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

import sys
import os

TESTS_PATH = os.path.dirname(os.path.realpath(__file__)) 

sys.path.append("..")
sys.path.append(".")

from radl.radl_parse import parse_radl
from radl.radl import RADL, Features, Feature, RADLParseException, system, outport
from radl.radl_json import parse_radl as parse_radl_json, dump_radl as dump_radl_json
import unittest

class TestRADL(unittest.TestCase):
	def __init__(self, *args):
		unittest.TestCase.__init__(self, *args)

	def radl_check(self, radl, expected_lengths=None, check_output=True):
		self.assertIsInstance(radl, RADL)
		radl.check()
		if expected_lengths:
			lengths = [len(l) for l in [radl.networks, radl.systems, radl.deploys,
			                            radl.configures, radl.contextualize]]
			self.assertEqual(lengths, expected_lengths)
		if check_output:
			self.radl_check(parse_radl(str(radl)), expected_lengths, check_output=False)
	
	def test_basic(self):
		r = parse_radl(TESTS_PATH + "/test_radl_0.radl")
		self.radl_check(r, [1, 1, 1, 1, 0])
		s = r.get_system_by_name("curso-aws")
		self.assertIsInstance(s, system)
		self.assertEqual(len(s.features), 17)
		self.assertEqual(s.getValue("disk.0.os.name"), "linux")
		
		radl_json = dump_radl_json(r)
		r = parse_radl_json(radl_json)
		s = r.get_system_by_name("curso-aws")
		self.assertIsInstance(s, system)
		self.assertEqual(len(s.features), 17)
		self.assertEqual(s.getValue("disk.0.os.name"), "linux")

	def test_basic0(self):

		r = parse_radl(TESTS_PATH + "/test_radl_1.radl")
		self.radl_check(r, [2, 2, 0, 0, 0])
		s = r.get_system_by_name("main")
		self.assertEqual(s.getValue("cpu.arch"), "x86_64")
		self.assertEqual(s.getValue("net_interface.0.connection"), "publica")
		self.assertEqual(s.getValue("memory.size"), 536870912)
		s = r.get_system_by_name("wn")
		self.assertEqual(s.getValue("disk.0.image.url"), ['one://server.com/1','one://server2.com/1'])
		
		radl_json = dump_radl_json(r)
		r = parse_radl_json(radl_json)
		self.radl_check(r, [2, 2, 0, 0, 0])
		s = r.get_system_by_name("main")
		self.assertEqual(s.getValue("cpu.arch"), "x86_64")
		self.assertEqual(s.getValue("net_interface.0.connection"), "publica")
		self.assertEqual(s.getValue("cpu.arch"), "x86_64")
		self.assertEqual(s.getValue("memory.size"), 536870912)
		s = r.get_system_by_name("wn")
		self.assertEqual(s.getValue("disk.0.image.url"), ['one://server.com/1','one://server2.com/1'])

	def test_references(self):

		r = parse_radl(TESTS_PATH + "/test_radl_ref.radl")
		self.radl_check(r, [2, 2, 0, 2, 2])
		
		radl_json = dump_radl_json(r)
		r = parse_radl_json(radl_json)
		self.radl_check(r, [2, 2, 0, 2, 2])

	def test_logic0(self):

		f0 = Feature("prop", ">=", 0)
		f1 = Feature("prop", "<=", 5)
		self.assertEqual(Features._applyInter((None, None), (f0, None)), (f0, None))
		self.assertEqual(Features._applyInter((None, None), (None, f1)), (None, f1))

	def test_dup_features(self):

		radl = """
system main (
cpu.count>=1 and
cpu.count<=0
)		"""

		with self.assertRaises(RADLParseException) as ex:
			parse_radl(radl)
		self.assertEqual(ex.exception.line, 4)

		radl = """
system main (
cpu.count=1 and
cpu.count=2
)		"""

		with self.assertRaises(RADLParseException) as ex:
			parse_radl(radl)
		self.assertEqual(ex.exception.line, 4)

		radl = """
system main (
cpu.count>=1 and
cpu.count>=5 and
cpu.count>=0
)		"""

		parse_radl(radl)

		radl = """
system main (
cpu.count=1 and
cpu.count>=0
)		"""

		parse_radl(radl)

		radl = """
system main (
cpu.count>=1 and
cpu.count<=5
)		"""

		parse_radl(radl)

		radl = """
system main (
cpu.count>=5 and
cpu.count<=5
)		"""

		parse_radl(radl)

	def test_concrete(self):

		r = parse_radl(TESTS_PATH + "/test_radl_conc.radl")
		self.radl_check(r)
		s = r.get_system_by_name("main")
		self.assertIsInstance(s, system)
		concrete_s, score = s.concrete()
		self.assertIsInstance(concrete_s, system)
		self.assertEqual(score, 201)
		
		radl_json = dump_radl_json(r)
		r = parse_radl_json(radl_json)
		self.radl_check(r)
		s = r.get_system_by_name("main")
		self.assertIsInstance(s, system)
		concrete_s, score = s.concrete()
		self.assertIsInstance(concrete_s, system)
		self.assertEqual(score, 201)
		
		
	def test_outports(self):

		radl = """
network publica (outbound = 'yes' and outports='8899a-8899,22-22')

system main (
net_interface.0.connection = 'publica'
)		"""
		r = parse_radl(radl)
		with self.assertRaises(RADLParseException):
			self.radl_check(r)

		radl = """
network publica (outbound = 'yes' and outports='8899-8899,22-22,1:10')

system main (
net_interface.0.connection = 'publica'
)		"""
		r = parse_radl(radl)
		r.check()
		net = r.get_network_by_id('publica')
		expected_res = [outport(8899, 8899, 'tcp'), outport(22, 22, 'tcp'), outport(1, 10, 'tcp', True)]
		self.assertEqual(net.getOutPorts(), expected_res)

	def test_check_password(self):

		radl = """
network publica ()

system main (
disk.0.os.credentials.new.password = 'verysimple'
)		"""
		r = parse_radl(radl)
		with self.assertRaises(RADLParseException):
			r.check()
			
		radl = """
network publica ()

system main (
disk.0.os.credentials.new.password = 'NotS0simple+'
)		"""
		r = parse_radl(radl)
		r.check()
		
	def test_check_newline(self):
		radl = """
system test (
auth = 'asd asd asd asd asd asd asd as dasd asd as das dasd as das d                            asd \n' and
otra = 1
)
		"""
		r = parse_radl(radl)
		r.check()


	def test_empty_contextualize(self):
		radl = """
			system test (
			cpu.count>=1
			)
			
			deploy test 1
			
			contextualize ()
			"""
		r = parse_radl(radl)
		r.check()
		self.assertEqual(r.contextualize.items, {})
		
		radl_json = dump_radl_json(r)
		r = parse_radl_json(radl_json)
		r.check()
		self.assertEqual(r.contextualize.items, {})
		
		radl = """
			system test (
			cpu.count>=1
			)
			
			deploy test 1
			"""
		r = parse_radl(radl)
		r.check()
		self.assertEqual(r.contextualize.items, None)
		
		radl_json = dump_radl_json(r)
		r = parse_radl_json(radl_json)
		r.check()
		self.assertEqual(r.contextualize.items, None)

	def test_ansible_host(self):

		radl = """
ansible ansible_master (host = 'host' and credentials.username = 'user' and credentials.password = 'pass')
network net ()

system main (
ansible_host = 'ansible_master' and
net_interface.0.connection = 'net'
)		"""
		r = parse_radl(radl)
		self.radl_check(r)
		
		radl_json = dump_radl_json(r)
		r = parse_radl_json(radl_json)
		self.radl_check(r)

		radl = """
ansible ansible_master (host = 'host' and credentials.username = 'user' and credentials.password = 'pass')
network net ()

system main (
ansible_host = 'ansible_master1' and
net_interface.0.connection = 'net'
)		"""
		r = parse_radl(radl)
		
		with self.assertRaises(RADLParseException):
			self.radl_check(r)
			
		radl = """
ansible ansible_master (credentials.username = 'user' and credentials.password = 'pass')
network net ()

system main (
net_interface.0.connection = 'net'
)		"""
		r = parse_radl(radl)
		
		with self.assertRaises(RADLParseException):
			self.radl_check(r)
			
		radl = """
ansible ansible_master (host = 'host' and credentials.username = 'user')
network net ()

system main (
net_interface.0.connection = 'net'
)		"""
		r = parse_radl(radl)
		
		with self.assertRaises(RADLParseException):
			self.radl_check(r)

	def test_radl_with_two_public_nets(self):
		radl = """
network public_net ( outbound = 'yes' )
network public_net_1 ( outbound = 'yes' )

system node_with_nets (
net_interface.0.connection = 'public_net_1' and
net_interface.1.connection = 'public_net' and
net_interface.1.ip = '10.0.0.1'
)
		"""
		r = parse_radl(radl)
		r.check()
		self.assertEqual(r.getPublicIP(), "10.0.0.1")

if __name__ == "__main__":
	unittest.main()
