from os import truncate
from pathlib import Path
from turtle import pos
from pyrr import Matrix44, Vector3

import moderngl
import pygame
import moderngl_window
from moderngl_window import geometry
from camera import *

import math

class TextureArrayExample(CameraWindow):
    """
    Cycles different texture layers in an array texture
    rendered on a cube.
    """
    title = "Texture Array"
    resource_dir = (Path(__file__).parent).resolve()
 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.num_layers = 1
        self.cube = geometry.cube(size = (40, 40, 40))
        self.sphere = geometry.sphere(radius = 2)
        self.texture = self.load_texture_array('ShiaLaBeouf.png', layers=self.num_layers, mipmap=True, anisotrpy=4.0)
        self.prog = self.load_program('texture.glsl')
        self.prog1 = self.load_program('texture.glsl')
        self.prog['texture0'].value = 0
        self.prog['num_layers'].value = 1
        self.prog1['texture0'].value = 0
        self.prog1['num_layers'].value = 1
        #self.prog['color'].value = 1.0, 1.0, 0.5, 0.5
        #self.prog1['color'].value = 1.0, 1.0, 0.5, 0.5

    def render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)
        
        time = self.wnd.frames

        modelview = Matrix44.identity(dtype='f4')
        #(abs(1/16 * math.sin(64 * time)), abs(1/16 * math.sin(64 * time)), abs(1/16 * math.sin(64 * time))), dtype='f4'
        num = abs(1/16 * math.sin(64 * time))
        num1 = abs(1/16 * math.sin(64 * time) * math.sin(64 * math.sin(64 * time) * time))
        rotation = Matrix44.from_eulers((0, 0, 0), dtype = 'f4') #TODO what is euler angles, Ima have a fun time learning that shit
        translation = Matrix44.from_translation((0.0, -30.0, -4.0), dtype='f4')
        modelview = translation * rotation
        
        #print(modelview)
        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_model'].write(modelview)
        self.prog['m_camera'].write(self.camera.matrix)
        self.prog['time'].value = time

        num = abs(1/16 * math.sin(64 * time))
        num1 = abs(1/16 * math.sin(64 * time) * math.sin(64 * math.sin(64 * time) * time))
        rotation = Matrix44.from_eulers((num, num, num), dtype = 'f4')
        translation = Matrix44.from_translation((0.0, 10.0, -4.0), dtype='f4')
        modelview = translation * rotation
        
        self.prog1['m_proj'].write(self.camera.projection.matrix)
        self.prog1['m_model'].write(modelview)
        self.prog1['m_camera'].write(self.camera.matrix)
        self.prog1['time'].value = time
        
        self.texture.use(location=0)
        self.cube.render(self.prog)
        self.sphere.render(self.prog1)
         
        #print(time)
        p = self.camera.position
        #print(p.y)
        # sf = s0 + vot + 1/2at^2
        # vf = v0 + at
        """
        t = time
        g = -9.8 / 100
        v0 = 4
        v = v0 + g * t
        s0 = 0
        sf = s0 + v0 * t + 1/2 * g * math.pow(t, 2)
        if t % 1 == 0 and v > -4:
            print(sf)
            print(v)
            print(" ")
            self.camera.set_position(p.x,-sf / 5,p.z)
        if time % 1 == 0:
            sf = 2 * math.sin(time / 10)
            self.camera.set_position(p.x,p.y -sf / 5,p.z)
        else: 
            t -= time
            v = v0 + g * t
            print(time)
            print(t)
            print(v)
            print(" ")
        """

if __name__ == '__main__':
    moderngl_window.run_window_config(TextureArrayExample)