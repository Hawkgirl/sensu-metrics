#! /usr/bin/python

import multiprocessing
import socket
import time
import psutil
import toolz
import collections

now = time.time()
hostname=socket.gethostname()

#cpu stats
cpu_count=multiprocessing.cpu_count()
print "%s.cpu.count %d %d" % (hostname,cpu_count, now)

#load avg
with open('/proc/loadavg', 'r') as f:
    one, five, fifteen = f.readline().split()[:3]

print "%s.cpu.load_avg.one %f %d" % (hostname,float(one), now)
print "%s.cpu.load_avg.five %f %d" % (hostname,float(five), now)
print "%s.cpu.load_avg.fifteen %f %d" % (hostname,float(fifteen), now)

#uptime stats
with open('/proc/uptime', 'r') as f:
    uptime_seconds, idle_seconds = f.readline().split()

idle_seconds = float(idle_seconds)/cpu_count

print "%s.cpu.uptime %f %d" % (hostname,float(uptime_seconds), now)
print "%s.cpu.idletime %f %d" % (hostname,idle_seconds, now)

#memory stats
mem_stats =psutil.virtual_memory()
print "%s.memory.total %d %d" % (hostname,mem_stats.total, now)
print "%s.memory.used %d %d" % (hostname,mem_stats.used, now)
print "%s.memory.free %d %d" % (hostname,mem_stats.free, now)
print "%s.memory.cached %d %d" % (hostname,mem_stats.cached, now)


#process stats
proc_stats = list(psutil.process_iter())
proc_dict=collections.defaultdict(int, toolz.countby(lambda x:x.status(), proc_stats))

print "%s.process.total %d %d" % (hostname,len(proc_stats), now)
print "%s.process.running %d %d" % (hostname,proc_dict['running'], now)
print "%s.process.sleeping %d %d" % (hostname,proc_dict['sleeping'], now)
print "%s.process.stopped %d %d" % (hostname,proc_dict['stopped'], now)


#disk stats
disk_stats = psutil.disk_io_counters(perdisk=True)
for key in disk_stats:
	#skip ram disks
	if key[:3] == 'ram': continue
	# skip cdrom devices
	if key[:2] == 'sr': continue
	print "%s.disk.%s.reads %d %d" % (hostname,key,disk_stats[key].read_count, now)
	print "%s.disk.%s.writes %d %d" % (hostname,key,disk_stats[key].write_count, now)

disk_partitions = psutil.disk_partitions()
for partition in disk_partitions:
	last_index = partition.device.rfind('/')
	dev_name = partition.device[last_index+1:]
	partition_usage = psutil.disk_usage(partition.mountpoint)
	print "%s.disk.%s.used %d %d" % (hostname, dev_name, partition_usage.used, now)
	print "%s.disk.%s.avail %d %d" % (hostname, dev_name, partition_usage.free, now)
	print "%s.disk.%s.capacity %d %d" % (hostname, dev_name, partition_usage.percent, now)

#network stats


connections = psutil.net_connections()
dic =  toolz.countby(lambda x: x.status, connections)
for item in dic:
	if item == 'NONE':
		continue
	print "%s.tcp.%s %d %d" % (hostname, item, dic[item], now)
