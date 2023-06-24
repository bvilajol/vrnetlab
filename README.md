vrnetlab - VR Network Lab
-------------------------

This repository is a fork of the project [vrnetlab/vrnetlab](https://github.com/vrnetlab/vrnetlab).

The fork has been created specifically for testing purposes.

The documentation provided in this fork only explains the parts that have been changed in any way from the upstream project. To get a general overview of the vrnetlab project itself, consider reading the docs of the upstream repo.

It is tested with:

 * Cisco CSR1000v 16.12.05 - csr1000v-universalk9.16.12.05-serial.qcow2
 * Cisco CSR1000v 17.03.04a - csr1000v-universalk9.17.03.04a-serial.qcow2
 * Cisco CSR1000v 17.03.05 - csr1000v-universalk9.17.03.05-serial.qcow2

[Lab 01 - Introduction to NAPALM](https://github.com/bvilajol/vrnetlab/blob/master/lab/01_napalm_cisco/README.md)
-------------------------

* You need to build your own containers for the network devices.
* Simple eBGP scenario of three Cisco CSR1000v nodes.
* Python NAPALM is used to configure and validate the laboratory.
