#!/usr/bin/env ruby

#
# This script shows how to bind Ansible and WEB rest api
# to produce dynamic inventory for Ansible.
# The web server supposed to return data in JSON format.
#
# WEB server developed in such a way that it generates list of
# host groups based on values of the attributes associated
# with each host in a host definition file at
# '~/ansible-examples/webserver/inventory_file.yaml'
#
# See '~/ansible-examples/webserver/webserver.rb' for more
# details about rest api implementation.
#
require 'open-uri'

INVENTORY_HOST = 'localhost' # CNAME to real server
INVENTORY_PORT = 8880
INVENTORY_URI = '/dynamic_inventory'

def get_list
  begin
    file = open("http://#{INVENTORY_HOST}:#{INVENTORY_PORT}#{INVENTORY_URI}")
  rescue
    '{}'
  else
    file.read
  end
end

if ARGV[0] == '--list'
  puts get_list
elsif ARGV[0] == '--host'
  puts '{}'
end

