'''
Buckets hold groups of tqdm instances.
    They are used to aggregate like metrics over time.
    For example if there are two concurrent 'download' tqdms and a single
      'upload' tqdm these would be grouped into two buckets.
'''
from datetime import datetime
from typing import Callable

from tqdmpromproxy.snapshot import TqdmSnapshot


class PrometheusBucket:
    '''
    Collection of all grouped metrics
    '''

    def __init__(self, from_snapshot:TqdmSnapshot, retired_attrs: list[str], current_attrs: list[str], bucket_expr:Callable[[TqdmSnapshot], str]=None):

        self.current_attrs = list.copy(current_attrs)
        self.retired_attrs = list.copy(retired_attrs)

        self.aggregated = dict([(attr, 0) for attr in self.retired_attrs])

        self.known_instances: dict[str, TqdmSnapshot] = {}
        self.last_seen:dict[str, datetime] = {}
        self.retired_instances = 0
        self.bucket_expr = bucket_expr or self._default_bucket_expr

        self.bucket_key = self.bucket_expr(from_snapshot)
        self.item_scale = from_snapshot.unit

    def _default_bucket_expr(self, snap: TqdmSnapshot):
        '''Return a summary of the instance, so like instances can be aggregated
        For example all Gzip tasks, or all FileUpload tasks'''
        return snap.desc.replace(' ', '_')

    def matches(self, instance: TqdmSnapshot):
        return self.bucket_expr(instance) == self.bucket_key

    def upsert(self, instance: TqdmSnapshot, observation_time=datetime.now()):
        id = instance.identity()

        self.known_instances[id] = instance
        self.last_seen[id] = observation_time

    # pylint: disable=unnecessary-dunder-call
    def to_prometheus_lines(self, format:callable):
        '''Return the metrics as a prometheus string'''

        cleaner = lambda x: x.replace('/', '_').replace('-', '_').replace('.','_')
        yield f"# TQDM group {self.bucket_key} "
        yield f"{cleaner(self.bucket_key)}_active_count {len(self.known_instances)}"
        yield f"{cleaner(self.bucket_key)}_finished_count {self.retired_instances}"

        yield f"## Individual properties with scale {self.item_scale}"
        for prop in self.current_attrs:

            val = sum([instance.__getattribute__(prop) or 0
                      for _, instance in self.known_instances.items()])

            if prop in self.retired_attrs:
                val += self.aggregated[prop]

            prop = cleaner(format(self.bucket_key, prop, self.item_scale)) if format else cleaner(f"{self.bucket_key}_{prop}_{self.item_scale}")

            yield f"{prop} {val}"

    # pylint: disable=unnecessary-dunder-call
    def retire(self, instance_key: str):
        '''Move an instance from the active to the retired list'''

        id=instance_key
        snapshot = self.known_instances[id]

        if id in self.known_instances.keys():
            for prop in self.retired_attrs:
                self.aggregated[prop] += snapshot.__getattribute__(prop)

            del self.known_instances[id]

            self.retired_instances += 1

    def prune(self, max_age: int):
        '''Remove any instances that are no longer active'''
        to_remove = []
        for key, value in self.last_seen.items():
            if (datetime.now() - value).total_seconds() > max_age:
                to_remove.append(key)

        for key in to_remove:
            self.retire(key)

        return len(to_remove)

    @classmethod
    def from_instance(cls, snapshot: TqdmSnapshot, retired=None, current=None, bucket_expr:Callable[[TqdmSnapshot], str]=None):

        default_retired = ['completed']
        default_current = ['completed', 'total', 'rate']

        if retired is None:
            retired = default_retired

        if current is None:
            current = default_current

        bucket = cls(snapshot, retired, current, bucket_expr)
        bucket.upsert(snapshot)
        
        return bucket

