require 'yaml'
#
# This piece of code is to demonstrate how you may build
# Ansible dynamic inventory out of single static file
# which describes all your hosts with random set of attributes.
#
# Example of YAML data file, aka the "source of truth".
# ---
# host_1:
#   loc: 'sf' # San Francisco
#   os:  'linux'
# host_2:
#   loc: 'sc' # Santa Clara
#   os:  'junos'  # Juniper OS
# host_3:
#   loc: 'sf'
#   os:  'ios'  # Cisco IOS
#
# ================================
# As a result, script will return a hash object with keys
# and values like this:
# { 'all'   => ['host_1', 'host_2', 'host_3'], # Ansible expects all objects here
#   'sf'    => ['host_1', 'host_3'],  # comes from 'loc' attr
#   'sc'    => ['host_2'],            # comes from 'loc' attr
#   'linux' => ['host_1'],            # comes from 'os'  attr
#   'junos' => ['host_2'],            # comes from 'os'  attr
#   'ios'   => ['host_3']             # comes from 'os'  attr
# }
#

module AnsibleInventory
  #
  # This class is designed to generate a list of all
  # possible values of attributes ever mentioned for any host definition.
  # Then, for each attr value it generates a list of hosts that have
  # that attr with that specific value.
  #
  # This is generic code self-adopting to the number of attributes
  # and all different values of all of those attributes, so one does not
  # have to worry about changing the code when new single attribute
  # is added (or new value for the attribute is added) - it will self-adapt.
  #
  # Only limitation to keep in mind - you will need to restart webserver
  # because class initialization (reading YAML file) only happens once when
  # webserver starts. It does not re-read YAML data file when changes are made
  # to the file - you need to restart web server to re-read it.
  #
  class SingleAttr
    attr_reader :entire_config # deserialization of your YAML file
    attr_reader :hosts  # list of all host names

    def initialize(file_path)
      file_content = File.read(file_path)
      @entire_config = YAML.safe_load(file_content)
      @hosts = entire_config.keys.sort
    end

    #
    # It returns the array of all values for specific attribute name
    # passed as parameter. In our case, attr values will be 'loc' or 'os'.
    # But it is generic code - will accept any value if you add more
    # attributes in the future (no need to change the code).
    #
    def attr_values(attr)
      entire_config.values.map { |v| v[attr] }.compact.sort.uniq
    end

    #
    # This helper function returns the list of host names
    # that contain a specific attribute (property) with a
    # specific value (value).
    #
    def hosts_per(property, value)
      hosts.select { |host| entire_config[host][property] == value }
    end

    #
    # generates a list of all attributes ever mentioned under any host.
    # The ruby code is intentionally 'sub-optimal' to make it easier
    # to understand for non-ruby programmers
    #
    def all_attributes
      all_attrs_with_dups = hosts.map { |host| entire_config[host].keys }
      return all_attrs_with_dups.flatten.sort.uniq
    end

    #
    # generates a list of all groups as uniq values for *all* attributes.
    # The ruby code is intentionally 'sub-optimal' to make it easier
    # to understand for non-ruby programmers.
    # We do not care about efficiency of our nested loops;
    # instead we care about humans to understand the logic.
    #
    def generate_each_group
      all_groups = {}
      all_attributes.each do |attr_name|
        attr_values(attr_name).each do |attr_value|
          hosts_matched = hosts_per(attr_name, attr_value)
          all_groups.merge!({attr_value => hosts_matched})
        end
      end
      return all_groups
    end

    #
    # This function produces the entire host-based inventory.
    # It combines all hosts with each group that is generated
    # based on single attribute.
    #
    def all_hosts
      { 'all' => hosts }.merge(
        generate_each_group)
    end

    def all_groups_meta
      meta = {}
      all_attributes.each do |attr_name|
        attr_values(attr_name).each do |attr_value|
          origin = {'origin' => "Group '#{attr_value}' coming from host attribute '#{attr_name}'"}
          meta.merge!({attr_value => origin})
        end
      end
      return meta
    end

  end
end
