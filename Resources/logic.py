from multiprocessing import Process, Queue
from ctypes import windll, wintypes
from queue import Empty
from time import perf_counter_ns as ns

class poly():
    
    _shapes = None

    def __init__(self, shape: list) -> None:
        self._shapes = shape
    @property
    def shapes(self):
        return self._shapes
    @shapes.setter
    def shapes(self, shape: list) -> None:
        self._shapes = shape
    def relv(self, x,y,z):
        self.shapes = [round(self.shapes[0]+x,2),round(self.shapes[1]+y,2),round(self.shapes[2]+z,2)]

def physics(queue: Queue):
    kernel32 = windll.kernel32
    kernel32.timeBeginPeriod(wintypes.UINT(1))
    frametime = 19000000
    delta = 1000000000

    p = poly([1,1,1])

    while p.shapes[1] < 5:
        sleep = ns()
        while delta+(ns()-sleep) < frametime:
            kernel32.Sleep(1) 
        delta = ns()   
        p.relv(0.01,0.01,0.01)
        delta = ns() - delta
        queue.put(p.shapes)

    kernel32.timeEndPeriod(wintypes.UINT(1))
if __name__ == '__main__':
    q = Queue(2)
    p = Process(target=physics, args=(q,))
    p.start()
    kernel32 = windll.kernel32
    kernel32.timeBeginPeriod(wintypes.UINT(1))
    while True:
        try:
            g = q.get(block=False)
            if g[1] == 5:
                break
        except Empty:
            pass
        kernel32.Sleep(1) 
    kernel32.timeEndPeriod(wintypes.UINT(1))
    p.join()