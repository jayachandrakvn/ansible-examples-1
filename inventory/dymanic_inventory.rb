#!/usr/bin/env ruby

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

