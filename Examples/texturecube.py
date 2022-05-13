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

class Ihavenoidea(CameraWindow):
    title = "Fun"
    resource_dir = (Path(__file__).parent).resolve()
 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True

        self.cube = spheres(geometry.sphere(radius = 2, name='center'))
        self.sphere = spheres(geometry.sphere(radius = 2, name='side'))

        self.texture = self.load_texture_array('help.png', layers=1, mipmap=True, anisotrpy=4.0)
        self.prog = simpleshader(self.load_program('texture.glsl'), name='center')
        self.prog1 = simpleshader(self.load_program('texture.glsl'), name='side')
        self.prog.shader['texture0'] = 0
        self.prog1.shader['texture0'] = 0
        self.prog.fieldadd(['m_proj', 'm_model','m_camera'])
        self.prog1.fieldadd(['m_proj', 'm_model','m_camera'])

    def render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)
        
        time = self.wnd.frames

        #(abs(1/16 * math.sin(64 * time)), abs(1/16 * math.sin(64 * time)), abs(1/16 * math.sin(64 * time))), dtype='f4'
        #num = abs(4 * math.sin(1/164 * time))
        #num1 = abs(1/16 * math.sin(64 * time) * math.sin(64 * math.sin(64 * time) * time))
        num2 = 4 * math.sin(time / 10)
        numx = 8 * math.sin(time / 25)
        numy = 16 * math.cos(time / 25)

        self.prog.run(self.camera.projection.matrix, self.camera.matrix, tran = (numx, numy, 0), rot = (num2, num2, num2)) #TODO what is euler angles, Ima have a fun time learning that shit
        num = abs(1/16 * math.sin(64 * time))
        self.prog.run(self.camera.projection.matrix, self.camera.matrix, tran = (num, num, num), rot = (0, 0, 0))
        
        self.texture.use(location=0)
        self.cube.findspheres('center').render(self.prog.shader)
        self.sphere.findspheres('side').render(self.prog1.shader)
         
        """
        if time % 3 == 0:
            y = -0.98 * 0.5 * math.pow((time/3*0.05),2)
            self.camera.set_position(p.x,p.y+y,p.z)

        #print(p.y)
        # sf = s0 + vot + 1/2at^2
        # vf = v0 + at
        t = time
        g = -9.8 / 100
        v0 = 4
        v = v0 + g * t
        s0 = 0
        sf = s0 + v0 * t + 1/2 * g * math.pow(t, 2)
        if t % 1 == 0 and v > -4:
            #print(sf)
            #print(v)
            #print(" ")
            self.camera.set_position(p.x,sf/5,p.z)
        if time % 1 == 0:
            sf = 2 * math.sin(time / 10)
            self.camera.set_position(p.x,p.y -sf / 5,p.z)
        """

if __name__ == '__main__':
    moderngl_window.run_window_config(Ihavenoidea)