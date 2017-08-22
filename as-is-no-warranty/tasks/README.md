### Welcome to collection of tasks (parts of different roles)

__napalm_show_diff.yaml__ is small, but very useful task. It allows us to stage a new version of JunOS config to the Juniper device and compare it to the running config. The "diff" will be returned and displayed at Ansible console for network engineer to review and decide whether to continue or abort.

__napalm_show_diff.yaml__ will give you an idea of all configuration fragments we developed by that moment. It registers a list (as Ansible variable) so the user may choose all fragments or just a subset when she runs a playbook.

__template_requested_fragments.yaml__ actually executes a "template" Ansible module for each code fragment that has been discovered on a file system. That allow us to maintain only a partial coverage for code fragments per OS type x per feature. That is right, we do not have to implement all 40+ features for all OS types we support, we may implement some featrues for some OS, but Ansible play won't fail if a particular file (template) is not found.

Thanks to creepy-but-useful way Ansible allows us to do so :)
```
when: src_files.results[item.0].stat.exists
```
