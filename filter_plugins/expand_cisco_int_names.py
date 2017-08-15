#!/usr/bin/env python

import re
import unittest
import pprint

KNOWN_NXOS_INTERFACES = [
    "Ethernet",
    "loopback",
    "port-channel",
    "vlan"
]

KNOWN_IOS_INTERFACES = [
    "GigabitEthernet",
    "FastEthernet",
    "Loopback",
    "Port-channel",
    "Vlan"
]

def nxos_short_name_to_long(shortname):
    for name in KNOWN_NXOS_INTERFACES:
        if shortname.lower() in name.lower():
            return name
    return "NETOPS_BUILD_ERROR_" + shortname

def ios_short_name_to_long(shortname):
    for name in KNOWN_IOS_INTERFACES:
        if shortname.lower() in name.lower():
            return name
    return "NETOPS_BUILD_ERROR_" + shortname


def xstr(s):
    return '' if s is None else str(s)

def expand_nxos_int_names(int_list):
    return _expand_cisco_int_names(int_list, nxos_short_name_to_long)

def expand_ios_int_names(int_list):
    return _expand_cisco_int_names(int_list, ios_short_name_to_long)

def expand_cisco_int_names(int_list, dev_os):
    if dev_os == 'ios':
        return expand_ios_int_names(int_list)
    if dev_os == 'nxos':
        return expand_nxos_int_names(int_list)
    return "NETOPS_BUILD_ERROR_unknown_Cisco_OS: " + str(dev_os)

def _expand_cisco_int_names(int_list, short_name_to_long):
    p = re.compile('^([a-z\-]+)(\d+)(\/\d+)?(\/\d+)?(\.\d+)?$', re.IGNORECASE)
    new_list = []
    input_list = int_list
    if not isinstance(int_list, list):
        input_list = [ int_list ]
    for name in input_list:
        m = p.search(name)
        if m:
            new_list.append(
                short_name_to_long(m.group(1))
                + m.group(2)
                + xstr(m.group(3))
                + xstr(m.group(4))
                + xstr(m.group(5))
            )
        else:
            new_list.append("NETOPS_BUILD_ERROR_" + name)
    if not isinstance(int_list, list):
        return new_list[0]
    else:
        return new_list

class FilterModule(object):
    def filters(self):
        return {
            'expand_cisco_int_names': expand_cisco_int_names,
        }

#
# --------- testing -----------
#
class TestNxosShortNameToLong(unittest.TestCase):
    def setUp(self):
      self.ethernet = ['e', 'Et', 'eth' ]
      self.loopback = 'Lo'
      self.lag = 'Po'
      self.vlan = 'Vlan'
      self.UNKNOWN = 'XXlan'

    def test_all_known(self):
        for ether_name in self.ethernet:
            self.assertEqual(nxos_short_name_to_long(ether_name), KNOWN_NXOS_INTERFACES[0])
        self.assertEqual(nxos_short_name_to_long(self.loopback), KNOWN_NXOS_INTERFACES[1])
        self.assertEqual(nxos_short_name_to_long(self.lag), KNOWN_NXOS_INTERFACES[2])
        self.assertEqual(nxos_short_name_to_long(self.vlan), KNOWN_NXOS_INTERFACES[3])

    def test_unknown(self):
        self.assertEqual(nxos_short_name_to_long(self.UNKNOWN), 'NETOPS_BUILD_ERROR_' + self.UNKNOWN)

class TestIosShortNameToLong(unittest.TestCase):
    def setUp(self):
      self.giga = ['Gi', 'g', 'gig' ]
      self.fast = ['Fa', 'FastE' ]
      self.loopback = 'Lo'
      self.lag = 'Po'
      self.vlan = 'Vlan'
      self.UNKNOWN = 'XXlan'

    def test_all_known(self):
        for ether_name in self.giga:
            self.assertEqual(ios_short_name_to_long(ether_name), KNOWN_IOS_INTERFACES[0])
        for ether_name in self.fast:
            self.assertEqual(ios_short_name_to_long(ether_name), KNOWN_IOS_INTERFACES[1])
        self.assertEqual(ios_short_name_to_long(self.loopback), KNOWN_IOS_INTERFACES[2])
        self.assertEqual(ios_short_name_to_long(self.lag), KNOWN_IOS_INTERFACES[3])
        self.assertEqual(ios_short_name_to_long(self.vlan), KNOWN_IOS_INTERFACES[4])

    def test_unknown(self):
        self.assertEqual(ios_short_name_to_long(self.UNKNOWN), 'NETOPS_BUILD_ERROR_' + self.UNKNOWN)

class TestExpandNxosIntNames(unittest.TestCase):
    def setUp(self):
        self.example_good = [
            'Po101',
            'Lo253',
            'Eth1/13',
            'Eth1/13.200',
            'Vlan200'
        ]
        self.example_bad = [
            'Et',
            '253',
            '1/13',
            '1/13.200'
        ]

    def test_regexp_match_good(self):
        self.assertEqual(expand_nxos_int_names(self.example_good), [
            'port-channel101',
            'loopback253',
            'Ethernet1/13',
            'Ethernet1/13.200',
            'vlan200'
        ])
        self.assertEqual(
             expand_nxos_int_names('port-ch101'),
             'port-channel101')

    def test_regexp_match_bad(self):
        self.assertEqual(expand_nxos_int_names(self.example_bad), [
            'NETOPS_BUILD_ERROR_Et',
            'NETOPS_BUILD_ERROR_253',
            'NETOPS_BUILD_ERROR_1/13',
            'NETOPS_BUILD_ERROR_1/13.200'
        ])

class TestExpandIosIntNames(unittest.TestCase):
    def setUp(self):
        self.example_good = [
            'Po101',
            'Lo253',
            'Fa1/13',
            'Gi1/13.200',
            'gi0/0/0',
            'Vlan200'
        ]
        self.example_bad = [
            'Et',
            '253',
            '1/13',
            '1/13.200'
        ]

    def test_regexp_match_good(self):
        self.assertEqual(expand_ios_int_names(self.example_good), [
            'Port-channel101',
            'Loopback253',
            'FastEthernet1/13',
            'GigabitEthernet1/13.200',
            'GigabitEthernet0/0/0',
            'Vlan200'
        ])
        self.assertEqual(
             expand_ios_int_names('port-ch101'),
             'Port-channel101')

    def test_regexp_match_bad(self):
        self.assertEqual(expand_ios_int_names(self.example_bad), [
            'NETOPS_BUILD_ERROR_Et',
            'NETOPS_BUILD_ERROR_253',
            'NETOPS_BUILD_ERROR_1/13',
            'NETOPS_BUILD_ERROR_1/13.200'
        ])

if __name__ == "__main__":
    unittest.main()
