#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;

uniform mat4 m_proj;
uniform mat4 m_model;
uniform mat4 m_camera;

out vec2 uv;

void main() {
    gl_Position = m_proj * m_camera * m_model * vec4(in_position, 1);
    uv = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
in vec2 uv;

uniform sampler2DArray texture0;

void main() {
    // Get the current and next texture layer
    vec4 c1 = texture(texture0, vec3(uv, 1));
    vec4 c2 = texture(texture0, vec3(uv, 1));

    // Interpolate between the two texture layers
    float t = mod(100, 1.0);
    fragColor = (c1) + vec4(0);
}
#endif