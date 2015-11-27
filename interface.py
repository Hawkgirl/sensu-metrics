#! /usr/bin/python
import ethtool
import socket
import re
import time

SKIP_DRIVERS = ('tun', 'openvswitch', 'bridge', 'veth', 'vxlan')
host_name = socket.gethostname()
time_now = int(time.time())
f = open("/proc/net/dev", "r");
data = f.read()
f.close()
 
r = re.compile("[:\s]+")
 
lines = re.split("[\r\n]+", data)
active_devices = ethtool.get_active_devices()
for line in lines[2:]:
	columns = r.split(line.lstrip())

	if len(columns) < 10:
            continue
	iface_name = columns[0]	
	# loopback devices has no driver and gives IOError, skip them
	try:	
		driver = ethtool.get_module(iface_name)
	except IOError: continue


	if driver in SKIP_DRIVERS:
		continue	

	if iface_name not in active_devices:
		continue


 	print '{}\t{}\t{}'.format(host_name + '.interface.' + iface_name + '.rx_bytes', columns[1], time_now)
 	print '{}\t{}\t{}'.format(host_name + '.interface.' + iface_name + '.rx_errors', columns[3], time_now)
 	print '{}\t{}\t{}'.format(host_name + '.interface.' + iface_name + '.tx_bytes', columns[9], time_now)
 	print '{}\t{}\t{}'.format(host_name + '.interface.' + iface_name + '.tx_errors', columns[11], time_now)

