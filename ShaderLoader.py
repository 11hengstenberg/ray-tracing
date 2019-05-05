#Universidad del Valle de Guatemala
#Graficas por Computadora
#Alexis Fernando Hengstenberg Chocooj
#carne 17699
#proyecto2 Graficas
#camara en movimiento


#importamos librerias
from OpenGL.GL import *
import OpenGL.GL.shaders


#cargamos el shader
def load_shader(shader_file):
    shader_source = ""
    with open(shader_file) as f:
        shader_source = f.read()
    f.close()
    return str.encode(shader_source)

#compilamos el shader
def compile_shader(vs, fs):
    vert_shader = load_shader(vs)
    frag_shader = load_shader(fs)

    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vert_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(frag_shader, GL_FRAGMENT_SHADER))
    return shader
#tutoriales en https://www.youtube.com/watch?v=VMsHs7ARv0U
