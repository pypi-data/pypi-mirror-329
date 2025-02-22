

from io import BytesIO
import multiprocessing

import unittest
import pickle

from tqdmpromproxy import TqdmPrometheusProxy

class TestPickle(unittest.TestCase):
    def setUp(self):
        q = multiprocessing.Manager().Queue()
        
        self.proxy = TqdmPrometheusProxy(event_queue=q)
        self.proxy.start()
  
    def test_pickle(self):
        data = BytesIO()
        pickle.dump(self.proxy, data)

        self.assertGreater(len(data.getvalue()), 0)
    
    def tearDown(self):
        self.proxy.stop()
