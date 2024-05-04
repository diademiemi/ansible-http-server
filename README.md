Ansible Collection - diademiemi.template
========================================
Documentation for the collection template.

Contents 
========

Roles
------
Role | Description | CI Status
--- | --- | ---
<!-- [diademiemi.template.EXAMPLE](./roles/template/) | Install EXAMPLE | [![Molecule test](https://github.com/diademiemi/ansible_collection_diademiemi.template/actions/workflows/ansible-role-EXAMPLE.yml/badge.svg)](https://github.com/diademiemi/ansible_collection_diademiemi.template/actions/workflows/ansible-role-EXAMPLE.yml) -->

Click on the role to see the README for that role.  

Collection Structure
--------------

This collection makes use of my [Ansible Role Template repository](https://github.com/diademiemi/ansible_role_%74emplate.git).  The `add-role.sh` script downloads this Template and generates a new role with the name specified. If a `molecule/default/molecule.yml` file is present, it will be ran with GitHub Actions.  
<!-- I use %74 here to encode to a "t" so it doesnt get recursively replaced. The .git causes a redirect so you end up at the right URL :)-->

Usage:
```bash
export NEW_ROLE_NAME="new_role"
./add-role.sh ${NEW_ROLE_NAME}
```

Using Template
--------------
To use this template for a new role, run


```bash
export NEW_ROLE_NAME="NEW_NAME"
export GITHUB_USER="diademiemi"
export GALAXY_API_KEY="YOUR_API_KEY"

find . -type f -exec sed -i "s/diademiemi/${GITHUB_USER}/g" {} + # Do not run this more than once
find . -type f -exec sed -i "s/template/${NEW_ROLE_NAME}/g" {} + # Do not run this more than once

# Assumes repo is named ansible_role_${NEW_ROLE_NAME}
gh secret set GALAXY_API_KEY -R ${GITHUB_USER}/ansible_collection_${GITHUB_USER}.${NEW_COLLECTION_NAME} -a actions -b ${GALAXY_API_KEY}

# Remove this section from README.md
sed -i "/Using Template/Q" README.md
```

This is also provided as a script as `replace.sh`.  
