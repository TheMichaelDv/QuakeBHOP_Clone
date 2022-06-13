from gettext import translation
import moderngl_window as mglw
import time
from pyrr import Matrix44
from moderngl.program import Program
from Resources.BaseCamera import KeyboardCamera
from moderngl_window.context.glfw import Keys
from moderngl_window.opengl.vao import VAO

import math
import numpy as np

class CameraWindow(mglw.WindowConfig):
    """Base class with built in 3D camera support"""
    _last_time = 0
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = KeyboardCamera(self.wnd.keys, aspect_ratio=self.wnd.aspect_ratio, near = 0.15)
        self.camera_enabled = True
        self.keys = Keys()

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if key == keys.D:
            if action == self.keys.ACTION_PRESS:
                self.camera.move_right(True)
            elif action == self.keys.ACTION_RELEASE:
                self.camera.move_right(False)
        # Left
        elif key == keys.A:
            if action == self.keys.ACTION_PRESS:
                self.camera.move_left(True)
            elif action == self.keys.ACTION_RELEASE:
                self.camera.move_left(False)
        # Forward
        elif key == keys.W:
            if action == self.keys.ACTION_PRESS:
                self.camera.move_forward(True)
            if action == self.keys.ACTION_RELEASE:
                self.camera.move_forward(False)
            # Backwards
        elif key == keys.S:
            if action == self.keys.ACTION_PRESS:
                self.camera.move_backward(True)
            if action == self.keys.ACTION_RELEASE:
                self.camera.move_backward(False)
        elif key == keys.F:
            self.camera_enabled = not self.camera_enabled
            self.wnd.mouse_exclusivity = self.camera_enabled
            self.wnd.cursor = not self.camera_enabled
        elif key == keys.SPACE:
            if action == self.keys.ACTION_PRESS:
                self.camera.move_up(True)
            if action == self.keys.ACTION_RELEASE:
                self.camera.move_up(False)
        elif key == keys.Z:
            if action == self.keys.ACTION_PRESS:
                self.camera.move_down(True)
            if action == self.keys.ACTION_RELEASE:
                self.camera.move_down(False)

    def mouse_position_event(self, x: int, y: int, dx, dy):
        if self.camera_enabled:
            self.camera.rot_state(-dx, -dy)

    def resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)
''' elif key == keys.J: 
            if action == self.keys.ACTION_PRESS:
                print("J")
                p = self.camera.position
                t = self.wnd.frames
                g = -9.8 / 100
                v0 = 4
                v = v0 + g * t
                s0 = 0
                sf = s0 + v0 * t + 1/2 * g * math.pow(t, 2)
                c = True
                while(c):
                    if t % 1 == 0 and v > -4:
                        self.camera.move_up(False)
                        self.camera.move_down(False)
                        self.camera.set_position(p.x,-sf / 5,p.z)
                        t += 1/10
                    else: 
                        c = False'''

class simpleshader():
    '''
    removes the need to spam the
    self.prog1['m_proj'].write(self.camera.projection.matrix)
    self.prog1['m_model'].write(modelview)
    self.prog1['m_camera'].write(self.camera.matrix)
    and other repetitive shit
    also simplifies the code
    '''
    name = None
    _rotation = [0,0,0]
    _translation = [0,0,0]
    fields = []
    def __init__(self, prog = None, name = None):
        self._shader = prog
        self.name = name
        self.collision = None
        self.size = None
    @property
    def shader(self):
        return self._shader
    @property
    def name(self):
        return self._name
    @shader.setter
    def shader(self, prog: Program):
        self._shader = prog
    @shader.deleter
    def shader(self, c = None):
        self._shader.release()
    @name.setter
    def name(self, name):
        self._name = name
    @property
    def translation(self):
        return self._translation
    @translation.setter
    def translation(self,matrix):
        self._translation = matrix
    def move(self,mod):
        self.translation = [self.translation[0]+mod[0],self.translation[1]+mod[1],self.translation[2]+mod[2]]
    @property
    def rotation(self):
        return self._rotation
    @rotation.setter
    def rotation(self, matrix):
        self._rotation = matrix
    def moverot(self,mod):
        self._rotation = [self._rotation[0]+mod[0],self._rotation[1]+mod[1],self._rotation[2]+mod[2]]
    def fieldadd(self, fields):
        self.fields = fields
    def write(self, data):
        for f in self.fields:
            if f != 'm_proj' or f != 'm_model' or f != 'm_camera':
                self.shader[f].write(data)
    def run(self, proj, camera, tran = None, rot = None):
        if tran:
            self._translation = tran
        if rot:
            self._rotation = rot
        self.shader['m_proj'].write(proj)
        self.shader['m_model'].write(Matrix44.from_translation(self.translation, dtype='f4') * Matrix44.from_eulers(self.rotation, dtype='f4'))
        self.shader['m_camera'].write(camera)
    def hitbox(self, cuboidCtr, cuboidSize):
        #4 5 6 7 top, 2 3 4 5 front, 7 3 left, 5 7 4 0 right, 6 7 1 0 back, 0 1 2 3 bottom
        boolList = [[-1, -1, -1], [-1, -1, 1], [1, -1, 1], [1, -1, -1], [1, 1, 1],[1, 1, -1], [-1, 1, 1], [-1, 1, -1]]
        shape = []
        for i in range(8):
            temp = [0,0,0]
            temp[0] = cuboidCtr[0] + boolList[i][0] * cuboidSize[0] / 2
            temp[1] = cuboidCtr[1] + boolList[i][1] * cuboidSize[1] / 2
            temp[2] = cuboidCtr[2] + boolList[i][2] * cuboidSize[2] / 2
            shape.append(temp)
        return np.array(shape,dtype='float64')
class shaders():

    _shader = {
    }

    def __init__(self, shader = None) -> None:
        if shader == None:
            pass
        else:
            self._shader[shader.name] = shader
    @property
    def shader(self):
        return self._shader
    @shader.setter
    def shader(self, shader: simpleshader):
        self._shader[shader.name] = shader
    @shader.deleter
    def shader(self):
        for name in self._shader.keys():
            del self._shader[name]
    def named(self, name):
        return self._shader[name]
    def render(self, proj = None, camera = None):
        for name in self._shader.keys():
            self._shader[name].run(proj, camera)

class cubes():
    def __init__(self, cube = None):
        if cube == None:
            self.cubes = {}
        else:
            self.cubes = {
                cube.name: cube, #cube, trans, rot
            }
    def add(self, cube: VAO):
        self.cubes[cube.name] = cube
    def find(self, name):
        try:
            return self.cubes[name]
        except:
            return None
    def remove(self, name):
        try:
            self.cubes[name].release()
        except:
            return None
    def rendprog(self, shaders: shaders, proj, camera):
        shaders.render(proj = proj, camera = camera)
        for name in self.cubes:
            self.cubes[name].render(shaders.named(name).shader)

class spheres():
    def __init__(self, sphere = None):
        if sphere == None:
            self.spheres = {}
        else:
            self.spheres = {
                sphere.name: sphere, #sphere, trans, rot
            }
    def add(self, sphere: VAO):
        self.spheres[sphere.name] = sphere
    def find(self, name):
        try:
            return self.spheres[name]
        except:
            return None
    def remove(self, name):
        try:
            self.spheres[name].release()
        except:
            return None
    def rendprog(self, shaders: shaders, proj, camera):
        shaders.render(proj = proj, camera = camera)
        for name in self.spheres:
            self.spheres[name].render(shaders[0][name])