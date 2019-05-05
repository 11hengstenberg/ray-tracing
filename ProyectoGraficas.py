#Universidad del Valle de Guatemala
#Graficas por Computadora
#Alexis Fernando Hengstenberg Chocooj
#carne 17699
#proyecto2 Graficas
#camara en movimiento


#importamos las librerias

#glfw
import glfw
#openGL
from OpenGL.GL import *
#pyrr
from pyrr import matrix44, Vector3, Matrix44
#otras clases
import ShaderLoader
import TextureLoader
from ObjLoader import *
from Camera import Camera


#tamaño de la ventana
def window_resize(window, width, height):
    glViewport(0, 0, width, height)




#camara
cam = Camera()
keys = [False] * 1024
wwidth, wheight = 1920, 1080
ultimaX, ultimaY = wwidth / 2, wheight / 2
mouse1 = True


def key_callback(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key >= 0 and key < 1024:
        if action == glfw.PRESS:
            keys[key] = True
        elif action == glfw.RELEASE:
            keys[key] = False




#lmovimiento por medio del teclado
def do_movement():


    #w hacia enfrente
    if keys[glfw.KEY_W]:
        cam.process_keyboard("FORWARD", 0.05)
    #s hacia atras
    if keys[glfw.KEY_S]:
        cam.process_keyboard("BACKWARD", 0.05)
    #A hacia la izquierda
    if keys[glfw.KEY_A]:
        cam.process_keyboard("LEFT", 0.05)
    #D hacia la derecha
    if keys[glfw.KEY_D]:
        cam.process_keyboard("RIGHT", 0.05)


#movimiento rotatorio con el mouse
def mouse_callback(window, xpos, ypos):


    global mouse1, ultimaX, ultimaY

    if mouse1:
        ultimaX = xpos
        ultimaY = ypos
        mouse1 = False
    xoffset = xpos - ultimaX
    yoffset = ultimaY - ypos
    ultimaX = xpos
    ultimaY = ypos
    cam.process_mouse_movement(xoffset, yoffset)


def main():


    # comenzar glfw
    if not glfw.init():
        return

    aspect_ratio = wwidth / wheight
    #creamos la ventana
    window = glfw.create_window(wwidth, wheight, "ProyectoGraficas", None, None)

    #terminar ventana
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)


    glfw.set_window_size_callback(window, window_resize)

    glfw.set_key_callback(window, key_callback)

    glfw.set_cursor_pos_callback(window, mouse_callback)

    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)


    #carbamos el primer ObjLoader
    casa = ObjLoader()
    #buscamos el objeto en nuestras carpetas
    casa.load_model("obj/casa2.obj")
    #buscamos la textura en nuestras carpetas
    casa_tex = TextureLoader.load_texture("obj/pared.jpg")
    #calculamos
    casa_texture_offset = len(casa.vertex_index) * 12


    #cargamos el segundo objeto
    monster = ObjLoader()
    #buscamos el obj en nuestras carpetas
    monster.load_model("obj/monster.obj")
    #buscamos la textura en nuestras carpetas
    monster_tex = TextureLoader.load_texture("obj/monster.jpg")
    #calculamos
    monster_texture_offset = len(monster.vertex_index) * 12

    #obtenemos los shaders de nuestras carpetas.
    generic_shader = ShaderLoader.compile_shader("shaders/generic_vertex_shader.vs", "shaders/generic_fragment_shader.fs")




#------------------------------------casa--------------------------------------------------------------------------#
    #generamos nestras variaml
    casavao = glGenVertexArrays(1)

    glBindVertexArray(casavao)

    casavbo = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, casavbo)

    glBufferData(GL_ARRAY_BUFFER, casa.model.itemsize * len(casa.model), casa.model, GL_STATIC_DRAW)




    #posicion
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, casa.model.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)




    #Texturas
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, casa.model.itemsize * 2, ctypes.c_void_p(casa_texture_offset))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)

#--------------------------------------------------------------------------------------------------------------------





#-------------------------------------------------------monstruo------------------------------------------------------#
    monster_vao = glGenVertexArrays(1)

    glBindVertexArray(monster_vao)

    monster_vbo = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, monster_vbo)

    glBufferData(GL_ARRAY_BUFFER, monster.model.itemsize * len(monster.model), monster.model, GL_STATIC_DRAW)


    #position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, monster.model.itemsize * 3, ctypes.c_void_p(0))

    glEnableVertexAttribArray(0)
    #textures
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, monster.model.itemsize * 2, ctypes.c_void_p(monster_texture_offset))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)
#-----------------------------------------------------------------------------------------------------------------------#



#colocamos el color negro


    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)



    projection = matrix44.create_perspective_projection_matrix(45.0, aspect_ratio, 0.1, 100.0)


    #traslacion del vector a la casa2
    #colocar en el lugar
    casaModelo = matrix44.create_from_translation(Vector3([0.0, 0.0, -3.0]))


    #traslacion en el vectro3 al monstruo
    #colocar en el lugar
    monster_model = matrix44.create_from_translation(Vector3([0.0, 0.0, -10.0]))

    #shaders
    glUseProgram(generic_shader)


    model_loc = glGetUniformLocation(generic_shader, "model")

    view_loc = glGetUniformLocation(generic_shader, "view")

    proj_loc = glGetUniformLocation(generic_shader, "proj")


    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


    #mientras la ventana
    while not glfw.window_should_close(window):



        glfw.poll_events()

        do_movement()
        #colocar la ventada de un color especifico
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        view = cam.get_view_matrix()

        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)


        #rotaciones
        rot_y = Matrix44.from_y_rotation(glfw.get_time() * 0.5)



#--------------------------------------casa--------------------------------------#
        glBindVertexArray(casavao)
        glBindTexture(GL_TEXTURE_2D, casa_tex)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, casaModelo)
        glDrawArrays(GL_TRIANGLES, 0, len(casa.vertex_index))
        glBindVertexArray(0)
#--------------------------------------------------------------------------------#


#---------------------------------------monstruo----------------------------------#
        glBindVertexArray(monster_vao)
        glBindTexture(GL_TEXTURE_2D, monster_tex)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, monster_model)
        glDrawArrays(GL_TRIANGLES, 0, len(monster.vertex_index))
        glBindVertexArray(0)
#--------------------------------------------------------------------------------------

    #buffer de la ventana
        glfw.swap_buffers(window)


    #finalizamos
    glfw.terminate()

    #inicializamos
if __name__ == "__main__":
    main()
