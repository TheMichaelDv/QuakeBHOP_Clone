"DO NOT RUN ANYMORE USE main.py"
from inspect import FrameInfo
from os import truncate
from pathlib import Path
from turtle import pos
from pyrr import Matrix44 

import moderngl
import pygame
import moderngl_window
from moderngl_window import geometry
from Resources.camera import *
from Resources.Models.level import *

import math
import time as a

class Game(CameraWindow):
    title = "Fun"
    objects = {
        "cubes": cubes(),
        "spheres": spheres()
    }
    progs = shaders()
    resource_dir = (Path(__file__).parent).resolve()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True

        self.camera.velocity = 5

        #self.objects['cubes'].add(geometry.cube(name='center'))
        #self.objects['cubes'].add(geometry.cube(size=(2,2,2), name='sides'))
        self.camera.set_position(2,0,0)
        self.texture = self.load_texture_array('Images/ayaka.jpg', layers=1, mipmap=True, anisotrpy=4.0)
        self.load_level()
        #self.progs.shader = simpleshader(self.load_program('Shaders/texture.glsl'), name='sides')

    def render(self, time: int, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)
        
        self.texture.use(location=0)

        self.objects['cubes'].rendprog(self.progs,self.camera.projection.matrix, self.camera.matrix)
        self.objects['spheres'].rendprog(self.progs,self.camera.projection.matrix, self.camera.matrix)

        return self.camera.projection.matrix, self.camera.position

    def physics(self, time: int, matrices: dict): #time in seconds
        for name in matrices[0].keys():
            self.progs.shader[name].translation = matrices[0][name]['tran']
            self.progs.shader[name].rotation = matrices[0][name]['rot']
        for name in matrices[0].keys():
            pos = self.hi(self.progs.shader[name].collision, self.camera.position)
            if pos[0]:
                self.camera.set_position(pos[1],pos[2],pos[3])
                break

    def load_level(self):
        level = scene('scene.json')
        figure = level.level
        for name in figure:
            if figure[name]['rectangle'] == TRUE:
                self.objects["cubes"].add(geometry.cube(size=(figure[name]['size']['x'],figure[name]['size']['y'],figure[name]['size']['z']),name=name))
                self.progs.shader = simpleshader(self.load_program('Shaders/' + figure[name]['shader']), name=name)
                self.progs.shader[name].collision = self.progs.shader[name].hitbox([figure[name]['center']['x'],figure[name]['center']['y'],figure[name]['center']['z']],[figure[name]['size']['x'],figure[name]['size']['y'],figure[name]['size']['z']])
                try:
                    self.progs.shader[name].shader['color'].value = figure[name]['color']['r']/255, figure[name]['color']['g']/255, figure[name]['color']['b']/255, figure[name]['color']['a']
                except KeyError:
                    pass
    def hi(self, hit, camera):
        #top
        # camera[0] = x,  camera[1] = y,  camera[2] = z  
        if camera[0] < hit[4][0] and camera[1] < hit[4][1] + .25 and camera[1] > hit[7][1] and camera[0] > hit[7][0] and camera[2] < hit[4][2] and camera[2] > hit[7][2]:
            camera = [True, camera[0],hit[4][1]+0.25,camera[2]]
        #bottom
        if camera[0] < hit[2][0] and camera[1] > hit[2][1] - 0.25 and camera[1] < hit[2][1] and camera[0] > hit[0][0] and camera[2] < hit[2][2] and camera[2] > hit[0][2]:
            camera = [True, camera[0], hit[3][1] - 0.25,camera[2]]
        #left [1, -1, -1] [-1, 1, -1] 2 7
        if camera[0] < hit[3][0] and camera[1] < hit[7][1] and camera[1] > hit[2][1] and camera[0] > hit[7][0] and camera[2] < hit[7][2] and camera[2] > hit[3][2] - .25:
            camera = [True, camera[0],camera[1],hit[3][2] - 0.25]
        #right [1,1,1] [-1,-1,1] 4 1
        if camera[0] < hit[4][0] and camera[1] < hit[4][1] and camera[1] > hit[1][1] and camera[0] > hit[1][0] and camera[2] > hit[1][2] and camera[2] < hit[4][2] + .25:
            camera = [True, camera[0],camera[1], hit[4][2] + 0.25]
        #front [1,1,1] [1, -1, -1] 3 4
        if camera[0] < hit[4][0] + 0.25 and camera[1] < hit[4][1] and camera[1] > hit[3][1] and camera[0] > hit[3][0] and camera[2] > hit[3][2] and camera[2] < hit[4][2]:
            camera = [True, hit[4][0] + 0.25,camera[1],camera[2]]
        #back [-1, 1, 1] [-1, -1, -1] 6 0
        if camera[0] > hit[6][0] - 0.25 and camera[1] < hit[6][1] and camera[1] > hit[0][1] and camera[0] < hit[0][0] and camera[2] > hit[0][2] and camera[2] < hit[6][2]:
            camera = [True, hit[6][0] - 0.25,camera[1],camera[2]]
        if camera[0] != True:
            camera = [False]
        return camera
        '''
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
        if time % 3 == 0:
            y = -0.98 * 0.5 * math.pow((time/3*0.05),2)
            self.camera.set_position(p.x,p.y+y,p.z)

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
        self.prog2 = self.load_program('Shaders/Simple Shader.glsl')
        self.scene = self.load_scene('Models/Person.obj')
        self.prog2['m_proj'].write(self.camera.projection.matrix)
        self.prog2['m_model'].write(Matrix44.identity(dtype='f4'))
        self.prog2['m_camera'].write(self.camera.matrix)
        self.scene.draw(
            projection_matrix=self.camera.projection.matrix,
            camera_matrix=self.camera.matrix,
            time=time,
        )
        self.scene.root_nodes[0].mesh.vao.render(self.prog2)
'''