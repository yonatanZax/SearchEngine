from multiprocessing.dummy import Pool as ThreadPool
import threading

class MyExecutors:

    def __init__(self):
        print ("MyExecutors")
        self.IOExecutor = ThreadPool(3)
        # self.UIExecutor = threading.main_thread()
        self.CPUExecutor = ThreadPool(5)


class Singleton(MyExecutors):
  _instances = {}
  def __new__(class_, *args, **kwargs):
    if class_ not in class_._instances:
        class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
    return class_._instances[class_]

class MyClass(Singleton):
  pass

_instance = MyClass()


