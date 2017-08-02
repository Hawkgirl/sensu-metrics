#! /usr/bin/python
import docker
import socket
from toolz import countby
from collections import defaultdict

import time


def calculate_cpu_percent(stats):
    cpu_count = len(stats["cpu_stats"]["cpu_usage"]["percpu_usage"])
    cpu_percent = 0.0
    cpu_delta = float(stats["cpu_stats"]["cpu_usage"]["total_usage"]) - \
                float(stats["precpu_stats"]["cpu_usage"]["total_usage"])
    system_delta = float(stats["cpu_stats"]["system_cpu_usage"]) - \
                   float(stats["precpu_stats"]["system_cpu_usage"])
    if system_delta > 0.0:
        cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
    return cpu_percent

hostname = socket.gethostname()
docker_obj = docker.from_env()

base_metric_str = 'docker.' + hostname + '.'
containers_metric_str = base_metric_str + 'containers.'
list_images = docker_obj.images()
print base_metric_str + 'images.count',len(list_images), int(time.time())

list_containers =  docker_obj.containers(all=True)
print containers_metric_str + 'count',len(list_containers), int(time.time())

group_by_state = countby(lambda x:x['State'], list_containers)
default_state_dic = defaultdict(int, group_by_state)
print containers_metric_str + 'state.exited', default_state_dic['exited'], int(time.time())
print containers_metric_str + 'state.running', default_state_dic['running'], int(time.time())
print containers_metric_str + 'state.paused', default_state_dic['paused'], int(time.time())
print containers_metric_str + 'state.restarting', default_state_dic['restarting'], int(time.time())

for container in list_containers:
	if container['State'] != 'running':
		continue
	container_metric_str = base_metric_str + 'container.' + container['Names'][0] + '.'
	stats = docker_obj.stats(container['Id'], stream=False)
	cpu_percentage = calculate_cpu_percent(stats)
	
	print container_metric_str + 'cpu_usage',cpu_percentage, int(time.time())
	print container_metric_str + 'mem_usage', stats['memory_stats']['usage'], int(time.time())
	print container_metric_str + 'mem_max', stats['memory_stats']['limit'], int(time.time())
	print container_metric_str + 'net_rx', stats['networks']['eth0']['rx_bytes'], int(time.time())
	print container_metric_str + 'net_tx', stats['networks']['eth0']['tx_bytes'], int(time.time())

	reads = writes = 0
	io_dict = stats['blkio_stats']['io_service_bytes_recursive']
	if io_dict:
		for data in io_dict:
			if data['op'] == 'Read':
				reads += data['value']
			elif data['op'] == 'Write':
				writes += data['value']

	print container_metric_str + 'disk_reads', reads, int(time.time())
	print container_metric_str + 'disk_write', writes, int(time.time())
	print container_metric_str + 'process_count', stats['pids_stats']['current'], int(time.time())
