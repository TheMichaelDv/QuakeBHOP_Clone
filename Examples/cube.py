from pathlib import Path
from pyrr import Matrix44, Vector3

import moderngl
import moderngl_window
from moderngl_window import geometry

from camera import CameraWindow

import math


class CubeSimple(CameraWindow):
    title = "Plain Cube"
    resource_dir = (Path(__file__).parent).resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.cube = geometry.cube(size=(2, 2, 2))
        self.prog = self.load_program('Simple Shader.glsl')
        self.prog['color'].value = 1.0, 1.0, 0.5, 0.5

    def render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)

        num = math.sin(1/2 * math.pi * time)
        rotation = Matrix44.from_eulers((num, num, num), dtype='f4')
        if (time - int(time) <= 0.05):
            print("Cube", time, time - int(time), num)
        translation = Matrix44.from_translation((0.0, 0.0, -3.5), dtype='f4')
        modelview = translation * rotation

        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_model'].write(modelview)
        self.prog['m_camera'].write(self.camera.matrix)

        self.cube.render(self.prog)

class SphereSimple(CameraWindow):
    title = "Plain Sphere"
    resource_dir = (Path(__file__).parent).resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.sphere = geometry.sphere(1)
        self.prog = self.load_program('Simple Shader.glsl')
        self.prog['color'].value = 1.0, 1.0, 0.5, 0.5

    def render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)

        num = math.sin(1/2 * math.pi * time)
        rotation = Matrix44.from_eulers((num, num, num), dtype='f4')
        if (time - int(time) <= 0.05):
            print("Sphere", time, time - int(time), num)
        translation = Matrix44.from_translation((0.0, 0.0, -3.5), dtype='f4')
        modelview = translation * rotation

        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_model'].write(modelview)
        self.prog['m_camera'].write(self.camera.matrix)

        self.sphere.render(self.prog)

class CubeAndSphereSimple(CameraWindow):
    title = "Plain Cube & Sphere"
    resource_dir = (Path(__file__).parent).resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.cube = geometry.cube(size=(2, 2, 2))
        self.cube = geometry.cube(size=(2, 2, 2))
        self.prog = self.load_program('Simple Shader.glsl')
        self.prog['color'].value = 1.0, 1.0, 0.5, 0.5

    def render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)

        num = math.sin(1/2 * math.pi * time)
        rotation = Matrix44.from_eulers((num, num, num), dtype='f4')
        if (time - int(time) <= 0.05):
            print("Cube", time, time - int(time), num)
        translation = Matrix44.from_translation((0.0, 0.0, -3.5), dtype='f4')
        modelview = translation * rotation

        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_model'].write(modelview)
        self.prog['m_camera'].write(self.camera.matrix)

        self.cube.render(self.prog)

if __name__ == '__main__':
    moderngl_window.run_window_config(SphereSimple)