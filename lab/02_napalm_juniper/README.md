# Lab 02 - Introduction to NAPALM

* You need to build your own containers for the network devices.
* Created simple eBGP scenario of three Cisco CSR1000v nodes.
* Pyton NAPALM is used to configure and validate the scenario.

<p align="center" width="50%">
    <img width="50%" src="lab.png">
</p>

## 0. Build the image

* Download vmx-bundle-18.2R1.9.tgz or any other "officially tested" version, as this is not...
* Follow the instructions on [vrnetlab](https://github.com/vrnetlab/vrnetlab/blob/master/vmx/README.md)
* vr-xcon is also needed, but available on docker-images

        sudo docker images
  
        REPOSITORY         TAG         IMAGE ID       CREATED             SIZE
        vrnetlab/vr-vmx    18.2R1.9    276886efe488   4 months ago     5.92GB
        vrnetlab/vr-xcon   latest      0843f237b02a   4 years ago      153MB




sudo docker run -d --name vr1 --privileged vrnetlab/vr-vmx:18.2R1.9
sudo docker run -d --name vr2 --privileged vrnetlab/vr-vmx:18.2R1.9
sudo docker run -d --name vr3 --privileged vrnetlab/vr-vmx:18.2R1.9
sudo docker run -d --name vr4 --privileged vrnetlab/vr-vmx:18.2R1.9
sudo docker run -d --name vr5 --privileged vrnetlab/vr-vmx:18.2R1.9

sudo docker run -d --privileged --name vr-xcon --link vr1 --link vr2 --link vr3 --link vr4 --link vr5 vrnetlab/vr-xcon --p2p vr1/1--vr2/2 --p2p vr2/1--vr3/2 --p2p vr3/1--vr1/2 --p2p vr1/3--vr5/1


https://www.juniper.net/documentation/us/en/software/junos/routing-policy/topics/example/policy-prefix-list.html#configuration449__policy-prefix-list-st


https://www.juniper.net/documentation/us/en/software/junos/junos-getting-started/topics/task/junos-software-router-hostname-configuring.html


sudo docker run -d --privileged --name vr-xcon2 --link vr4 --link vr5 vrnetlab/vr-xcon --p2p vr4/1--vr5/1


                       _____ cisco ____
juniper ____ cisco___ /                juniper
                      \_____ cisco ____/






-----------------

vrnetlab@re0# show 
## Last changed: 2024-08-12 18:11:39 UTC
version 18.2R1.9;
groups {
    re0 {
        system {
            host-name re0;
        }
        interfaces {
            fxp0 {
                unit 0 {
                    family inet {
                        address 10.0.0.15/24;
                    }
                }
            }
        }
    }
    re1 {
        system {
            host-name re1;
        }
        interfaces {
            fxp0 {
                unit 0 {
                    family inet {
                        address 10.0.0.16/24;
                    }
                }
            }
        }
    }
}
apply-groups [ re0 re1 ];
system {
    login {
        user vrnetlab {
            uid 2000;
            class super-user;
            authentication {
                encrypted-password "$6$CDmzGe/d$g43HmhI3FA.21JCYppnTg1h4q/JO4DOHSICLhhavqBem5zUTgKEcg5m9tBG1Ik6qmfb7L3v.wgj4/DkfgZejO0"; ## SECRET-DATA
            }
        }
    }
    root-authentication {               
        encrypted-password "$6$vOte4zs5$j1X3fElYvJSt8VPNXx2KzRNrZIkp9CeRX83/W4wQo5K4Tl/MHZeMcvbymEzm9/2ya3S4hU993YDSLY26ROGnW/"; ## SECRET-DATA
    }
    services {
        ssh;
        extension-service {
            request-response {
                grpc {
                    clear-text {
                        port 57400;
                    }
                }
            }
        }
        netconf {
            ssh;
        }
    }
    syslog {
        user * {
            any emergency;
        }
        file messages {
            any notice;
            authorization info;
        }
        file interactive-commands {
            interactive-commands any;
        }
    }
}
chassis {
    fpc 0 {
        pic 0 {
            number-of-ports 96;
        }
    }
}
interfaces {
    ge-0/0/0 {
        unit 0 {
            family inet {
                address 1.1.1.2/24;
            }                           
        }
    }
    lo0 {
        unit 0 {
            family inet {
                address 2.2.2.2/32;
            }
        }
    }
}
routing-options {
    static {
        route 192.168.100.0/24 next-hop 2.2.2.2;
    }
    router-id 1.1.1.2;
    autonomous-system 100;
}
protocols {
    bgp {
        group ibgp-peers {
            type internal;
            export test;
            neighbor 1.1.1.1;
        }
    }
    ospf {
        area 0.0.0.0 {
            interface all;
            interface lo0.0 {
                passive;
            }
            interface fxp0.0 {
                disable;
            }
        }
    }
}
policy-options {
    policy-statement test {
        term 1 {
            from protocol ospf;
        }
        then accept;                    
    }
}

[edit]



------------------

vrnetlab@re0# show 
## Last changed: 2024-08-12 17:49:51 UTC
version 18.2R1.9;
groups {
    re0 {
        system {
            host-name re0;
        }
        interfaces {
            fxp0 {
                unit 0 {
                    family inet {
                        address 10.0.0.15/24;
                    }
                }
            }
        }
    }
    re1 {
        system {
            host-name re1;
        }
        interfaces {
            fxp0 {
                unit 0 {
                    family inet {
                        address 10.0.0.16/24;
                    }
                }
            }
        }
    }
}
apply-groups [ re0 re1 ];
system {
    login {
        user vrnetlab {
            uid 2000;
            class super-user;
            authentication {
                encrypted-password "$6$CDmzGe/d$g43HmhI3FA.21JCYppnTg1h4q/JO4DOHSICLhhavqBem5zUTgKEcg5m9tBG1Ik6qmfb7L3v.wgj4/DkfgZejO0"; ## SECRET-DATA
            }
        }
    }
    root-authentication {               
        encrypted-password "$6$vOte4zs5$j1X3fElYvJSt8VPNXx2KzRNrZIkp9CeRX83/W4wQo5K4Tl/MHZeMcvbymEzm9/2ya3S4hU993YDSLY26ROGnW/"; ## SECRET-DATA
    }
    services {
        ssh;
        extension-service {
            request-response {
                grpc {
                    clear-text {
                        port 57400;
                    }
                }
            }
        }
        netconf {
            ssh;
        }
    }
    syslog {
        user * {
            any emergency;
        }
        file messages {
            any notice;
            authorization info;
        }
        file interactive-commands {
            interactive-commands any;
        }
    }
}
chassis {
    fpc 0 {
        pic 0 {
            number-of-ports 96;
        }
    }
}
interfaces {
    ge-0/0/0 {
        unit 0 {
            family inet {
                address 1.1.1.1/24;
            }                           
        }
    }
}
routing-options {
    router-id 1.1.1.1;
    autonomous-system 100;
}
protocols {
    bgp {
        group ibgp-peers {
            type internal;
            neighbor 1.1.1.2;
        }
    }
}
