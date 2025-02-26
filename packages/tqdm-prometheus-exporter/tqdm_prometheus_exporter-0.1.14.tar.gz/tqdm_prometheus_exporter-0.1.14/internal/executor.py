'''Executor class that tracks the number of completed tasks'''
from concurrent.futures import ProcessPoolExecutor

# pylint: disable=missing-function-docstring


class TaskCountingExecutor():
    '''Pool executor that tracks the number of completed tasks'''

    def __init__(self, *args, executor=ProcessPoolExecutor, **kwargs):
        self._pool = executor(*args, **kwargs)
        self._completed_tasks = 0
        self._callback = None

    def set_callback(self, callback):
        self._callback = callback

    def submit(self, *args, **kwargs):
        future = self._pool.submit(*args, **kwargs)

        future.add_done_callback(self._worker_is_done)
        return future

    def _worker_is_done(self, _):
        self._completed_tasks += 1

        if self._callback:
            self._callback()

    def get_completed_count(self):
        return self._completed_tasks
