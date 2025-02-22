from typing import Callable
import jsonpickle
import logging

from tqdmpromproxy.bucket import PrometheusBucket
from tqdmpromproxy.snapshot import TqdmSnapshot


class BucketManager():
    def __init__(self, 
                 metric_expr:Callable[[str, str, str], str]=None,
                 bucket_expr:Callable[[TqdmSnapshot], str]=None):
        
        self.buckets: list[PrometheusBucket] = []
        self.metric_formatter = metric_expr
        self.bucket_expr = bucket_expr

    def update(self, snapshot: TqdmSnapshot):
        '''Called asynchronously with snapshot events'''
        for b in self.buckets:
            if b.matches(snapshot):
                b.upsert(snapshot)
                return

        self.buckets.append(PrometheusBucket.from_instance(snapshot, bucket_expr=self.bucket_expr))

    def export(self, out_stream):
        logging.info("Begin bucket dump (%d) buckets", len(self.buckets))
        out_stream.write(f"# total categories {len(self.buckets)}")

        for b in self.buckets:
            logging.info("Dumping bucket %s -> %s", b.bucket_key, b)

            for line in b.to_prometheus_lines(self.metric_formatter):
                out_stream.write(line)
                out_stream.write("\n")

        logging.info("End bucket dump")
    
    def debug(self, out_stream):
        str = jsonpickle.encode(self)

        out_stream.write(str)
