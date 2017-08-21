#!/usr/bin/env python

import dns.resolver

#
# This filter resolves DNS name into IP.
#
# First parameter is the structure that may contains FQDN to resolve.
# Second parameter is a list of DNS servers to run a dns query against.
#
# The first parameter could be one of the following:
# 1. hash (dict). See possible options below...
# 2. string, which is treaded as FQDN
#
# If a dict, then it checks for the following keys:
# - 'ip':   if present, its value will be returned (not DNS query to run)
# - 'name': treated as FQDN to resolve
#
def get_ip_addr(host_hash, dns_servers_arr):
    if "ip" in host_hash:
        ip_candidate = host_hash["ip"]
    else:
        my_resolver = dns.resolver.Resolver()
        my_resolver.nameservers = dns_servers_arr
        if "name" in host_hash:
            fqdn = host_hash["name"]
        else:
            fqdn = host_hash
        try:
            answer = my_resolver.query(fqdn, "A")
        except Exception as err:
            ip_candidate = "NETOPS_BUILD_ERROR_DNS_failed"
        else:
            for data in answer:
                ip_candidate = data.address
                break

    return ip_candidate

class FilterModule(object):
    def filters(self):
        return {
            'get_ip_addr': get_ip_addr,
        }
