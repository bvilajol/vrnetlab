#!/bin/bash -x

/usr/local/bin/ansible-playbook -i inventory.yml pb_configure_network.yml
