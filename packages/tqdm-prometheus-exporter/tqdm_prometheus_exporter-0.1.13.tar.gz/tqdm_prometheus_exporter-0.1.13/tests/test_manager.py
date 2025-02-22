'''
unittest bucket manager
'''
import io
from unittest import TestCase
from tqdmpromproxy.manager import BucketManager
from tqdmpromproxy.snapshot import TqdmSnapshot


class TestBucketManager(TestCase):

    def setUp(self):
        self.manager = BucketManager()

    def test_update_creates_new_bucket(self):
        snapshot = TqdmSnapshot(bar_id=0, desc="test", total=100, n=50)
        self.manager.update(snapshot)
        self.assertEqual(len(self.manager.buckets), 1)

    def test_update_reuses_matching_bucket(self):
        snapshot1 = TqdmSnapshot(bar_id=0, desc="test", total=100, n=50)
        snapshot2 = TqdmSnapshot(bar_id=0, desc="test", total=100, n=75)

        self.manager.update(snapshot1)
        self.manager.update(snapshot2)

        self.assertEqual(len(self.manager.buckets), 1)

    def test_dump_content_writes_metrics(self):
        snapshot = TqdmSnapshot(0, "test", total=100, n=50)
        self.manager.update(snapshot)

        output = io.StringIO()
        self.manager.export(output)

        lines = output.getvalue().split("\n")
        self.assertTrue(any("test" in line for line in lines))
        self.assertTrue(any("50" in line for line in lines))

    def test_metric_name_override(self):
        snapshot = TqdmSnapshot(0, "test", total=100, n=50)
        self.manager.update(snapshot)
        self.manager.metric_formatter = lambda desc, unit, attr: f"forced_name_{unit}_{attr}"

        output = io.StringIO()
        self.manager.export(output)

        lines = output.getvalue().split("\n")
        self.assertTrue(any("forced_name_" in line for line in lines))