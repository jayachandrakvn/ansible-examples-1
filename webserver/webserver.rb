#!/usr/bin/env ruby

require 'webrick'
require 'json'

require_relative 'fs_tree.rb'

PORT = 8880
EXAMPLES_DIR = '/../playbooks/examples'

root = File.dirname(File.expand_path(__FILE__))
server = WEBrick::HTTPServer.new(Port: PORT, DocumentRoot: root + '/empty')

helper = FsTree::FsTree.new(root + EXAMPLES_DIR)

all_ansible_hosts = helper.all_examples.merge(
  '_meta' => {
    'hostvars' => {}
  }
)

server.mount_proc '/' do |_request, response|
  response.body = 'Hello, world!'
  response.content_type = 'text/plain'
end

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
