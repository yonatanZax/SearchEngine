from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import threading

'''
The rule of thumb is:

IO bound jobs -> multiprocessing.pool.ThreadPool
CPU bound jobs -> multiprocessing.Pool
Hybrid jobs -> depends on the workload, I usually prefer the multiprocessing.Pool due to the advantage process isolation brings

On Python 3 you might want to take a look at the concurrent.future.Executor pool implementations.
'''

class MyExecutors:

    def __init__(self):
        self.IOExecutor = ThreadPool(5)
        # self.UIExecutor = threading.main_thread()
        self.CPUExecutor = Pool(8)


class Singleton(MyExecutors):
  _instances = {}
  def __new__(class_, *args, **kwargs):
    if class_ not in class_._instances:
        class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
    return class_._instances[class_]

class MyClass(Singleton):
  pass

_instance = MyClass()


