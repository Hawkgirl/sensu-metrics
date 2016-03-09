#!/usr/bin/python
from ext_cloud import get_ext_cloud
from ext_cloud.BaseCloud.BaseCompute.BaseInstance import STATE

import warnings
warnings.filterwarnings("ignore")

import sys
cloud_obj =  get_ext_cloud("openstack")

services = cloud_obj.services.list_compute_services()

down = 0
down_str = ""
disabled = 0
disabled_str = ""
for service in services:
	if service.state == 'down':
		down += 1
		down_str += '[' + service.name + ':' + service.host + '] '

	if service.status == 'disabled':
		disabled += 1
		disabled_str += '[' + service.name + ':' + service.host + '] '
		
if not down and not disabled:
	sys.exit(0)

msg = ""
if down:
	msg += '{} compute service(s) down.[service name:host] {}'.format(down, down_str)

if disabled:
	msg += '{} compute service(s) disabled.[service name:host] {}'.format(disabled, disabled_str)

print msg
sys.exit(1)
