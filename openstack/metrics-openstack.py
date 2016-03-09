#!/usr/bin/python
from ext_cloud import get_ext_cloud

import warnings
warnings.filterwarnings("ignore")

cloud_obj =  get_ext_cloud("openstack")

metrics = cloud_obj.stats.list_metrics()
for metric in metrics:
	print metric.name,'\t',metric.value,'\t',metric.timestamp
