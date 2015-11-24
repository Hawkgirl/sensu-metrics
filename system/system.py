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

print "%s.load_avg.one %f %d" % (hostname,float(one), now)
print "%s.load_avg.five %f %d" % (hostname,float(five), now)
print "%s.load_avg.fifteen %f %d" % (hostname,float(fifteen), now)

#uptime stats
with open('/proc/uptime', 'r') as f:
    uptime_seconds, idle_seconds = f.readline().split()

idle_seconds = float(idle_seconds)/cpu_count

print "%s.uptime %f %d" % (hostname,float(uptime_seconds), now)
print "%s.idletime %f %d" % (hostname,idle_seconds, now)

#memory stats
mem_stats =psutil.virtual_memory()
print "%s.memory.total %d %d" % (hostname,mem_stats.total, now)
print "%s.memory.used %d %d" % (hostname,mem_stats.used, now)
print "%s.memory.free %d %d" % (hostname,mem_stats.free, now)
print "%s.memory.cached %d %d" % (hostname,mem_stats.cached, now)


#process stats
proc_stats = psutil.get_process_list()
proc_dict=collections.defaultdict(int, toolz.countby(lambda x:x.status, proc_stats))

print "%s.process.total %d %d" % (hostname,len(proc_stats), now)
print "%s.process.running %d %d" % (hostname,proc_dict['running'], now)
print "%s.process.sleeping %d %d" % (hostname,proc_dict['sleeping'], now)
print "%s.process.stopped %d %d" % (hostname,proc_dict['stopped'], now)


#disk stats
disk_stats = psutil.disk_io_counters(perdisk=True)
for key in disk_stats:
	print "%s.disk.%s.reads %d %d" % (hostname,key,disk_stats[key].read_count, now)
	print "%s.disk.%s.writes %d %d" % (hostname,key,disk_stats[key].write_count, now)
