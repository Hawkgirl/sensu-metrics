#!/usr/bin/python
from __future__ import division
from ext_cloud import get_ext_cloud

import warnings
warnings.filterwarnings("ignore")

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cpu', default=70, type=int)
parser.add_argument('-m', '--memory', default=70, type=int)
parser.add_argument('-d', '--disk', default=70, type=int)
args = parser.parse_args()

import sys
cloud_obj =  get_ext_cloud("openstack")
hypervisors = cloud_obj.compute.list_hypervisors()

msg = ""
error = False
for hypervisor in hypervisors:
	current_cpu_usage = (hypervisor.vcpus_used/hypervisor.cpus * 100)
	if current_cpu_usage > args.cpu:
		error = True
		msg += 'Hypervisor:{} vcpus usage is {} %.'.format(hypervisor.name, current_cpu_usage)

	current_memory_usage = (hypervisor.memory_used_mb/hypervisor.memory_mb * 100)
	if current_memory_usage > args.memory:
		error = True
		msg += 'Hypervisor:{} memory  usage is at {} %.'.format(hypervisor.name, current_memory_usage)

	current_disk_usage = (hypervisor.disk_used_gb/hypervisor.disk_gb * 100)
	if current_disk_usage > args.disk:
		error = True
		msg += 'Hypervisor:{} disk usage is at {}%.'.format(hypervisor.name, current_disk_usage)



if error is False:
	sys.exit(0)

print msg
sys.exit(1)
