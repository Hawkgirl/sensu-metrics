#!/usr/bin/python
from ext_cloud import get_ext_cloud
import sys

import warnings
warnings.filterwarnings("ignore")

#cloud_obj =  get_ext_cloud("openstack",username='admin', password='zEPre25+UF_ba-wEp2e?', tenant_name='admin', auth_url='https://vcaas-prod.vcaas-ibm.com:5000/v2.0', cacert='/opt/stack/ssl/openstack.crt')
cloud_obj =  get_ext_cloud("openstack")

resources = cloud_obj.resources.list_zombie_resources()

from  toolz import countby
dic = countby(lambda x: x.resource_type, resources)
if len(dic) is 0:
	sys.exit(0)
print dic
sys.exit(1)
'''
print len(instances)
for instance in instances:
	print instance.id, instance.resource_type
'''

