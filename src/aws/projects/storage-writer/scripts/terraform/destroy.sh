#!/bin/bash
set -e
terraform -chdir=deploy/terraform destroy -auto-approve
rm -f deploy/dist/function.zip
