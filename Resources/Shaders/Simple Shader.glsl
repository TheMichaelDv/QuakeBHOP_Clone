#version 330

//https://stackoverflow.com/questions/4421261/vertex-shader-vs-fragment-shader
//generally shaders determines color of a shape. Specifically Vertex Shaders determine the color of vertices in the object, say the 8 corners of the block. The Fragment Shader defines the color between the vertices, the faces of the cube for example.

#if defined VERTEX_SHADER

//given certain information
in vec3 in_position;
in vec3 in_normal;

//Model information, camera, and direction
uniform mat4 m_model;
uniform mat4 m_camera;
uniform mat4 m_proj;

//outputs
out vec3 pos;
out vec3 normal;

void main() {
    pos = vec3(m_model * vec4(in_position, 1.0));
    normal = in_normal;  
    
    gl_Position = m_proj * m_camera * vec4(pos, 1.0);
}

//https://en.wikipedia.org/wiki/Graphics_pipeline
#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform vec4 color;

in vec3 pos;
in vec3 normal;

void main() {
    fragColor = color;// * color This determines final color. Usually we define a uniform so we can modify it in python
}
#endif
