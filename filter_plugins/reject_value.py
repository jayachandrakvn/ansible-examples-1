#!/usr/bin/env python

#import pprint

def reject_values(arr, values):
    new_arr = [l for l in arr if l not in values]
    return new_arr

class FilterModule(object):
    def filters(self):
        return {
            'reject_values': reject_values,
        }
