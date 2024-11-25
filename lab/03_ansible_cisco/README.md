# Lab 03 - ANSIBLE

Inventory file results in:

        ansible-inventory -i inventory.yml --graph

        @all:
        |--@ungrouped:
        |--@routers:
        |  |--@vr1:
        |  |  |--172.17.0.2
        |  |--@vr2:
        |  |  |--172.17.0.3
        |  |--@vr3:
        |  |  |--172.17.0.4

Basic connectivity check:

        ansible all -i inventory.yml -m ping
        172.17.0.4 | SUCCESS => {
            "changed": false,
            "ping": "pong"
        }
        172.17.0.2 | SUCCESS => {
            "changed": false,
            "ping": "pong"
        }
        172.17.0.3 | SUCCESS => {
            "changed": false,
            "ping": "pong"
        }
