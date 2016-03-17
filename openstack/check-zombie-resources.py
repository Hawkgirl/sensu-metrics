#!/usr/bin/python
from ext_cloud import get_ext_cloud
import sys

import warnings
warnings.filterwarnings("ignore")

cloud_obj =  get_ext_cloud("openstack")

resources = cloud_obj.resources.list_zombie_resources()

from  toolz import countby
dic = countby(lambda x: x.resource_type, resources)
if len(dic) is 0:
	sys.exit(0)
print dic
sys.exit(1)

