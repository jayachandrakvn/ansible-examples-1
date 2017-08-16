#!/usr/bin/env python

import dns.resolver

#
# This filter generates a list of port names based on
# fixed prefix (first argument/string) and a simpler pattern
# for numeric range (second argument/string).
#
# We may extend that functionality further as we go
# by adding more sophisticated patterns to expand.
#
def expand_ports(prefix, pattern):
    a_z = pattern.split('..') # we expect definitions like '0..47'
    arr = []
    for i in range(int(a_z[0]), int(a_z[1]) + 1):
        arr.append(prefix + str(i))

    return arr

class FilterModule(object):
    def filters(self):
        return {
            'expand_ports': expand_ports,
        }
