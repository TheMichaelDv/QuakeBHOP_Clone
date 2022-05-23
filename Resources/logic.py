from ctypes import windll, wintypes
from queue import Empty, Full
from time import perf_counter_ns as ns

'''
TODO: Add modularity and reuseablity
'''

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

def physics(queue):
    kernel32 = windll.kernel32
    kernel32.timeBeginPeriod(wintypes.UINT(1))

    frametime = 19000000
    delta = 1000000000

    p = poly([0,0,0])
    while True:
        sleep = ns()
        while delta+(ns()-sleep) < frametime:
            kernel32.Sleep(1) 
        delta = ns()   
        p.relv(0,0.01,0)
        try:
            queue[0].put(p.shapes, block=False)
        except Full:
            kernel32.Sleep(1)
        try:
            if queue[1].get(block=False):
                break
        except Empty:
            pass
        except Full:
            pass
        delta = ns() - delta
    kernel32.timeEndPeriod(wintypes.UINT(1))
'''
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
'''