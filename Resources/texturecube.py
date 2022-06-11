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

        self.camera.velocity = 2

        #self.objects['cubes'].add(geometry.cube(name='center'))
        #self.objects['cubes'].add(geometry.cube(size=(2,2,2), name='sides'))
        self.texture = self.load_texture_array('Images/ayaka.jpg', layers=1, mipmap=True, anisotrpy=4.0)

        self.obj = self.load_scene('Models/Person.obj')

        self.load_level()
        #self.progs.shader = simpleshader(self.load_program('Shaders/texture.glsl'), name='sides')

    def render(self, time: int, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)
        
        self.texture.use(location=0)

        tim = time/10

        self.progs.shader['center'].shader['lightpos'].value = self.camera.position[0], self.camera.position[1], self.camera.position[2]
        
        camera_matrix = self.camera.matrix * Matrix44.from_translation((0,5-time/2,0)) * Matrix44.from_eulers((3.14/2, 0, 0))

        self.obj.draw(
            projection_matrix= self.camera.projection.matrix,
            camera_matrix= camera_matrix,
            time = time
        )
        
        #self.progs.shader['center'].shader['lightpos'].value = math.sin(time) + 1, math.cos(time) + 1, math.sin(time) + 1

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
                except:
                    pass
                try: 
                    self.progs.shader[name].shader['color'].value = figure[name]['color']['r']/255, figure[name]['color']['g']/255, figure[name]['color']['b']/255
                    self.progs.shader[name].shader['lightColor'].value = 1, 1, 1
                    self.progs.shader[name].shader['lightpos'].value = 0, 5, 0
                except:
                    pass
        self.camera.set_position(0,5,0)
    def hi(self, hit, camera):
        #top
        # camera[0] = x,  camera[1] = y,  camera[2] = z   [1,1,1] [-1,1,-1]
        if camera[0] < hit[4][0] and camera[1] < hit[4][1] + .25 and camera[1] > hit[7][1] and camera[0] > hit[7][0] and camera[2] < hit[4][2] and camera[2] > hit[7][2]:
            camera = [True, camera[0],hit[4][1]+0.25,camera[2]]
        #bottom
        elif camera[0] < hit[2][0] and camera[1] > hit[2][1] - 0.25 and camera[1] < hit[0][1] and camera[0] > hit[0][0] and camera[2] < hit[2][2] and camera[2] > hit[0][2]:
            camera = [True, camera[0], hit[3][1] - 0.25,camera[2]]
        #left [1, -1, -1] [-1, 1, -1] 2 7
        elif camera[0] < hit[3][0] and camera[1] < hit[7][1] and camera[1] > hit[2][1] and camera[0] > hit[7][0] and camera[2] < hit[7][2] and camera[2] > hit[3][2] - .25:
            camera = [True, camera[0],camera[1],hit[3][2] - 0.25]
        #right [1,1,1] [-1,-1,1] 4 1
        elif camera[0] < hit[4][0] and camera[1] < hit[4][1] and camera[1] > hit[1][1] and camera[0] > hit[1][0] and camera[2] > hit[1][2] and camera[2] < hit[4][2] + .25:
            camera = [True, camera[0],camera[1], hit[4][2] + 0.25]
        #front [1,1,1] [1, -1, -1] 3 4
        elif camera[0] < hit[4][0] + 0.25 and camera[1] < hit[4][1] and camera[1] > hit[3][1] and camera[0] > hit[3][0] and camera[2] > hit[3][2] and camera[2] < hit[4][2]:
            camera = [True, hit[4][0] + 0.25,camera[1],camera[2]]
        #back [-1, 1, 1] [-1, -1, -1] 6 0
        elif camera[0] > hit[6][0] - 0.25 and camera[1] < hit[6][1] and camera[1] > hit[0][1] and camera[0] < hit[0][0] and camera[2] > hit[0][2] and camera[2] < hit[6][2]:
            camera = [True, hit[6][0] - 0.25,camera[1],camera[2]]
        else:
            camera = [False]
        return camera

