import subprocess
import xmltodict
import time

time_now = int(time.time())

xml_str = subprocess.check_output(['crm_mon', '-Xr'])

tree = xmltodict.parse(xml_str)

totalnodes = upnodes = downnodes = 0
total_resources = running = failed = stopped = 0
for node in  tree['crm_mon']['nodes']['node']:
	totalnodes += 1
	if node['@online'] == 'true' : upnodes += 1
	
downnodes = totalnodes - upnodes


if tree['crm_mon']['resources'].has_key('resource'):
	for node in tree['crm_mon']['resources']['resource']:
		total_resources += 1
		if node['@failed']: failed += 1
		elif node['@active']: running += 1
		else: stopped += 1

#cluster resources
if tree['crm_mon']['resources'].has_key('clone'):
	for node in tree['crm_mon']['resources']['clone']:
		for item in node['resource']: 
			total_resources += 1
			if item['@failed'] == 'true' : failed += 1
			elif item['@active'] == 'true': running += 1
			else: stopped += 1

print '{}\t{}\t{}'.format('cluster.nodes_total', totalnodes, time_now)
print '{}\t{}\t{}'.format('cluster.nodes_up', upnodes, time_now)
print '{}\t{}\t{}'.format('cluster.nodes_down', downnodes, time_now)
			
print '{}\t{}\t{}'.format('cluster.total_resources', total_resources, time_now)
print '{}\t{}\t{}'.format('cluster.running_resources', running, time_now)
print '{}\t{}\t{}'.format('cluster.failed_resources', failed, time_now)
print '{}\t{}\t{}'.format('cluster.stopped_resources', stopped, time_now)
			
