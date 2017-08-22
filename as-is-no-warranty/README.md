### Welcome to as-is no warranty section!

Here you may find some fragments of real Ansible code developed by OpenTable, but it won't be complete or described in much of details.
Also, that code might change in future, but that snapshot might remain outdated. The goal here is - to expose some 'interesting' solutions that are sometimes hard to find in Ansible documentation.
By the nature of our development cycle (when we started - we knew very little about Ansible), some older code may look ugly and inefficient. That is known issue, but it is not the first priority for us to fix.
When we decide to do major code cleaup, and possibly expose some code officially for public use, we might address those issues.

Both playbooks are real thing (snapshot):
- build_config
- init_via_console

They use (import) same variables from 'variables/common.yaml' - also real thing.
In that variables file you may see what fragments are part of initial provisioning over serial console (when no IP management address exists yet).

Tasks and vault subfolders have their own README files.
