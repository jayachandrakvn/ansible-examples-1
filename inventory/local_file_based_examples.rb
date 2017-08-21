#!/usr/bin/env ruby

#
# This is internal script to support demo examples that extends Ansible
# dynamic inventory. In fact, every static file (YAML) and
# any executable script placed under ~/ansible-examples/inventory
# would extend the overall set of host inventory for Ansible.
# Ansible would execute them all and combine the results together.
#
# This particular script does extend Ansible dynamic inventory
# for the set of file-based examples. It is internal implementation
# intended to minimize the development effort of creating new examples.
#
# The results of that script are not part of WEB rest api, so
# that extension would only be available for a local host.
#
# The other part of dynamic inventory exposed via WEB supposed
# to be available to other hosts (ansible dev, ansible ops, etc)
# So inventory is produced in one place and consumed by many.
# But this script is not part of web rest api; it is local source only.
#
# In fact, by looking what that script returns via CLI command like this
# ~/ansible-examples/inventory $ ./local_file_based_examples.rb --list | jq '.'
# one may learn a great deal of all static-file-based examples as jq tool
# produces very nice human-readable output.
# With jq you see the code staged to be executed, and when you actually run
# a playbook, you will see the results of that code.
#

require 'json'

require_relative '../scripts/internal_dev_fs_tree.rb'

EXAMPLES_DIR = '../playbooks/examples'

def get_list
  root = File.dirname(File.expand_path(__FILE__))
  # Get all examples from local file system
  helper = FsTree::FsTree.new(root + '/' + EXAMPLES_DIR)
  all_fs_example = helper.all_examples

  # Now we add '_meta' attribute that Ansible will use
  # to extend host vars and group vars
  all_fs_example.merge!({
    '_meta' => {
      'hostvars'  => helper.all_hosts_meta,  # dynamically inject your per-host variables
    }
  })
  return all_fs_example.to_json
end

if ARGV[0] == '--list'
  puts get_list
elsif ARGV[0] == '--host'
  puts '{}'
end
