#!/usr/bin/env ruby

require 'webrick'
require 'json'

require_relative 'internal_dev_fs_tree.rb'
require_relative 'example_hosts_dyn_inventory.rb'

PORT = 8880
EXAMPLES_DIR = '../playbooks/examples'
HOST_INVENTORY_FILE = 'inventory_file.yaml'

root = File.dirname(File.expand_path(__FILE__))
server = WEBrick::HTTPServer.new(Port: PORT, DocumentRoot: root + '/empty')

# 1. get all examples from local file system
helper1 = FsTree::FsTree.new(root + '/' + EXAMPLES_DIR)
all_fs_example = helper1.all_examples

# 2. Get every host from host inventory file
helper2 = AnsibleInventory::SingleAttr.new(root + '/' + HOST_INVENTORY_FILE)
all_hosts_from_source_of_truth = helper2.all_hosts

# 3. little trick - now we need to merge two ['all'] sets we got
#    from two different sources: general purpose host-based inventory
#    and file-based examples that is unique to this demo.

combined_sections_named_all = all_fs_example['all'] +
  all_hosts_from_source_of_truth['all']  # combining two arrays together

# 4. Now we can produce the united version of both inventory sources:
all_ansible_hosts = all_fs_example.merge(
  all_hosts_from_source_of_truth).merge({
    'all' => combined_sections_named_all
  }) # the last one will overwrite the ['all'] section

# 5. Now we add '_meta' attribute that Ansible will use
#    to extend host vars and group vars
all_ansible_hosts.merge!({
  '_meta' => {
    'hostvars ' => helper1.all_hosts_meta,  # dynamically inject your per-host variables
    'groupvars' => helper2.all_groups_meta  # dynamically inject your per-group variables
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

# BUT.....
# Since we have a local web server, we are free to expose
# [via REST API] whatever we want! For example, we can expose host-based
# inventory separately - for possible troubleshooting, or for easier
# understanding (because that host-based inventory what people really care about)
#
# To see what is in there you may run this CLI command
# (you might need to install two utilities: curl and jq):
#
#  your_box> curl http://localhost:8880/debug_host_inventory | jq '.'
#
server.mount_proc '/debug_host_inventory' do |_request, response|
  response.body = all_hosts_from_source_of_truth.merge({
    '_meta' => {
      'groupvars' => helper2.all_groups_meta  # dynamically inject your per-group variables
    }
  }).to_json
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
