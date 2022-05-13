from gettext import translation
import moderngl_window as mglw
from pyrr import Matrix44
from moderngl.program import Program
from moderngl_window.scene.camera import KeyboardCamera, OrbitCamera
from moderngl_window.context.base import BaseKeys
from moderngl_window.opengl.vao import VAO

import math

class CameraWindow(mglw.WindowConfig):
    """Base class with built in 3D camera support"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = KeyboardCamera(self.wnd.keys, aspect_ratio=self.wnd.aspect_ratio)
        self.camera_enabled = True
        self.keys = BaseKeys()

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
        #jump
        elif key == keys.J: 
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
                        c = False
        elif key == keys.F:
            self.camera_enabled = not self.camera_enabled
            self.wnd.mouse_exclusivity = self.camera_enabled
            self.wnd.cursor = not self.camera_enabled
        elif key == keys.SPACE:
            print("Space")
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

class cubes():
    def __init__(self):
        self.cubes = []
    def __init__(self, cube: VAO):
        self.cubes = [cube]
    def addcube(self, cube: VAO):
        self.cube.append(cube)
    def findcube(self, name):
        for cube in self.cubes:
            if cube.name == name:
                return cube
        return None
    def removecube(self, name):
        for cube in self.cubes:
            if cube.name == name:
                cube.release(True)
    def rendprog(self, shaders, name):
        rend = None
        for shade in shaders:
            if shade.name == name:
                rend = shade
        for cube in self.cubes:
            if cube.name == name and rend != None:
                cube.render(rend)

class spheres():
    def __init__(self):
        self.cubes = []
    def __init__(self, sphere: VAO):
        self.spheres = [sphere]
    def addsphere(self, sphere: VAO):
        self.spheres.append(sphere)
    def findspheres(self, name):
        for sphere in self.spheres:
            if sphere.name == name:
                return sphere
        return None
    def removesphere(self, name):
        for sphere in self.spheres:
            if sphere.name == name:
                spheres.release(True)
    def rendprog(self, shaders, name):
        rend = None
        for shade in shaders:
            if shade.name == name:
                rend = shade
        for sphere in self.spheres:
            if sphere.name == name and rend != None:
                sphere.render(rend)
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
    _rotation = (0,0,0)
    _translation = (0,0,0)
    fields = []
    def __init__(self):
        self._shader = None
    def __init__(self, prog: Program, name = None):
        self._shader = prog
        self.name = name
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
    @property
    def rotation(self):
        return self._rotation
    @rotation.setter
    def rotation(self, matrix):
        self._rotation = matrix
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

class shaders():
    def __init__(self) -> None:
        self.shaders = []
    def run(self, camera) -> None:
        for n in shaders:
            n.run(camera)