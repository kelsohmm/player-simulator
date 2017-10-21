#!/usr/bin/python
import logging
import sys
import psutil

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%H:%M:%S',  level=logging.DEBUG)
last_2_args = sys.argv[len(sys.argv)-2:]
[controller_pid, vm_pid] = last_2_args

error_message = None
try:
    controller_process = psutil.Process(int(controller_pid))
    vm_process = psutil.Process(int(vm_pid))

    logging.info("VM pid %s supervisor started for controller pid %s", vm_pid, controller_pid)
    controller_process.wait()

    logging.info("Controller process finished, killing VM")
    vm_process.kill()

except TypeError:
    error_message = "TypeError on cast to int - invalid pids, controller_pid: " + controller_pid + ' vm_pid: ' + vm_pid
except psutil.NoSuchProcess:
    error_message = "NoSuchProcess - invalid pids, controller_pid: " + controller_pid + ' vm_pid: ' + vm_pid
finally:
    if isinstance(error_message, str):
        file = open('logs/supervisor_' + controller_pid + '_' + vm_pid + '.err', 'w')
        file.write(error_message)

