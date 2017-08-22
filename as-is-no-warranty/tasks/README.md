### Welcome to collection of tasks (parts of different roles)

1) __napalm_show_diff.yaml__ is small, but very useful task. It allows us to stage a new version of JunOS config to the Juniper device and compare it to the running config. The "diff" will be returned and displayed at Ansible console for network engineer to review and decide whether to continue or abort.

2) __napalm_show_diff.yaml__ will give you an idea of all configuration fragments we developed by that moment. It registers a list (as Ansible variable) so the user may choose all fragments or just a subset when she runs a playbook.

3) __template_requested_fragments.yaml__ actually executes a "template" Ansible module for each code fragment that has been discovered on a file system. That allow us to maintain only a partial coverage for code fragments per OS type x per feature. That is right, we do not have to implement all 40+ features for all OS types we support, we may implement some features for some OS, but Ansible play won't fail if a particular file (template) is not found.

Thanks to creepy-but-useful way Ansible allows us to do so :)
```
when: src_files.results[item.0].stat.exists
```

4) The interesting property of __assemble_config.yaml__ is that it looks for "compilation" errors before staging new config to destination device. That allows us to detect missing data before we even connect to real network box. The latest approach to developing Ansible code is to put a specific string (like we do now: __NETOPS_BUILD_ERROR__) as default value when we try to lookup or calculate a specific value. If lookup fails for any reason, the default value will stick, and we will be able to detect that at the moment when we glue all smaller fragments together as a single "candidate" config file. 
