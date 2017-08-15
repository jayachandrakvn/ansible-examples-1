#!/usr/bin/env python

import pprint

def print_debug(stuff):
    pp = pprint.PrettyPrinter(indent=4)
    return pp.pformat(stuff)

class FilterModule(object):
    def filters(self):
        return {
            'pprint': print_debug,
        }
