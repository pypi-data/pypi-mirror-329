from io import StringIO
import logging
from queue import Empty, Queue
from threading import Thread, Event
from time import sleep
from typing import Callable

from bottle import WSGIRefServer, Bottle, route, response
import requests

from tqdmpromproxy.manager import BucketManager
from tqdmpromproxy.snapshot import TqdmSnapshot


class AsyncMetricServer:
    def __init__(self, queue: Queue[str],
                 http_listen_host: str = "[::1]", http_listen_port: int = 3000,
                 metric_func: Callable[[str, str, str], str] = None,
                 bucket_func: Callable[[TqdmSnapshot], str] = None):
        self.address = http_listen_host
        self.port = http_listen_port

        self.snapshot: str = "# No metric data has been collected yet. Check back soon\n"

        global TQDM_PROM_DATA
        TQDM_PROM_DATA = self.snapshot

        self.bottle = Bottle()
        self.bottle.route('/metrics')(self.metrics)
        self.bottle.route('/debug')(self.debug)
        self.bottle.route('/')(self.home)

        self.queue = queue
        self.poller = Thread(target=self.poll, daemon=True,
                             name=f"{__class__.__name__}.poller")
        self.wsgi = None

        self.wsgi = WSGIRefServer(
            app=self.bottle, host=self.address, port=self.port, quiet=True)
        self.wsgi.quiet = True
        self.server = Thread(
            target=self.wsgi.run, args=(self.bottle, ), daemon=True, name=f"{__class__.__name__}.server")

        self.bucketer = BucketManager(metric_func, bucket_func)
        self.additional_content: str = ''

        self._stop_event = Event()
        self.check_delay = 1

    def start(self):
        self.poller.start()
        self.server.start()

    def stop(self):
        self._stop_event.set()

        if not hasattr(self.wsgi, 'srv'):
            # dirty force lazy load
            try:
                requests.get(
                    f'http://{self.address}:{self.port}/shutdown', timeout=0.1)
            except requests.exceptions.ConnectTimeout:
                pass
            finally:
                pass

        if hasattr(self.wsgi, 'srv'):
            self.wsgi.srv.shutdown()
        self.server.join()

        # print("Stopped http server")

    def poll(self):
        last_found = 0
        while not self._stop_event.is_set():
            try:
                item = self.queue.get(0.1)
                self.bucketer.update(item)
                last_found = 0
                logging.info("Polled queue")

            except Empty:
                last_found += 1

                if last_found % 10 == 0:
                    logging.info("No tqdm updates recently")

            except EOFError:
                logging.info("Queue has been closed")
                break

            finally:
                pass

        # print("Stopped polling for snapshot events to publish")

    @route('/metrics')
    def metrics(self):
        response.content_type = 'text/plain; charset=utf-8'

        buff = StringIO()
        self.bucketer.export(buff)
        self.snapshot = buff.getvalue()

        logging.info("Metrics requested, returning %d bytes",
                     len(self.snapshot))

        return self.snapshot

    @route('/debug')
    def debug(self):
        response.content_type = 'application/json; charset=utf-8'

        buff = StringIO()
        self.bucketer.debug(buff)
        content = buff.getvalue()

        logging.info("Debug requested, returning %d bytes",
                     len(content))

        return content

    @route('/')
    def home(self):
        response.content_type = 'text/html; charset=utf-8'
        return '''
<html>
<head>
    <title>TQDM Prometheus Proxy</title>
</head>
<body>
    <h1>TQDM Prometheus Proxy</h1>
    <p>Metrics are available at <a href="/metrics">/metrics</a></p>
    <p>Debug information is available at <a href="/debug">/debug</a></p>
</body>
</html>
'''
