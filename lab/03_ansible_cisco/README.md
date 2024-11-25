# Lab 03 - ANSIBLE

Run Cisco virtual instances and vr-xcon for links

        sudo docker run -d --name vr1 --privileged vrnetlab/vr-csr:17.03.07
        sudo docker run -d --name vr2 --privileged vrnetlab/vr-csr:17.03.07
        sudo docker run -d --name vr3 --privileged vrnetlab/vr-csr:17.03.07

        docker run -d --privileged --name vr-xcon --link vr1 --link vr2 --link vr3 vrnetlab/vr-xcon --p2p vr1/1--vr2/2 vr2/1--vr3/2 vr3/1--vr1/2

Result:

        (net) waas@xtux:~/projects/vrnetlab/lab/03_ansible_cisco$ sudo docker ps
        [sudo] password for waas: 
        IMAGE                      COMMAND                  CREATED        STATUS                        PORTS                                                 NAMES
        vrnetlab/vr-xcon           "/xcon.py --p2p vr1/…"   11 hours ago   Up 11 hours       (healthy)                                                         vr-xcon
        vrnetlab/vr-csr:17.03.07   "/launch.py"             11 hours ago   Up 11 hours (healthy)   22/tcp, 830/tcp,      5000/tcp, 10000-10099/tcp, 161/udp   vr3
        vrnetlab/vr-csr:17.03.07   "/launch.py"             11 hours ago   Up 11 hours (healthy)   22/tcp, 830/tcp,      5000/tcp, 10000-10099/tcp, 161/udp   vr2
        vrnetlab/vr-csr:17.03.07   "/launch.py"             11 hours ago   Up 11 hours (healthy)   22/tcp, 830/tcp,      5000/tcp, 10000-10099/tcp, 161/udp   vr1

Virtual routers will be available on the bridge.

        waas@xtux:~/projects/vrnetlab/lab/03_ansible_cisco$ sudo docker inspect bridge
        ...
            "8eddfc9cf0748ddff0a0e9088287a3bf07b5d29c27dd0c47b83cf7b3920b3e41": {
                "Name": "vr3",
                "EndpointID": "861241dc9c64ad6792415b260be709c415c7d3b0c52f33340fee577d1e362b34",
                "MacAddress": "02:42:ac:11:00:04",
                "IPv4Address": "172.17.0.4/16",
                "IPv6Address": ""
            },
            "98d7ec91fcd16129e3a763083882064f25d6f56e500a52b4e913eaa22de01817": {
                "Name": "vr2",
                "EndpointID": "254ccbe25fe84994fb5ed89440d2a47f75e7d2eadbb8dacf3a80a8eca25d63c1",
                "MacAddress": "02:42:ac:11:00:03",
                "IPv4Address": "172.17.0.3/16",
                "IPv6Address": ""
            },
            "f240dc792d05cfec11bb161ce66c036c1c9e943d664b2c223d0a299b833cff64": {
                "Name": "vr1",
                "EndpointID": "705bc1edb3c3c199f16a1a49a1fbd4b908e31d3f03a9806bf436353f970a08f4",
                "MacAddress": "02:42:ac:11:00:02",
                "IPv4Address": "172.17.0.2/16",
                "IPv6Address": ""
            }

Those IP's are used within the ansible inventory.

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

Playbook exec:

        (net) waas@xtux:~/projects/vrnetlab/lab/03_ansible_cisco$ ansible-playbook -i inventory.yml pb_configure_network.yml
        
        PLAY [Exercice 2]       
        
        TASK [Configure interfaces i no t'equivoquis de vía]
        changed: [172.17.0.3]
        changed: [172.17.0.2]
        changed: [172.17.0.4]
        
        TASK [Connectivity validation i xapa bé les cintes]
        ok: [172.17.0.3]
        ok: [172.17.0.4]
        ok: [172.17.0.2]
        
        TASK [Configure BGP i recorda la reunió]
        ok: [172.17.0.3]
        ok: [172.17.0.4]
        ok: [172.17.0.2]
        
        TASK [Get IP BGP Summary i assegura amb ganes]
        ok: [172.17.0.2]
        ok: [172.17.0.3]
        ok: [172.17.0.4]
        
        TASK [BGP Peering Validation i escala el finde]
        ok: [172.17.0.4]
        ok: [172.17.0.2]
        ok: [172.17.0.3]
        
        PLAY RECAP
        172.17.0.2  : ok=5    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
        172.17.0.3  : ok=5    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
        172.17.0.4  : ok=5    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
