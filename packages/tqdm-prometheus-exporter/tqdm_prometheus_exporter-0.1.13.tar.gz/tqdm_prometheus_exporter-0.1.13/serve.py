from tqdmpromproxy.metric_server import AsyncMetricServer

from queue import Queue
import time
import logging


def main():
    q = Queue()
    s = AsyncMetricServer(q, 'localhost', 9000)

    s.start()

    try:

        for i in range(50):
            print('putting', i)
            q.put(f"test_metric {i}")
            time.sleep(.1)

    finally:
        s.stop()


if __name__ == '__main__':

    logging.basicConfig(filename="data/server.log",
                        filemode='w',
                        format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG
                        )

    main()
