from ctypes import windll, wintypes
from multiprocessing.sharedctypes import Value
from queue import Empty, Full
from time import perf_counter_ns as ns
import numpy as np
from Resources.Models.level import *
'''
TODO: Add modularity and reuseablity
'''

class obj():
    
    _shapes = {}

    def __init__(self, names: list) -> None:
        for name in names:
            self._shapes[name] = {
                'tran': np.array([0,0,0],dtype='float64'),
                'rot': np.array([0,0,0],dtype='float64'),
                'collision': None
            }
    @property
    def shapes(self):
        return self._shapes
    @shapes.setter
    def shapes(self, name) -> None:
        self._shapes[name] = {
                'tran': np.array([0,0,0],dtype='float64'),
                'rot': np.array([0,0,0],dtype='float64')
        }
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
    def hitbox(self, name, cuboidCtr, cuboidSize):
        boolList = [[-1, -1, -1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1], [1, -1, -1], [1, 1, -1], [-1, 1, 1], [1, 1, 1]]
        shape = []
        for i in range(8):
            temp = [0,0,0]
            temp[0] = cuboidCtr[0] + boolList[i][0] * cuboidSize[0] / 2
            temp[1] = cuboidCtr[1] + boolList[i][1] * cuboidSize[1] / 2
            temp[2] = cuboidCtr[2] + boolList[i][2] * cuboidSize[2] / 2
            shape.append(temp)
        self._shapes[name]['collision'] = np.array(shape,dtype='float64')

def pos(hit, camera):
        #print(camera)
        #top
        if camera[0] < 1 and camera[1] < 1.25 and camera[1] > 1 and camera[0] > -1 and camera[2] < 1 and camera[2] > -1:
            camera = [True, camera[0],1.25,camera[2]]
        #bottom
        if camera[0] < 1 and camera[1] > -1.25 and camera[1] < -1 and camera[0] > -1 and camera[2] < 1 and camera[2] > -1:
            camera = [True, camera[0],-1.25,camera[2]]
        #left
        if camera[0] < 1 and camera[1] < 1 and camera[1] > -1 and camera[0] > -1 and camera[2] > 1 and camera[2] < 1.25:
            camera = [True, camera[0],camera[1],1.25]
        #right
        if camera[0] < 1 and camera[1] < 1 and camera[1] > -1 and camera[0] > -1 and camera[2] > -1.25 and camera[2] < -1:
            camera = [True, camera[0],camera[1],-1.25]
        #front
        if camera[0] < -1 and camera[1] < 1 and camera[1] > -1 and camera[0] > -1.25 and camera[2] > -1 and camera[2] < 1:
            camera = [True, -1.25,camera[1],camera[2]]
        #back
        if camera[0] > 1 and camera[1] < 1 and camera[1] > -1 and camera[0] < 1.25 and camera[2] > -1 and camera[2] < 1:
            camera = [True, 1.25,camera[1],camera[2]]
        if camera[0] != True:
            camera = [False]
        return camera
def physics(queue):
    kernel32 = windll.kernel32
    kernel32.timeBeginPeriod(wintypes.UINT(1))

    hitbox = None
    camera = [2,0,0]
    frametime = 19000000
    delta = 1000000000

    lvl = scene('scene.json')
    things = lvl.level    

    p = obj([name for name in things])
    for t in things:
        p.set(t, tran = np.array([things[t]['center']['x'],things[t]['center']['y'],things[t]['center']['z']],dtype='float64'))
        p.hitbox(t,[things[t]['center']['x'],things[t]['center']['y'],things[t]['center']['z']], [things[t]['size']['x'],things[t]['size']['y'],things[t]['size']['z']])

        print(p.shapes)
    while True:
        sleep = ns()
        while delta+(ns()-sleep) < frametime:
            kernel32.Sleep(1) 
        delta = ns()   

        #p.move('center',tran=np.array([0,0.01,0]))
        #p.move('sides', rot=np.array([0,0.01,0]))

        try:
            queue[0].put((p.shapes, camera), block=False)
        except Full:
            pass
        try:
            hitbox = queue[1].get(block=False)
        except Empty:
            pass
        if type(hitbox) == type(tuple()):
            camera = pos(hitbox[0], hitbox[1])
        if hitbox == True:
            break
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