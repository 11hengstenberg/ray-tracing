#Universidad del Valle de Guatemala
#Graficas por Computadora
#Alexis Fernando Hengstenberg Chocooj
#carne 17699
#proyecto2 Graficas
#camara en movimiento




#importamos libreria numpy
#matrices
import numpy as np


#creamos la clase OBJLoader
#para cargar el obj
class ObjLoader:
    def __init__(self):

        self.vert_coords = []
        self.text_coords = []
        self.norm_coords = []
        self.vertex_index = []
        self.texture_index = []
        self.normal_index = []
        self.model = []



        #funcion para cargar el modeloo obj
    def load_model(self, file):
        #leemos el archivo
        for line in open(file, 'r'):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue

            #vertices
            if values[0] == 'v':
                self.vert_coords.append(values[1:4])

            if values[0] == 'vt':
                self.text_coords.append(values[1:3])

            #vectores normales
            if values[0] == 'vn':
                self.norm_coords.append(values[1:4])


            #caras
            if values[0] == 'f':
                face_i = []
                text_i = []
                norm_i = []
                for v in values[1:4]:
                    #separadas por una diagonal
                    w = v.split('/')
                    face_i.append(int(w[0])-1)
                    text_i.append(int(w[1])-1)
                    norm_i.append(int(w[2])-1)
                self.vertex_index.append(face_i)
                self.texture_index.append(text_i)
                self.normal_index.append(norm_i)

        self.vertex_index = [y for x in self.vertex_index for y in x]
        self.texture_index = [y for x in self.texture_index for y in x]
        self.normal_index = [y for x in self.normal_index for y in x]

        for i in self.vertex_index:
            self.model.extend(self.vert_coords[i])

        for i in self.texture_index:
            self.model.extend(self.text_coords[i])

        for i in self.normal_index:
            self.model.extend(self.norm_coords[i])

        self.model = np.array(self.model, dtype='float32')


#tutorial en https://www.youtube.com/watch?v=VMsHs7ARv0U
