from pathlib import Path

#Matrix Manipulation is the most common operation to do on 3D objects
from pyrr import Matrix44, Vector3

import moderngl
import moderngl_window
from moderngl_window import geometry

#Camera.py above this file
from camera import CameraWindow

import math


class CubeSimple(CameraWindow):
    #title of window
    title = "Plain Cube"
    #Where to look for images,shader programs etc
    resource_dir = (Path(__file__).parent).resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Makes the Cursor stuck to the center
        self.wnd.mouse_exclusivity = True
        #Creates a 2 by 2 by 2 cube 
        self.cube = geometry.cube(size=(2, 2, 2))
        #Loads a GLSL program Simple Shader.glsl located in same folder
        self.prog = self.load_program('Simple Shader.glsl')
        #color of cube (can be modified)
        self.prog['color'].value = 1.0, 1.0, 0.5, 0.5

    def render(self, time: float, frametime: float):
        #https://learnopengl.com/Advanced-OpenGL/Face-culling | https://learnopengl.com/Advanced-OpenGL/Depth-testing
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)

        #Creates a 4x4 Matrix that translates the cube's vertices
        rotation = Matrix44.from_eulers((time,time,time), dtype='f4')
        '''
        Michael Changes
        num = math.sin(1/2 * math.pi * time)
        rotation = Matrix44.from_eulers((num, num, num), dtype='f4')
        if (time - int(time) <= 0.05):
            print("Cube", time, time - int(time), num)
        '''
        translation = Matrix44.from_translation((0.0, 0.0, -3.5), dtype='f4')
        modelview = translation * rotation

        #Writes the nessesary information to shaders https://learnopengl.com/Getting-started/Shaders MUST READ!
        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_model'].write(modelview)
        self.prog['m_camera'].write(self.camera.matrix)

        #Renders the Shaders
        self.cube.render(self.prog)

class SphereSimple(CameraWindow):
    title = "Plain Sphere"
    resource_dir = (Path(__file__).parent).resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.sphere = geometry.sphere(1)
        self.prog = self.load_program('Simple Shader.glsl')
        #self.prog['color'].value = 1.0, 1.0, 0.5, 0.5

    def render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)

        num = math.sin(1/2 * math.pi * time)
        rotation = Matrix44.from_eulers((num, num, num), dtype='f4')
        '''
        if (time - int(time) <= 0.05):
            print("Sphere", time, time - int(time), num)
        '''
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
        self.cube = geometry.cube(size=(2, 2, 2)) #need to have two different set of variables
        self.sphere = geometry.sphere(radius = 4)
        self.prog = self.load_program('Simple Shader.glsl')
        self.prog1 = self.load_program('Simple Shader.glsl')
        #self.prog['color'].value = 1.0, 1.0, 0.5, 0.5

    def render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)

        num = math.sin(1/2 * math.pi * time)
        rotation = Matrix44.from_eulers((num, num, num), dtype='f4')
        '''
        if (time - int(time) <= 0.05):
            print("Cube", time, time - int(time), num)
        '''
        translation = Matrix44.from_translation((0.0, 0.0, 0), dtype='f4')
        modelview = translation * rotation
        
        #also requires different shader instances for moving
        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_model'].write(modelview)
        self.prog['m_camera'].write(self.camera.matrix)


        num = math.sin(1/2 * math.pi * time)
        rotation = Matrix44.from_eulers((num, num, num), dtype='f4')
        translation = Matrix44.from_translation((0.0, -10.0, 0), dtype='f4')
        modelview = translation * rotation
        
        self.prog1['m_proj'].write(self.camera.projection.matrix)
        self.prog1['m_model'].write(modelview)
        self.prog1['m_camera'].write(self.camera.matrix)

        self.cube.render(self.prog)
        self.sphere.render(self.prog1)

if __name__ == '__main__':
    moderngl_window.run_window_config(CubeAndSphereSimple)