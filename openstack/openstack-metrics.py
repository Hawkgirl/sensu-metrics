#! /usr/bin/python
from ext_cloud import get_ext_cloud

import warnings
warnings.filterwarnings("ignore")

cloud_obj =  get_ext_cloud("openstack",username='admin', password='sd33lejrfewsd43t4fds', tenant_name='admin', auth_url='https://vcaas.vcaas-ibm.com:5000/v2.0/', cacert='/opt/stack/ssl/openstack.crt')

metrics = cloud_obj.stats.list_metrics()
for metric in metrics:
	print metric.name,'\t',metric.value,'\t',metric.timestamp
