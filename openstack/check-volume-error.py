#!/usr/bin/python
from ext_cloud import get_ext_cloud

import warnings
warnings.filterwarnings("ignore")

import sys
cloud_obj =  get_ext_cloud("openstack")

volumes = cloud_obj.volumes.get_volumes_by_error_state()

if len(volumes) == 0:
	sys.exit(0)

msg = '{} volume(s) in ERROR state.[volume id: name] '.format(len(volumes))

for volume in volumes:
	msg += '[' + volume.id + ':' + volume.name + '] '	
print msg
sys.exit(1)
