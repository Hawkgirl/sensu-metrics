#! /usr/bin/python
import time
import subprocess
import collections
import socket

MAX_LINES = 20
line_count = 0
cpu_dic = collections.defaultdict(float)
mem_dic = collections.defaultdict(float)

time_now = int(time.time())
host_name = socket.gethostname()

output = subprocess.check_output(['ps', '-A', '--no-header',  '-o', 'user,%cpu,%mem', '--sort', '-%cpu'])
#print output
for line in output.splitlines():
	if line_count == MAX_LINES:
		break
	
	username, cpu_perc, mem_perc = line.split()

	if cpu_perc  != '0.0':
		cpu_dic[username] += float(cpu_perc)
	if mem_perc != '0.0':
		mem_dic[username] += float(mem_perc)

for item in cpu_dic:
	print "%s.user_percent.cpu.%s %f %d" % (host_name, item, cpu_dic[item], time_now)
for item in mem_dic:
	print "%s.user_percent.mem.%s %f %d" % (host_name, item, mem_dic[item], time_now)
