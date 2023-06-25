vrnetlab - VR Network Lab
-------------------------

This repository is a fork of the project [vrnetlab/vrnetlab](https://github.com/vrnetlab/vrnetlab).

The fork has been created specifically for testing purposes.

The documentation provided in this fork only explains the parts that have been changed in any way from the upstream project. To get a general overview of the vrnetlab project itself, consider reading the docs of the upstream repo.

It is tested with:

 * Cisco CSR1000v 16.12.05 - csr1000v-universalk9.16.12.05-serial.qcow2
 * Cisco CSR1000v 17.03.04a - csr1000v-universalk9.17.03.04a-serial.qcow2
 * Cisco CSR1000v 17.03.05 - csr1000v-universalk9.17.03.05-serial.qcow2

[TIG stack](https://github.com/bvilajol/vrnetlab/blob/master/tig)
-------------------------

* [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) is a plugin-driven server agent for collecting and reporting metrics.  
* [InfluxDB](https://www.influxdata.com/time-series-platform/influxdb/) handles massive amounts of time-stamped information.  
* [Grafana](https://grafana.com/) is a trending open platform for analytics and monitoring.  

  
[Lab 01 - Introduction to NAPALM](https://github.com/bvilajol/vrnetlab/blob/master/lab/01_napalm_cisco)
-------------------------

* You need to build your own containers for the network devices. This repository has all the needed scripts and steps to do so.
* Simple eBGP scenario of three [Cisco CSR1000v](https://www.cisco.com/c/en/us/products/routers/cloud-services-router-1000v-series/index.html) nodes.
* [Python NAPALM](https://github.com/napalm-automation/napalm) is used to configure and validate the laboratory.
