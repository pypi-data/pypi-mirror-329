'''
Entry point 
Owns the pool of monitors and the http server

'''
import multiprocessing
from queue import Queue
from typing import Callable

from tqdm import tqdm as native_tqdm

from tqdmpromproxy.monitor import TqdmMonitor
from tqdmpromproxy.metric_server import AsyncMetricServer
from tqdmpromproxy.snapshot import TqdmSnapshot


class TqdmPrometheusProxy():
    '''Root of the proxy system'''

    def __init__(self, 
                 http_host='[::1]', http_port=3000, 
                 event_queue: Queue = None, 
                 metric_func: Callable[[str, str, str], str] = None,
                 bucket_func: Callable[[TqdmSnapshot], str] = None):
        '''
        Start a proxy to capture tqdm updates and expose them via a prometheus endpoint.
        '''
        self.tqdm_events = event_queue if event_queue else multiprocessing.Manager().Queue()

        self.http_server = AsyncMetricServer(
            self.tqdm_events, 
            http_host, http_port, 
            metric_func=metric_func,
            bucket_func=bucket_func)

        self.monitors: list[TqdmMonitor] = []

    def __getstate__(self):
        state = self.__dict__.copy()

        del state["http_server"]
        del state["monitors"]

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

        self.http_server = None
        self.monitors = []

    def tqdm(self, *args, **kwargs):
        '''Convienience method to create a tqdm instance and add it to the proxy'''
        instance = native_tqdm(*args, **kwargs)

        self.add(instance)

        return instance

    def add(self, tqdm):
        '''Add a new tqdm instance to the proxy'''
        monitor = TqdmMonitor(self.tqdm_events)
        monitor.add(tqdm)
        self.monitors.append(monitor)

        monitor.start()

    def start(self):
        self.http_server.start()

    def stop(self):
        for m in self.monitors:
            m.stop()
            
        for m in self.monitors:
            # print(f"Joining monitor@{m.discovered[0].desc}")
            m.worker.join()

        # print(f"monitors stopped")
        self.http_server.stop()
