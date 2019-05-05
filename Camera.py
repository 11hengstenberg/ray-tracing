#Universidad del Valle de Guatemala
#Graficas por Computadora
#Alexis Fernando Hengstenberg Chocooj
#carne 17699
#proyecto2 Graficas
#camara en movimiento

from pyrr import *
from math import sin, cos, radians


class Camera:
    def __init__(self):
        #pisitcion de la camara
        self.camera_pos = Vector3([0.0, 2.0, 20.0])
        #frontal de la macara
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        #altura de la camara
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        #derecha camara
        self.camera_right = Vector3([1.0, 0.0, 0.0])


        #mause
        self.mouse_sensitivity = 0.15
        self.yaw = -90.0
        self.pitch = 0.0


        #matrix
    def get_view_matrix(self):
        return self.look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

        #movimiento con el teclado.
    def process_keyboard(self, direction, velocity):


        #avanzar
        if self.camera_pos[2]>= 16 and self.camera_pos[0]>=-7.9 and self.camera_pos[0]<=7.9 :
            if direction == "FORWARD":
                self.camera_pos += self.camera_front * velocity
        #retroceder
        if self.camera_pos[2]<=40 and self.camera_pos[0]>=-7.9  and self.camera_pos[2]>- 16 :
                if direction == "BACKWARD":
                    self.camera_pos -= self.camera_front * velocity
        #izquierda
        if self.camera_pos[0]>=-8 and self.camera_pos[2]>= 15 :
                if direction == "LEFT":
                    self.camera_pos -= self.camera_right * velocity
        #derecha
        if self.camera_pos[0]<=8 and self.camera_pos[2]>= 15 :
            if direction == "RIGHT":
                self.camera_pos += self.camera_right * velocity


        #movimiento del mouse_sensitivity
        #https://www.youtube.com/watch?v=VMsHs7ARv0U tutoriales
    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 45.0:
                self.pitch = 45.0
            if self.pitch < -45.0:
                self.pitch = -45.0

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        front.z = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0])))

    def look_at(self, position, target, world_up):
        
        # 1.Posicion
        # 2.Calcular direccion de camara
        zaxis = vector.normalise(position - target)
        # 3.posicion a la izquierda
        xaxis = vector.normalise(vector3.cross(vector.normalise(world_up), zaxis))
        # 4.calcular el vector de la camara
        yaxis = vector3.cross(zaxis, xaxis)

        # traslacion y rotacion de matrices
        translation = Matrix44.identity()
        translation[3][0] = -position.x
        translation[3][1] = -position.y
        translation[3][2] = -position.z

        rotation = Matrix44.identity()
        rotation[0][0] = xaxis[0]
        rotation[1][0] = xaxis[1]
        rotation[2][0] = xaxis[2]
        rotation[0][1] = yaxis[0]
        rotation[1][1] = yaxis[1]
        rotation[2][1] = yaxis[2]
        rotation[0][2] = zaxis[0]
        rotation[1][2] = zaxis[1]
        rotation[2][2] = zaxis[2]

        return translation * rotation

#tutoriales en https://www.youtube.com/watch?v=VMsHs7ARv0U
