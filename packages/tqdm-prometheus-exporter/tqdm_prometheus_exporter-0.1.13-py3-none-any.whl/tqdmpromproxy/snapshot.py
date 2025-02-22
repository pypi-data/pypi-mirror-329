import datetime
from tqdm import tqdm as native_tqdm


class TqdmSnapshot():
    '''Snapshot of the state of a tqdm instance'''

    def __init__(self,
                 bar_id: int = None,
                 desc: str = None,
                 n: int = None,
                 total: int = None,
                 elapsed: int = None,
                 unit: str = None,
                 prefix: str = None,
                 unit_scale: str = None,
                 rate: float = None,
                 postfix: str = None,
                 unit_divisor: int = None,
                 initial: int = None,
                 time_ms: datetime.datetime = None,
                 **_kwargs
                 ):
        # from our wrapper
        self.bar_id = bar_id
        self.time_ms = time_ms

        # from tqdm api args
        self.completed = n
        self.total = total
        self.elapsed = elapsed
        self.prefix = prefix
        self.postfix = postfix
        self.unit = unit
        self.unit_scale = unit_scale
        self.unit_divisor = unit_divisor
        self.rate = rate
        self.initial = initial

        # from other/meta attributes
        self.desc = desc

    def __repr__(self):
        friendly = "Instance %s Bar = %s/%s, Finished %s Total %s (%s), throughput %s" % \
            (self.bar_id, self.prefix, self.desc, self.completed,
             self.total, self.unit, self.rate)

        return friendly

    def identity(self):
        '''Return a unique identifier for this instance.
        These properties should not change during the lifetime of the instance'''
        return str(self.bar_id) + str(self.desc.split(' ')[0])

    @classmethod
    def from_bar(cls, tqdm_bar: native_tqdm):
        if not isinstance(tqdm_bar, native_tqdm):
            raise ValueError("Expected a tqdm instance")

        return cls(bar_id=getattr(tqdm_bar, 'pos', 0),
                   desc=getattr(tqdm_bar, 'desc', ''),
                   time_ms=datetime.datetime.now(),
                   **tqdm_bar.format_dict)
