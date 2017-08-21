# Welcome to Ansible examples by OpenTable!

Please check out our SF Ansiblefest 2017 "Case Study" presentation suitable for any audience [here](Ansiblefest2017/OT_case_study.pdf)

Another "deep dive" version (for geeks only) is available [here](Ansiblefest2017/OT_deep_dive.pdf)

## Interactive play with examples
If you wish to have hands-on experience with all examples and code fragments available in this repo, you may want to build python virtual environment by following those steps:
- sudo pip install virtualenv
- virtualenv --no-site-packages venv
- source venv/bin/activate
- pip install -r requirements.txt
- ansible-galaxy install -r requirements.yaml

Then you should be able to run ansible-playbook command like this:
```
(venv) user@host:~/github/ansible-examples $ ansible-playbook playbooks/example.yaml
```
which will give you a list of examples that you may execute and see what they produce (and examine their code, if interested).
```
TASK [describe_examples : Display short descriptions for each category] ***********************************************************************************************
skipping: [test]
ok: [help] => {
    "changed": false, 
    "msg": [
        "builtin_filters      - Ansible builtin filters and extra filters installed via pip requirements.txt", 
        "custom_filters       - Custom python filters we built ourselves to extend Ansible "
    ]
}
```
The trick here is - we use static inventory file that has a single host entry called 'help'. The output you see is simply what is designed to show when "{{ inventory_hostname == 'help'}}". But if you enable dynamic inventory (see next step - how to start a local web server), then you will have more targets to play with in your inventory.
In fact, you may want to see all static examples (related to python filters) by simply executing this command:
```
(venv) user@host:~/github/ansible-examples $ inventory/local_file_based_examples.rb --list | jq '.'
```

## Start local webserver for dynamic inventory from YAML file
The next step (after you see a list of examples' groups available from previous command)
would be to start a local web server that will support Ansible dynamic
inventory. For that you would need to run command similar to this:
```
(venv) user@host:~/github/ansible-examples $ webserver/webserver.rb  2> /dev/null &
```
Assuming that the webrick (ruby-based) web server started successfuly, one may verify what Ansible dynamic inventory would look like (by running CLI command like this: curl http://localhost:8880/dynamic_inventory | jq 'keys'). Note that you might need to install packages like 'curl' and 'jq' first. Example below only displays 'keys', or groups' names - in Ansible terms.
```
(venv) user@host:~/github/ansible-examples $ curl http://localhost:8880/dynamic_inventory | jq 'keys'
[
  "_meta",
  "all",
  "foobar",
  "h3c",
  "ios",
  "junos",
  "reusable_code",
  "reusable_definitions",
  "sc",
  "sf"
]
```

### Disclosure: This is primitive WEB server! If you modify the content of the source of truth YAML, you will have to restart the WEB server to force it to read new files from the disk...

Now each host-related example group (per-OS, like 'ios' or 'junos', or per-location like 'sf' or 'sc') would be addressable via "-l" argument of ansible-playbook command:
```
(venv) user@host:~/github/ansible-examples $ ansible-playbook playbooks/example.yaml -l reusable_definitions
```
