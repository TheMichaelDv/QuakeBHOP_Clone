from pathlib import Path
from pyrr import Matrix44

import moderngl

import moderngl_window
from moderngl_window import geometry
from camera import CameraWindow


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
        self.cube = geometry.cube(size=(2, 2, 2))
        self.texture = self.load_texture_array(
            'help.png', layers=self.num_layers, mipmap=True, anisotrpy=8.0)
        self.prog = self.load_program('texture.glsl')
        self.prog['texture0'].value = 0
        self.prog['num_layers'].value = 1

    def render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)

        #modelview = Matrix44.identity(dtype='f4')
        
        rotation = Matrix44.from_eulers((time, time, time), dtype='f4')
        translation = Matrix44.from_translation((0.0, 0.0, -3.5), dtype='f4')
        modelview = translation * rotation
        
        #print(modelview)
        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_model'].write(modelview)
        self.prog['m_camera'].write(self.camera.matrix)
        self.prog['time'].value = time

        self.texture.use(location=0)
        self.cube.render(self.prog)


if __name__ == '__main__':
    moderngl_window.run_window_config(TextureArrayExample)