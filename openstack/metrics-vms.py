#!/usr/bin/python
from ext_cloud import get_ext_cloud
import datetime

import warnings
warnings.filterwarnings("ignore")

cloud_obj =  get_ext_cloud("openstack")

#instance = cloud_obj.compute.get_instance_by_id('337b0305-1128-4377-88bf-a4c8a2da58ec')
#metrics = instance.list_usage_metrics()
metrics = cloud_obj.compute.list_vm_usage_metrics()
for metric in metrics:
        print metric.name,'\t',metric.value,'\t',metric.timestamp
