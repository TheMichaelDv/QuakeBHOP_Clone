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
    /*
    mat4 m_view = m_camera * m_model;
    vec4 p = m_view * vec4(in_position, 1.0);
    gl_Position =  m_proj * p;
    mat3 m_normal = inverse(transpose(mat3(m_view)));
    normal = m_normal * normalize(in_normal);
    pos = vec3(1,1,1);
    */
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
    float ambientStrength = 0.6;
    vec3 ambient = ambientStrength * vec3(1,1,1);

    vec3 result = ambient * vec3(1,1,1);
    fragColor = color;// * color This determines final color. Usually we define a uniform so we can modify it in python
}
#endif
