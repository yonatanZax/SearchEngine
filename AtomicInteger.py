"""An atomic, thread-safe incrementing counter."""

import threading
import MyExecutors

class AtomicCounter:

    def __init__(self, initial=0):
        """Initialize a new atomic counter to given initial value (default 0)."""
        self._value = initial
        self._lock = threading.Lock()

    def incrementAndGet(self, num=1):
        """Atomically increment the counter by num (default 1) and return the
        new value.
        """
        with self._lock:
            print(self._value)
            self._value += num
            return self._value

    def getAndIncrement(self, num=1):
        with self._lock:
            val = self._value
            self._value += num
            return val

    def get(self):
        with self._lock:
            return self._value


index = AtomicCounter()

for i in range(0,1000):
    MyExecutors._instance.IOExecutor.apply_async(index.incrementAndGet)










