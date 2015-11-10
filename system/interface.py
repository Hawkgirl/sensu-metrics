import ethtool
import socket
import re
import time

SKIP_DRIVERS = ('tun', 'openvswitch')
host_name = socket.gethostname()
time_now = int(time.time())
f = open("/proc/net/dev", "r");
data = f.read()
f.close()
 
r = re.compile("[:\s]+")
 
lines = re.split("[\r\n]+", data)
for line in lines[2:]:
	columns = r.split(line)

	if len(columns) < 18:
            continue
	
	iface_name = columns[1]

	# loopback devices has no driver and gives IOError, skip them
	try:	
		driver = ethtool.get_module(iface_name)
	except IOError: continue

	if driver in SKIP_DRIVERS:
		continue	

 	print '{}\t{}\t{}'.format(host_name + '.interface.' + iface_name + '.rx_bytes', columns[2], time_now)
 	print '{}\t{}\t{}'.format(host_name + '.interface.' + iface_name + '.rx_errors', columns[4], time_now)
 	print '{}\t{}\t{}'.format(host_name + '.interface.' + iface_name + '.tx_bytes', columns[10], time_now)
 	print '{}\t{}\t{}'.format(host_name + '.interface.' + iface_name + '.tx_errors', columns[12], time_now)

