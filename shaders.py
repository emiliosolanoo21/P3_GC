#En OpenGl, los shaders se escriben
#en un nuevo lenguaje llamado GLSL
#(Graphics Library Shaders Language)


#-----------------------------------
#Vertex Shaders
#-----------------------------------

vertex_shader= '''
#version 450 core

layout(location=0) in vec3 position;
layout(location=1) in vec2 texCoords;
layout(location=2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;

out vec2 UVs;
out vec3 outNormals;

void main()
{   
    outNormals = (modelMatrix * vec4(normals,0.0)).xyz;
    outNormals = normalize(outNormals);

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    UVs = texCoords;
}
'''

complex_shader= '''
#version 450 core

layout(location=0) in vec3 position;
layout(location=1) in vec2 texCoords;
layout(location=2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec3 outNormals;
out vec3 worldPos;
out vec3 outPosition;
out vec2 UVs;

void main()
{   
    outNormals = normalize(modelMatrix * vec4(normals, 1.0)).xyz;
    vec4 pos = viewMatrix * vec4(position, 1.0);
    worldPos = pos.xyz;
    outPosition = position;
    UVs = texCoords;
    gl_Position = projectionMatrix * modelMatrix * pos;
}
'''

vibing_shader= '''
#version 450 core

layout(location=0) in vec3 position;
layout(location=1) in vec2 texCoords;
layout(location=2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;

out vec2 UVs;
out vec3 outNormals;

void main()
{
    vec3 pos = position;
    pos.y += sin(time + pos.x + pos.z)/2;
    
    outNormals = (modelMatrix * vec4(normals,0.0)).xyz;
    outNormals = normalize(outNormals);
    
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(pos, 1.0);
    UVs = texCoords;
}
'''

fat_shader= '''
#version 450 core

layout(location=0) in vec3 position;
layout(location=1) in vec2 texCoords;
layout(location=2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float fatness;

out vec2 UVs;
out vec3 outNormals;

void main()
{   
    outNormals = (modelMatrix * vec4(normals,0.0)).xyz;
    outNormals = normalize(outNormals);
    vec3 pos = position + (fatness/4) * outNormals;
    
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(pos, 1.0);
    UVs = texCoords;
}
'''

#-----------------------------------
#Fragment Shaders
#-----------------------------------

fragment_shader = '''
#version 450 core

layout(binding = 0) uniform sampler2D tex;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    fragColor = texture(tex, UVs);
}
'''

gourad_shader = '''
#version 450 core

layout(binding = 0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals, -dirLight);
    fragColor = texture(tex, UVs) * intensity;
}
'''

toon_shader = '''
#version 450 core

layout(binding = 0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals, -dirLight);
    
    if (intensity < 0.3)
        intensity = 0.2;
    else if (intensity < 0.66)
        intensity = 0.6;
    else
        intensity = 1.0;
        
    fragColor = texture(tex, UVs) * intensity;
}
'''

chess_shader = '''
#version 450 core

layout(binding = 0) uniform sampler2D tex;

in vec3 outNormals;
in vec3 worldPos;
in vec3 outPosition;

out vec4 fragColor;

float pulse(float val, float dst) {
    return floor(mod(val*dst,1.0)+.5);
}

void main()
{
    vec3 dir = vec3(0,1,0);
  
    vec3 currentPos = outPosition;
  
    const float f = 5.0;

    float bright = pulse(currentPos.x,f) + pulse(currentPos.y,f);

    vec3 color = mod(bright,2.0) > .5 ? vec3(1,1,1) : vec3(0.3,0.3,0.3); 

    float diffuse = .95 + dot(outNormals,dir);
    fragColor = vec4(diffuse * color, 1.0);
}
'''

golden_shader = '''
#version 450 core

layout(binding = 0) uniform sampler2D tex;

in vec3 outNormals;
in vec3 worldPos;
in vec3 outPosition;

uniform float time;

out vec4 fragColor;

vec3 diffuse = vec3(.1,.1,.1);

vec3 ambient = vec3(.83, .62, .06);

vec3 specular = vec3(.05,.05,.05);

float s = 20.0;

vec3 camera = vec3(0.0, 0.0, 1.0);

vec3 phong(in vec3 light)
{
  
  float diffuseWeight =  max( dot(light, outNormals) , 0.0) ;
  vec3 toEye = normalize(camera - worldPos);
  vec3 reflective = reflect(-light, outNormals);
  float sWeight = pow(max(dot(reflective, toEye), 0.0), s);
  return ambient + diffuseWeight * diffuse + specular * sWeight;
}

void main()
{
    vec3 light = vec3(0.0, 1.2, 0.0);
    fragColor = vec4(phong(light), 1.0);
}
'''

disco_shader = '''
#version 450 core

layout(binding = 0) uniform sampler2D tex;

in vec3 outNormals;
in vec3 worldPos;
in vec3 outPosition;

uniform float time;

out vec4 fragColor;

vec3 color() {
  
    vec3 color = vec3(0.0, 0.0, 0.0);
  
    color.x = sin(time * 50.0) * outPosition.x;
    color.y = cos(time * 20.0) * outPosition.y;
    color.z =  sin(time * 50.0) * cos(time * 20.0);
  
    return color;
}

void main()
{
  fragColor = vec4(color(), 1.0);
}
'''

pattern_shader = '''
#version 450 core

layout(binding = 0) uniform sampler2D tex;

in vec3 outNormals;
in vec3 worldPos;
in vec3 outPosition;

uniform float time;

out vec4 fragColor;

vec3 color() {
  
    vec3 color = vec3(0.0,0.0,0.0);
  
    if( abs(mod( abs(outPosition.x), abs(.2 * sin(time) )   )) < .1){
        color.x = 0.45;    
        color.z = 0.86;
    }
  
  
    if( abs(mod(outPosition.y, .2 * sin(time * 2))) < .1){  
        color.y = 0.78;
        color.z = 0.45;
    }

    return color;
}

void main()
{
    fragColor = vec4(color(), 1.0);
}
'''

#-----------------------------------------------------------------------------------------
#vec4 newPos = vec4(position.x, position.y + sin(time + position.x)/2, position.z, 1.0);
""" layout(binding = 0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals, -dirLight);
    intensity = min(1,intensity);
    intensity = max(0,intensity);
    fragColor = texture(tex, UVs) * intensity;
} """