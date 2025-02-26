'''
Group snapshots into user configurable buckets
'''
import logging
from threading import Thread
from time import sleep
from typing import Callable

import jsonpickle

from tqdmpromproxy.bucket import PrometheusBucket
from tqdmpromproxy.snapshot import TqdmSnapshot

# pylint: disable=missing-function-docstring

logger = logging.getLogger(__name__)


class BucketManager():
    '''Group snapshots into user configurable buckets'''

    def __init__(self,
                 metric_expr: Callable[[str, str, str], str] = None,
                 bucket_expr: Callable[[TqdmSnapshot], str] = None):

        self.buckets: list[PrometheusBucket] = []
        self.metric_formatter = metric_expr
        self.bucket_expr = bucket_expr

        self.pruner = Thread(target=self._prune, daemon=True,
                             name=f"{__class__.__name__}.pruner")

    def update(self, snapshot: TqdmSnapshot):
        '''Called asynchronously with snapshot events'''
        for b in self.buckets:
            if b.matches(snapshot):
                b.upsert(snapshot)
                return

        self.buckets.append(PrometheusBucket.from_instance(
            snapshot, bucket_expr=self.bucket_expr))

    def export(self, out_stream):
        logger.info("Begin bucket dump (%d) buckets", len(self.buckets))
        out_stream.write(f"# total categories {len(self.buckets)}")

        for b in self.buckets:
            logger.info("Dumping bucket %s -> %s", b.bucket_key, b)

            for line in b.to_prometheus_lines(self.metric_formatter):
                out_stream.write(line)
                out_stream.write("\n")

        logger.info("End bucket dump")

    def debug(self, out_stream):
        out_stream.write(jsonpickle.encode(self))

    def _prune(self):
        '''Periodically remove old metrics and empty buckets'''
        while True:
            for b in self.buckets:
                b.prune()

            # dont prune empty buckets, they should be retained
            # for persistent metrics

            sleep(15)
