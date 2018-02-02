# iperf benchmark playbook

## Requirements

* [Ansible](http://docs.ansible.com/ansible/latest/intro.html)
* IP connectivity between hosts
* SSH access to nodes from host that will be running ansible

## Overview

This playbook, and subsquent role can be used to perform iperf benchmark testing on a given set of hosts.

All communications patterns are supported :

* many-to-many
* one-to-many
* many-to-one
* one-to-one

This is dependent on which nodes you assigned to which `[host groups]` defined in the `hosts` file.

### Host definition

Within the `hosts` file in this directory there are two groups defined, `iperf_servers` and `iperf_clients`, the 
nameing of these groups is meant to stay in line with the typical iperf nomenclature.

Define which hosts you would like to run iperf in server mode `-s`, along with which hosts you would like to run client
connectivity tests.

### Play variables

#### `test_count`

There is currently only a single variable for definition within this role. This variable is located in the `var/` subdirectory.

The variable `test_count` will control how many concurrent tests you would like to run between nodes. This variable will help
when utilizing LAG (bond) interfaces when testing connectivity between multiple hosts within a network.



