#!/usr/bin/python
import logging
import re
import sys
import psutil
from virtualbox import VirtualBox
from virtualbox.library import CleanupMode
from vm_host import VM_CLONE_TAG

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

    logging.info("Removing cloned vms")
    for machine in VirtualBox().machines:
        if machine.name.startswith(VM_CLONE_TAG):
            deleted_media = machine.unregister(CleanupMode.full)
            progress = machine.delete_config(deleted_media)
            progress.wait_for_completion()

except TypeError:
    error_message = "TypeError on cast to int - invalid pids, controller_pid: " + controller_pid + ' vm_pid: ' + vm_pid
except psutil.NoSuchProcess:
    error_message = "NoSuchProcess - invalid pids, controller_pid: " + controller_pid + ' vm_pid: ' + vm_pid
finally:
    if isinstance(error_message, str):
        file = open('logs/supervisor_' + controller_pid + '_' + vm_pid + '.err', 'w')
        file.write(error_message)

