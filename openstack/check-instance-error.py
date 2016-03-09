#!/usr/bin/python
from ext_cloud import get_ext_cloud

import warnings
warnings.filterwarnings("ignore")

import sys
cloud_obj =  get_ext_cloud("openstack")

instances = cloud_obj.compute.get_instances_by_error_state()

if len(instances) == 0:
	sys.exit(0)

msg = '{} instance(s) in ERROR state.[Instance id: name] '.format(len(instances))

for instance in instances:
	msg += '[' + instance.id + ':' + instance.name + '] '	
print msg
sys.exit(1)
