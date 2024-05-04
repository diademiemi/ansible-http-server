#!/bin/bash

echo "Enter role name: "
read role_name

mkdir -p ./roles/$role_name

wget -O /tmp/ansible_role_template.$$ https://github.com/diademiemi/ansible_role_template/archive/refs/heads/main.zip 

./.github/workflow-templates/copy-role-template.sh $role_name

cd ./roles/$role_name

ln -s . ansible_role_template-main
unzip /tmp/ansible_role_template.$$
rm ansible_role_template-main

rm /tmp/ansible_role_template.$$

ROLE_IN_COLLECTION="true" bash replace.sh $role_name

echo "Role $role_name created"