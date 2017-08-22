### Welcome to collection of tasks (parts of different roles)

1) __napalm_show_diff.yaml__ is small, but very useful task. It allows us to stage a new version of JunOS config to the Juniper device and compare it to the running config. The "diff" will be returned and displayed at Ansible console for network engineer to review and decide whether to continue or abort.

2) __napalm_show_diff.yaml__ will give you an idea of all configuration fragments we developed by that moment. It registers a list (as Ansible variable) so the user may choose all fragments or just a subset when she runs a playbook.

3) __template_requested_fragments.yaml__ actually executes a "template" Ansible module for each code fragment that has been discovered on a file system. That allow us to maintain only a partial coverage for code fragments per OS type x per feature. That is right, we do not have to implement all 40+ features for all OS types we support, we may implement some features for some OS, but Ansible play won't fail if a particular file (template) is not found.

Thanks to creepy-but-useful way Ansible allows us to do so :)
```
when: src_files.results[item.0].stat.exists
```

4) The interesting property of __assemble_config.yaml__ is that it looks for "compilation" errors before staging new config to destination device. That allows us to detect missing data before we even connect to real network box. The latest approach to developing Ansible code is to put a specific string (like we do now: __NETOPS_BUILD_ERROR__) as default value when we try to lookup or calculate a specific value. If lookup fails for any reason, the default value will stick, and we will be able to detect that at the moment when we glue all smaller fragments together as a single "candidate" config file. 

5) Home-grown TCL/expect script __expect-cmd__
It helps us to get to network device admin CLI via serial console (takes care of username/password/enable and so on) and then it executes the list of commands passed as CLI arguments. It supports several meta-tags (like <<__CTRL_D__>> or <<__SLEEP=5__>>) so we would have better control over some commands that do not produce the CLI prompt until you send a special chracter like __CTRL_D__.
That TCL/expect script seems fairly stable now, and supports different OS: Cisco IOS, Cisco NXOS, Juniper EX/QFX (but have not really tested Juniper SRX yet).
It also assumes that your Ansible box (where you executing that script) has a proper API access to a console server named "conserver" - available in several Linux distributions. That allows your Ansible box not having a local seral cable connected directly to a network device, but instead it connects securely to a console server over TCP/IP, which has those local serial cables in [remote] place. 

6) __init_via_console_junos.yaml__ is a good (but not entirely complete) example of how Ansible play calls an external TCL/expect script, and what commands are to be executed at JunOS CLI. That includes two interesting things: pushing a candidate config to JunOS and store it as local file, and pushing SSH private RSA key and generting prublic key off of private key. Both rely on __CTRL_D__ to be sent - to get back to regular JunOS CLI prompt.

7) __gen_ssh_keys.yaml__ is also an interesting example that allows to reuse existing SSH keys for devices that already had been provisioned that way. If SSH key is not found (but required - setting inside Ansible host_var config) then new SSH RSA key is generated.
Private key is always stored in encrypted format. Some OS will take the encrypted private key (and will ask for passphrase), others would need unencrypted private key, which is produced on-the-fly so it __is not__ stored in clear text format on Ansible server.

8) __combine_facts.yaml__ is built to pull facts from a network device and store them locally, in order to provide a way for operators to quickly check device facts such as serialnumber, hostname, version, etc. An example of a fact file is stored in as-is-no-warranty/factcache
