from ctypes import windll, wintypes
from multiprocessing.sharedctypes import Value
from queue import Empty, Full
from time import perf_counter_ns as ns
import numpy as np

'''
TODO: Add modularity and reuseablity
'''

class obj():
    
    _shapes = {}

    def __init__(self, names: list) -> None:
        for name in names:
            self._shapes[name] = {
                'tran': np.array([0,0,0],dtype='float64'),
                'rot': np.array([0,0,0],dtype='float64')
            }
    @property
    def shapes(self):
        return self._shapes
    @shapes.setter
    def shapes(self, shape: dict) -> None:
        self._shapes = shape
    def move(self, name, tran = np.array([0,0,0],dtype='float64'), rot = np.array([0,0,0],dtype='float64')):
        if name not in self._shapes:
            return None
        self._shapes[name]['tran'] += tran
        self._shapes[name]['rot'] += rot
    def set(self, name, tran = np.array([0,0,0],dtype='float64'), rot = np.array([0,0,0],dtype='float64')):
        if name not in self._shapes:
            return None
        self._shapes[name]['tran'] = tran
        self._shapes[name]['rot'] = rot
def physics(queue):
    kernel32 = windll.kernel32
    kernel32.timeBeginPeriod(wintypes.UINT(1))

    frametime = 19000000
    delta = 1000000000

    p = obj(['center','sides'])
    while True:
        sleep = ns()
        while delta+(ns()-sleep) < frametime:
            kernel32.Sleep(1) 
        delta = ns()   

        p.move('center',tran=np.array([0,0.01,0]))
        p.move('sides', rot=np.array([3.14/500,0,0]))
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
    q = Queue(2)--
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