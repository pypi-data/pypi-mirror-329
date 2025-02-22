from itertools import repeat
from multiprocessing import Queue
from time import sleep

from tqdm import tqdm as native_tqdm

from tqdmpromproxy.internal.executor import TaskCountingPoolExecutor
from tqdmpromproxy.proxy import TqdmPrometheusProxy

task_names = ["Upload", "Download", "Gzip", "Bzip", "Tar", "Untar", "Copy", "Move", "Delete", "List"]

def generator_init(lock, queue):
    native_tqdm.set_lock(lock)

    global tqdm_slot
    # if this fails the queue is empty and we should exit
    tqdm_slot = queue.get(timeout=1)

def create_threadpool(size:int=2, base: int = 0):
        offsets = Queue()

        for r in range(base, base+size):
            offsets.put(r)

        pool = TaskCountingPoolExecutor(size,
                                    initializer=generator_init,
                                    initargs=(native_tqdm.get_lock(), offsets))
    
        return pool


def queue_tasks(pool:TaskCountingPoolExecutor, quanity:int, proxy:TqdmPrometheusProxy):

    for q in range(quanity):
        pool.submit(_off_thread_task,name= task_names[q % len(task_names)],duration=5, step=0.5, proxy= proxy)

def _off_thread_task(name:str, duration:int = 5, step:float = 0.2, proxy:TqdmPrometheusProxy=None):

    with proxy.tqdm(total=duration, desc=name, position=tqdm_slot, leave=False) as pbar:
        for _ in range(int(duration / step)):
            sleep(step)
            pbar.update(round(step,2))