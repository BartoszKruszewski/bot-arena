import subprocess
import threading
import queue
import time

from packages import BOTS_DIRECTORY
from packages.simulator.utils import get_run_command

class Bot:
    def __init__(self, file):
        file = BOTS_DIRECTORY + "/" + file
        self.process = subprocess.Popen(get_run_command(file), bufsize=1, shell=False, text=True,
                                        stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        self.in_queue = queue.Queue()
        self.out_queue = queue.Queue()
        self.threads = [
            threading.Thread(target=self._reader),
            threading.Thread(target=self._writer)
        ]
        for thread in self.threads:
            thread.setDaemon(True)
            thread.start()
        
        self.total_time = 0
        self.start_time = None

    def _reader(self):
        proc = self.process
        while proc.poll() is None:
            prompt = proc.stdout.readline()
            if self.start_time is not None:
                self.total_time += time.time() - self.start_time
                self.start_time = None
            self.in_queue.put(prompt)

    def _writer(self):
        proc = self.process
        stdin = proc.stdin
        while proc.poll() is None:
            try:
                prompt = self.out_queue.get(timeout=1)
                stdin.write(prompt)
                stdin.write('\n')
                stdin.flush()
                self.out_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error while writing to subprocess: {e}")
                break

    def get(self):
        try:
            info = self.in_queue.get(timeout=1)
            self.in_queue.task_done()
            return info.strip()
        except queue.Empty:
            return None
        except Exception as e:
            print(f"Error while reading from queue: {e}")
            return None

    def put(self, item, measure_time=False):
        if measure_time:
            assert self.start_time is None
            self.start_time = time.time()
        return self.out_queue.put(item)


    def kill(self):
        self.process.kill()
        for thread in self.threads:
            thread.join()
        # may not work






    