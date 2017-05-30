#!/usr/bin/env python

#import pprint

def print_list_results(d, attr_key='item', attr_val='stdout'):
#    pprint.pprint(d)
    str_list = []
    for elem in d:
        item_name = elem[attr_key]
        item_line = elem[attr_val]
        str = "%-20s - %s" % (item_name, item_line)
#        pprint.pprint(str)
        str_list.append(str)
    return str_list

class FilterModule(object):
    def filters(self):
        return {
            'print_list_results': print_list_results,
        }
