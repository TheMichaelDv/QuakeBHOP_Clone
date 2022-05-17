"DO NOT RUN ANYMORE USE main.py"
from inspect import FrameInfo
from os import truncate
from pathlib import Path
from turtle import pos
from pyrr import Matrix44, Vector3

import moderngl
import pygame
import moderngl_window
from moderngl_window import geometry
from Resources.camera import *

import math
import time as a

class Game(CameraWindow):
    title = "Fun"
    resource_dir = (Path(__file__).parent).resolve()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True

        self.cube = cubes(geometry.cube(name='center'))
        self.sphere = cubes(geometry.cube(size=(2,2,2), name='side'))

        self.texture = self.load_texture_array('Images/help.png', layers=1, mipmap=True, anisotrpy=4.0)
        self.prog = simpleshader(self.load_program('Shaders/texture.glsl'), name='center')
        self.prog1 = simpleshader(self.load_program('Shaders/texture.glsl'), name='side')
        self.prog.shader['texture0'] = 0
        self.prog1.shader['texture0'] = 0
        self.tick = a.time()
        """
        time = self.tick

        num = abs(4 * math.sin(1/164 * time))
        num1 = abs(1/16 * math.sin(64 * time) * math.sin(64 * math.sin(64 * time) * time))
        num2 = 4 * math.sin(time / 10)
        numx = 8 * math.sin(time / 25)
        numy = 16 * math.cos(time / 25)

        rotation = Matrix44.from_eulers((num2, num2, num2), dtype = 'f4') #TODO what is euler angles, Ima have a fun time learning that shit
        translation = Matrix44.from_translation((num2, num2, num2), dtype='f4')
        translation = Matrix44.from_translation((numx, numy, 0), dtype='f4')
        modelview = translation * rotation

        self.prog1['m_proj'].write(self.camera.projection.matrix)
        self.prog1['m_model'].write(modelview)
        self.prog1['m_camera'].write(self.camera.matrix)
        self.prog1['time'].value = time
        """

    def render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)
        
        time = self.wnd.frames

        #print(frametime)
        t = self.prog1.translation

        '''
        if self.camera.matrix[3][2] >=5:
           position = self.camera.matrix[3]
           self.camera.set_position(position[0],position[1],5)

        time = self.tick
        num = abs(4 * math.sin(1/164 * time))
        num1 = abs(1/16 * math.sin(64 * time) * math.sin(64 * math.sin(64 * time) * time))
        num2 = 4 * math.sin(time / 10)
        numx = 8 * math.sin(time / 25)
        numy = 16 * math.cos(time / 25)
        rotation = Matrix44.from_eulers((num2, num2, num2), dtype = 'f4')
        translation = Matrix44.from_translation((num2, num2, num2), dtype='f4')
        modelview = translation * rotation
        self.prog['m_model'].write(modelview)
        self.prog1['m_model'].write(modelview)
        '''

        self.prog.run(self.camera.projection.matrix, self.camera.matrix) #TLDR: Euler Angles rotate the cube x radians in each axis,    
        #this is why we abstract or else this would be 10 lines instead of 4 
        if t[1] >=  -5 and t[1] <= 5:
            self.prog1.run(self.camera.projection.matrix, self.camera.matrix, tran = (0,0,0), rot = (0,0,0))
            #self.camera.set_position(1,1,1)
            #print(self.camera.projection.matrix)
        else:
            self.prog1.run(self.camera.projection.matrix, self.camera.matrix, rot= (0,0,0))

        self.texture.use(location=0)
        self.cube.find('center').render(self.prog.shader)
        self.sphere.find('side').render(self.prog1.shader)
        
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
    def physics(self, time: float): #time in seconds
        pass