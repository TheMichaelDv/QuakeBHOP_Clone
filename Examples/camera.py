import moderngl_window as mglw
from moderngl.program import Program
from moderngl_window.scene.camera import KeyboardCamera, OrbitCamera
from moderngl_window.context.base import BaseKeys
from moderngl_window.opengl.vao import VAO

class CameraWindow(mglw.WindowConfig):
    """Base class with built in 3D camera support"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = KeyboardCamera(self.wnd.keys, aspect_ratio=self.wnd.aspect_ratio)
        self.camera_enabled = True
        self.keys = BaseKeys()

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if self.camera_enabled:
            #self.camera.key_input(key, action, modifiers)
            pass
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
    def addprog(self, prog: Program, name):
        for cube in self.cubes:
            if cube.name == name:
                cube.render(prog)

class shaders():
    '''
    removes the need to spam the
    self.prog1['m_proj'].write(self.camera.projection.matrix)
    self.prog1['m_model'].write(modelview)
    self.prog1['m_camera'].write(self.camera.matrix)
    and other repetitive shit

    also simplifies the code
    '''

    def __init__(self) -> None:
        self.shaders = []
    def __init__(self, shader: Program):
        self.shaders = [(shader, True)]
    def addshader(self, shader: Program, third = True, ):
        self.shaders.append((shader,True))
    def write(self, data, field, shader):
        pass
    