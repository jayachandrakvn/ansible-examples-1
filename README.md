## Welcome to Ansible examples by OpenTable!

Please check out our SF Ansiblefest 2017 presentation [here](Ansiblefest2017/Ansiblefest_2017_OT.pdf)

If you wish to have hands-on experience with all examples and code fragments available in this repo, you may want to build python virtual environment by following those steps:
- sudo pip install virtualenv
- virtualenv --no-site-packages venv
- source venv/bin/activate
- pip install -r requirements.txt
- ansible-galaxy install -r requirements.yaml

Then you should be able to run ansible-playbook command like this:
```
ansible-playbook playbooks/example.yaml
```
which will give you a list of examples that you may execute and see what they produce (and examine their code, if interested).
