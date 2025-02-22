
from io import StringIO
from time import sleep
import unittest

from tqdmpromproxy.proxy import TqdmPrometheusProxy


class ProxyIntegrationTest(unittest.TestCase):
    def test_export(self):
        try:
            proxy = TqdmPrometheusProxy()
            proxy.start()

            instances = [proxy.tqdm(i, desc=f'Item#{i}', total=100, position=i)
                         for i in range(10)]

            counter = 0
            for i in instances:
                i.update(counter*10)
                counter += 1

            def test():
                _buf = StringIO()
                proxy.http_server.bucketer.export(_buf)
                buf = _buf.getvalue()

                return 'Item#0' in buf, f"Wanted Item#0 in '{buf}'"

            self._retryable_assertion(test)
        finally:
            proxy.stop()


    def test_long_task_not_duplicated(self):
        try:
            proxy = TqdmPrometheusProxy()
            proxy.start()

            duration_s = 30
            total = 100

            for i in proxy.tqdm(range(total), desc=f'LongItem'):
                sleep(duration_s/float(total))

    
            _buf = StringIO()
            proxy.http_server.bucketer.export(_buf)
            buf = _buf.getvalue()
            # for bucket in self.manager.buckets:
            #     self.assertInPrometheusResult(result, {
            #         key('active', 'count', bucket): 1,   
            #         key('finished', 'count', bucket): 0, 
            #         key('completed', 'items', bucket): 100,
            #         key('total', 'items', bucket): 100,
            #     })

            self.assertIn('LongItem_active_count 1', buf, f"Wanted single instance in \n---\n'{buf}'\n---")
        finally:
            proxy.stop()

    def _retryable_assertion(self, test: callable, max_wait=10.0):
        delay = 0.2
        assertion = False
        while not assertion:
            assertion, message = test()
            if not assertion:
                delay *= 2
                if delay > max_wait:
                    break

                print(
                    f"Assertion failed. Recieved: {message}")
                sleep(delay)

        return self.assertTrue(assertion, message)
