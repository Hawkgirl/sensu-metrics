from pynvml import *

import time
import socket

now = time.time()
hostname=socket.gethostname()

nvmlInit()


deviceCount = nvmlDeviceGetCount()
for i in range(deviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)
        tasks = nvmlDeviceGetComputeRunningProcesses(handle)
        info = nvmlDeviceGetUtilizationRates(handle)

        print "%s.gpu%d.gpu_percent %d %d" % (hostname, i, info.gpu, now)
        print "%s.gpu%d.gpumem_percent %d %d" % (hostname, i, info.memory, now)
        print "%s.gpu%d.task_count %d %d" % (hostname, i, len(tasks), now)

nvmlShutdown()
