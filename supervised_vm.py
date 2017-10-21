import logging
import sys
import os

import psutil


class SupervisedVmDecorator:
    def __init__(self, vm):
        self.vm = vm
        self.supervisor_process = None

    def start(self):
        self.vm.start()
        self_pid = os.getpid()
        vm_pid = self.vm.machine.session_pid
        supervisor_pid = self._start_detached_process(self_pid, vm_pid)
        logging.info("Started supervisor for VM, self_pid: %d, vm_pid: %d, supervisor_pid: %d", self_pid , vm_pid , supervisor_pid)
        self.supervisor_process = psutil.Process(supervisor_pid)

    def _start_detached_process(self, self_pid, vm_pid):
        command = sys.executable or 'python'
        return os.spawnl(os.P_NOWAITO,  # mode - detached
                          command,  #command
                          command, 'vm_process_supervisor.py', str(self_pid), str(vm_pid))  # args

    def stop(self):
        self.supervisor_process.kill()
        self.supervisor_process = None
        return self.vm.stop()

    def keys_up(self, keys):
        return self.vm.keys_up(keys)

    def keys_down(self, keys):
        return self.vm.keys_down(keys)

    def take_screen_shot(self):
        return self.vm.take_screen_shot()