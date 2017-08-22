# Welcome to Ansible examples by OpenTable!

Please check out our SF Ansiblefest 2017 "Case Study" presentation suitable for any audience [here](Ansiblefest2017/OT_case_study.pdf)

Another "deep dive" version (more technical) is available [here](Ansiblefest2017/OT_deep_dive.pdf)

## What is the prurpose of this repo
The first thing is - it __is not__ a tutorial for Ansible or Jinja2. It will not teach you from ground zero.
The idea behind this repo is - to keep a collection of semi-advanced coding examples for s/w engineers who are coming from different languages, but have limited experience with Ansible or jinja2 at the moment.
The hacky coding examples supposed to provoke extra "thinking" (like: "what does it do?" or "why does it even work?") and will help to realize the different ways to "do stuff" in Ansible. It provides you some kind of "hacking framework" where you modify the existing code, or add your own examples to see if they work the way you expect. 

## Brief overview of examples currently available
- The combined Ansible inventory consists of three parts: one static file, two dynamic scripts. One script executes locally and produces json output for partial inventory (the statically coded examples). It was simply a byproduct of the development of static examples in this repo: the script discovers new example files and adds them to the inventory automatically. But it is a good example how Ansible put togther all the sources available.
- the other dynamic inventory script is very simple - it queries a local WEB server that you need to start manually. The web server script is another example how to generate dynamic inventory from a 'source of truth' file where objects (hosts) have properties (attributes). This example might be particularly interesting for others because a WEB service could be exposed to multiple consumers (dev environment, prod/operations environment - everybody need host inventory).
- there are several examples about custom python filters OpenTable developed for its private Ansible project. Some of most common and more generic filters are publishes as examples (but not all).
- coding examples: reusable code fragments (include and macro). Those are pretty small and pretty basic, but they give you an idea...
- reusable YAML definitions: we can call them 'in-line jinja2 templates' because that is what they are by nature. When you define data object inside YAML file (host_vars, or group_vars - does not matter), the key is always immutable (string), and the value could be an "expression" in a form of jinja2 expression. That means you can manipulate data inside your YAML file. That allows for complex inheritance between host_vars and group_vars and global_vars (only watch for potencial loops). The lazy evaluation by Ansible would obtain the real value during the execution time.

## Interactive play with examples
If you wish to have hands-on experience with all examples and code fragments available in this repo, you may want to build python virtual environment by following those steps:
- sudo pip install virtualenv
- virtualenv --no-site-packages venv
- source venv/bin/activate
- pip install -r requirements.txt
- ansible-galaxy install -r requirements.yaml

Then you should be able to run ansible-playbook command like this:
```
(venv) user@host:~/ansible-examples $ ansible-playbook playbooks/example.yaml
```
which will give you a list of file-based examples (builtin_filters and custom_filters) that you may execute and see what they produce. The other two named 'reusable_*' won't work just yet because they need WEB-based dynamic inventory to populate those groups with real hosts (otherwise those groups are empty).
```
TASK [describe_examples : Display short descriptions for each category] ***********************************************************************************************
ok: [help] => {
    "msg": [
        "builtin_filters      - Builtin jinja2 filters plus extra - installed via requirements.txt", 
        "custom_filters       - Custom python filters we built ourselves", 
        "reusable_code        - Examples of reusable jinja2 macros", 
        "reusable_definitions - Using inline jinja2 as values for YAML variables"
    ]
}
```
The trick here is - we use static inventory file that has a single host entry called 'help'. The output you see is simply what is designed to show when you do not enforce any limit with '-l' flag, i.e. condition "{{ inventory_hostname == 'help'}}" is true. 

One dynamic inventory script 'local_file_based_examples.rb' scans local file system for code examples under the folder 'playbooks/examples' and populates and describes all those groups.
In fact, you may take a look at all static examples (related to python filters) by simply executing this command:
```
(venv) user@host:~/ansible-examples $ inventory/local_file_based_examples.rb --list | jq '.'
```

## Start local webserver to extend Ansible dynamic inventory further
When you enable additional dynamic inventory via local WEB server (details below), then you will see even more targets [to play with] in your total inventory, which, at this point, will be a combination of one static inventory file and two dynamic inventory scripts (one of those executed locally, and the other one calls WEB service you are about to start). To start very simple WEB server on your local box, you need to execute this command:
```
(venv) user@host:~/ansible-examples $ webserver/webserver.rb /dev/null &
```
Assuming that the webrick (ruby-based) web server started successfuly, one may verify what Ansible dynamic inventory would look like by running CLI command like this: "curl http://localhost:8880/dynamic_inventory | jq '.'". Note that you might need to install packages like 'curl' and 'jq' first. 

Example below only displays 'keys', or groups' names - in Ansible terms.
```
(venv) user@host:~/ansible-examples $ curl http://localhost:8880/dynamic_inventory | jq 'keys'
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

### Disclosure: This is primitive WEB server! If you modify the content of the source of truth YAML file 'webserver/inventory_file.yaml', you would need to restart the WEB server to force it to re-read the file...

Now each host-related example group (per-OS, like 'ios' or 'junos', or per-location like 'sf' or 'sc') would be addressable via "-l" argument of ansible-playbook command:
```
(venv) user@host:~/ansible-examples $ ansible-playbook playbooks/example.yaml -l reusable_definitions
or 
(venv) user@host:~/ansible-examples $ ansible-playbook playbooks/example.yaml -l reusable_code
or
(venv) user@host:~/ansible-examples $ ansible-playbook playbooks/example.yaml -l ios
or
(venv) user@host:~/ansible-examples $ ansible-playbook playbooks/example.yaml -l junos

and so on...
```
### Just a side note...
The 'example.yaml' playbook and its roles & plays under 'ansible-demo/playbooks' are nothing like the real ones that OpenTable uses for its private Ansible repo. They are oversimplified to do just one thing - run a small piece of code as standalone demo...
Exposing real playbooks is hard because they tightly integrated with the overall data structure and file structure of the entire project, and we have not put too much effort (yet) to make it more generic.
We copied some fragments of our code under '~/ansible-examples/as-is-no-warranty', but those will not work - they are "display only". It still might give you an idea or two, or maybe you would realized they are sub-optimal in one way or the other (that is absolutely plausible, we know that).
