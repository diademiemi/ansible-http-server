#!/bin/bash
# Run this relative to the collection root
# ./copy-role-template.sh example

export role_name=$1

cp .github/workflow-templates/ansible-role-template.yml .github/workflows/ansible-role-$role_name.yml

sed -i "s/template/$role_name/g" .github/workflows/ansible-role-$role_name.yml

echo "Workflow for $role_name created"