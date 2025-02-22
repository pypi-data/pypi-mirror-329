'''
unittest bucket manager
'''
import io
from time import sleep
import unittest

from tqdmpromproxy.manager import BucketManager
from tqdmpromproxy.snapshot import TqdmSnapshot


class TestBucketManagerIntegration(unittest.TestCase):

    def setUp(self):
        self.manager = BucketManager()

    def test_same_items_updates_bucket(self):
        '''
        one independent bars
        '''
        max_it = 100
        for i in range(max_it):
            snapshot = TqdmSnapshot(bar_id=0, desc="test", total=max_it, n=i)
            self.manager.update(snapshot) 

        self.assertBucketCountIs(1)
        self.assertBucketBreakdownIs([1])

    def test_dual_items_separate_bucket(self):
        '''
        two independent bars
        '''
        max_it = 100
        for i in range(max_it):
            self.manager.update(TqdmSnapshot(bar_id=0, desc="test", total=max_it, n=i+1))
            self.manager.update(TqdmSnapshot(bar_id=1, desc="diff", total=max_it, n=i+1))  

        self.assertBucketCountIs(2)
        self.assertBucketBreakdownIs([1,1])
        
        result = self._get_prometheus_result_as_str()
        key = self._key

        for bucket in self.manager.buckets:
            self.assertInPrometheusResult(result, {
                key('active', 'count', bucket): 1,   
                key('finished', 'count', bucket): 0, 
                key('completed', 'None', bucket): 100,
                key('total', 'None', bucket): 100,
            })

    def test_dual_items_updates_bucket(self):
        '''
        two bars with the same metric that should be aggregated
        '''
        max_it = 100
        for i in range(max_it):
            self.manager.update(TqdmSnapshot(bar_id=0, desc="upload", total=max_it, n=i+1, unit="items"))
            self.manager.update(TqdmSnapshot(bar_id=1, desc="upload", total=max_it, n=i+1, unit="items")) 

        self.assertBucketCountIs(1)
        self.assertBucketBreakdownIs([2])
        
        result = self._get_prometheus_result_as_str()
        key = self._key
 
        self.assertInPrometheusResult(result, {
            key('active', 'count'): 2,   
            key('finished', 'count'): 0, 
            key('completed', 'items'): 200,
            key('total', 'items'): 200,
        })

    def test_single_items_different_position_updates_bucket(self):
        '''
        two bars with the same metric that should be aggregated
        '''
        max_it = 100
        for i in range(max_it):
            self.manager.update(TqdmSnapshot(bar_id=2, desc="upload", total=max_it, n=i+1, unit="items")) 

        self.assertBucketCountIs(1)
        self.assertBucketBreakdownIs([1])
        
        result = self._get_prometheus_result_as_str()
        key = self._key
 
        for bucket in self.manager.buckets:
            self.assertInPrometheusResult(result, {
                key('active', 'count', bucket): 1,   
                key('finished', 'count', bucket): 0, 
                key('completed', 'items', bucket): 100,
                key('total', 'items', bucket): 100,
            })

    def test_long_second_update(self):
        duration_s = 5
        max_items = 100

        for item in range(max_items):
            self.manager.update(TqdmSnapshot(bar_id=0, desc="upload", total=max_items, n=item+1, unit="items"))

            sleep(duration_s/float(max_items))

        self.assertBucketCountIs(1)
        self.assertBucketBreakdownIs([1])
        
        result = self._get_prometheus_result_as_str()
        key = self._key
 
        self.assertInPrometheusResult(result, {
            key('active', 'count'): 1,   
            key('finished', 'count'): 0, 
            key('completed', 'items'): 100,
            key('total', 'items'): 100,
        })


    def assertInPrometheusResult(self, result:str, expected:dict[str, int]):
        for ex_key, ex_val in expected.items():
            self.assertIn(f"{ex_key} {ex_val}", result, f"Expected item '{ex_key} {ex_val}' was not in \n---\n{result}\n---")

    def _key(self, attr, scale=None, bucket=None,):
        _bucket = bucket or self.manager.buckets[0]
        _scale = str(scale or _bucket.item_scale)

        return f"{_bucket.bucket_key}_{attr}_{_scale}"
    
    def _get_prometheus_result_as_str(self, manager: BucketManager = None):

        _manager = manager or self.manager

        _buf = io.StringIO()
        _manager.export(_buf)
        return _buf.getvalue()
    
    def assertBucketCountIs(self, expected:int):
        self.assertEqual(len(self.manager.buckets), expected, 
                         f"Expected {expected} buckets, but got {len(self.manager.buckets)}")
       

    def assertBucketBreakdownIs(self, expected: list[int]):
        instance_breakdown = [len(i.known_instances) for i in self.manager.buckets]
        self.assertEqual(instance_breakdown, expected, 
                         f"Expected {expected} instances in each bucket, but got {instance_breakdown}")

if __name__ == '__main__':
    unittest.main()
