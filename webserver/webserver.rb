#!/usr/bin/env ruby

require 'webrick'
require 'json'

require_relative '../scripts/hosts_dyn_inventory.rb'

PORT = 8880
HOST_INVENTORY_FILE = 'inventory_file.yaml'

root = File.dirname(File.expand_path(__FILE__))
server = WEBrick::HTTPServer.new(Port: PORT, DocumentRoot: root + '/empty')

# Generate all host groups from host inventory file
helper = AnsibleInventory::SingleAttr.new(root + '/' + HOST_INVENTORY_FILE)
all_ansible_hosts = helper.all_hosts

# Now we add '_meta' attribute that Ansible will use
# to extend host vars and group vars
all_ansible_hosts.merge!({
  '_meta' => {
    'groupvars' => helper.all_groups_meta  # dynamically inject your per-group variables
  }
})

server.mount_proc '/' do |_request, response|
  response.body = 'Hello, world!'
  response.content_type = 'text/plain'
end

# This is the most important URL to support. It's hard-coded in Ansible
# dynamic inventory script 'inventory/dynamic_inventory.rb'
server.mount_proc '/dynamic_inventory' do |_request, response|
  response.body = all_ansible_hosts.to_json
  response.content_type = 'text/json'
end

#
# The following command will provide a hook to shutdown the server
# (often done with Ctrl+C)
#
trap('INT') { server.shutdown }
#
# Start the server
#
server.start
