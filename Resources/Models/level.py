from pathlib import Path
import json

'''
Each item in the dic represents a lvl object. Gonna need to load each of them in, once in the render once in the physics engine.

Current Hierarchy (All lowercase letters):
Name{
    Rectangle: Boolean,
    Sphere: Boolean,
    Floating: Boolean, # i dont think we need this but whatever
    Collision: Boolean,
    Shader: str, #name of file in Resources/Shaders
    Size: {
        x: int,
        y: int,
        z: int
    },
    corners: { #for orientation
        lttc: {
            x: int,
            y: int,
            z: int
        },
        rbbc: {
            x: int,
            y: int,
            z: int,
        }
    }
}
'''

path = (Path(__file__).parent).resolve()

TRUE = "True"
FALSE = "False"

class scene():
    _level = None
    def __init__(self, level: str) -> None:
        with open(path / level) as lvl:
            self._level = json.load(lvl)
    @property
    def level(self):
        return self._level
    @level.setter
    def level(self, obj):
        self._level = obj
    def getobj(self, name):
        return self._level[name]