from functools import reduce
import logging
from multiprocessing import RLock, freeze_support
from time import sleep

from tqdm import tqdm as native_tqdm

from tqdmpromproxy import TqdmPrometheusProxy
from tqdmpromproxy.internal.creator import _off_thread_task, create_threadpool,queue_tasks,task_names
from tqdmpromproxy.snapshot import TqdmSnapshot

def pool_task_formatter(bucket_key:str, prop:str, scale:str):
    taskname = bucket_key
    native_tqdm.write(f"Formatting metrics({bucket_key}|{prop})",)

    if reduce(lambda x, y: x or bucket_key.startswith(y), task_names, False):
        taskname = "NiceTask"

    return f"{taskname}_{prop}_{scale}"

def bucket_func(snapshot: TqdmSnapshot):
    taskname = snapshot.desc
    native_tqdm.write(f"Comparing bucket name({snapshot.bar_id}|{snapshot.desc})",)

    if reduce(lambda x, y: x or snapshot.desc.startswith(y), task_names, False):
        taskname = "AggregatedTask"

    return taskname

def main():
    # muliprocessing setup
    freeze_support()  # for Windows support
    native_tqdm.set_lock(RLock())  # for managing output contention

    global proxy
    proxy = TqdmPrometheusProxy(http_host='[::1]', metric_func=pool_task_formatter, bucket_func=bucket_func)
    proxy.start()

    threads = 3
    depth = 10
    pool = create_threadpool(threads, base=3) # use slots 3, 4, 5
    pool.submit(_off_thread_task, name="Encode", duration=60, step=0.2, proxy=proxy)
    queue_tasks(pool, threads * depth, proxy)
    
    try:
        for _ in proxy.tqdm(range(10), desc="Main Loop", position=0):
            for _ in proxy.tqdm(range(5), desc="Sub Loop", position=1, leave=False):
                for _ in proxy.tqdm(range(5), desc="Innnnner Loop", position=2, leave=False):
                    sleep(0.2)

    finally:
        proxy.stop()


if __name__ == "__main__":
    logging.basicConfig(filename="data/proxy.log",
                        filemode='w',
                        format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG
                        )
    main()
