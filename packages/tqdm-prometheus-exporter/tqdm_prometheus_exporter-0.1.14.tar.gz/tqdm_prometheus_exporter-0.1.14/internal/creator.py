'''Collection of functions for testing and validation'''
from multiprocessing import Queue
from time import sleep

from tqdm import tqdm as native_tqdm

from internal.executor import TaskCountingExecutor
from tqdmpromproxy.proxy import TqdmPrometheusProxy

task_names = ["Upload", "Download", "Gzip", "Bzip",
              "Tar", "Untar", "Copy", "Move", "Delete", "List"]


def generator_init(lock, queue):
    '''Initialize the generator with a lock and a queue'''
    native_tqdm.set_lock(lock)

    global tqdm_slot  # pylint: disable=global-variable-undefined

    # if this fails the queue is empty and we should exit
    tqdm_slot = queue.get(timeout=1)


def create_threadpool(size: int = 2, base: int = 0):
    '''Create a thread pool with a given size and base tqdm position'''
    offsets = Queue()

    for r in range(base, base+size):
        offsets.put(r)

    pool = TaskCountingExecutor(size,
                                initializer=generator_init,
                                initargs=(native_tqdm.get_lock(), offsets))

    return pool


def queue_tasks(pool: TaskCountingExecutor, quanity: int, proxy: TqdmPrometheusProxy):
    '''Add a number of tasks to the pool'''

    for q in range(quanity):
        pool.submit(run_task, name=task_names[q % len(
            task_names)], duration=5, step=0.5, proxy=proxy)


def run_task(name: str, duration: int = 5, step: float = 0.2, proxy: TqdmPrometheusProxy = None):
    '''Create and run a tqdm instance with a given duration and step'''

    with proxy.tqdm(total=duration, desc=name, position=tqdm_slot, leave=False) as pbar:
        for _ in range(int(duration / step)):
            sleep(step)
            pbar.update(round(step, 2))
