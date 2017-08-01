#! /usr/bin/python
import docker
import socket

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
container_metric_str = base_metric_str + 'container.'
list_containers =  docker_obj.containers(all=True)
print container_metric_str + 'count',len(list_containers), int(time.time())

for container in list_containers:
	if container['State'] != 'running':
		continue
	stats = docker_obj.stats(container['Id'], stream=False)
	cpu = calculate_cpu_percent(stats)
	print cpu
