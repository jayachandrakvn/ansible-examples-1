#!/usr/bin/env python

import pprint
import unittest
import collections

def print_list_results(d, attr_key='item', attr_val='stdout'):
#    pprint.pprint(d)
    if not isinstance(d, collections.Iterable):
        return "print_list_results: wrong input - not iterable..."

    str_list = []
    err1 = "'%s' attr1 not found" % attr_key
    err2 = "'%s' attr2 not found" % attr_val

    for elem in d:
#        pprint.pprint(elem)
        item_name = elem.get(attr_key, err1)
        item_line = elem.get(attr_val, err2)
        str = "%-20s - %s" % (item_name, item_line)
        str_list.append(str)
    return str_list

class FilterModule(object):
    def filters(self):
        return {
            'print_list_results': print_list_results,
        }

#
# ---- Unit testing -----
#
class TestGetIn(unittest.TestCase):
    def setUp(self):
        self.happy_results = [
            {
                "_ansible_item_result": True,
                "changed": True,
                "cmd": "cat /Users/ykretov/github/ansible-examples/playbooks/examples/builtin_filters/description.txt",
                "delta": "0:00:00.014175",
                "end": "2017-08-14 16:39:31.087398",
                "invocation": { },
                "item": "builtin_filters",
                "rc": 0,
                "start": "2017-08-14 16:39:31.073223",
                "stderr": "",
                "stdout": "Ansible builtin filters...",
                "stdout_lines": [
                    "Ansible builtin filters..."
                ],
                "warnings": []
            },
            {
                "item":   "foo",
                "stdout": "bar"
            }
        ]
        self.unhappy_results = [
            {},
            { "item": "foo" },
            { "stdout": "bar"}
        ]
        self.empty_results = None

    def test_happy_path(self):
        self.assertEqual(
            print_list_results(self.happy_results),
            [
                "builtin_filters      - Ansible builtin filters...",
                "foo                  - bar"
            ])

    def test_unhappy_path(self):
        self.assertEqual(
            print_list_results(self.unhappy_results),
            [
                "'item' attr1 not found - 'stdout' attr2 not found",
                "foo                  - 'stdout' attr2 not found",
                "'item' attr1 not found - bar"
            ])

    def test_empty_input(self):
        self.assertEqual(
            print_list_results(self.empty_results),
            "print_list_results: wrong input - not iterable...")

if __name__ == "__main__":
    unittest.main()
