from OpenGL.GL import *
import glm
from numpy import array, float32

import pygame

class Model(object):
    def __init__(self, data):
        self.vertexBuffer = array(data, dtype= float32)
        
        #Vertex Buffer Object
        self.VBO = glGenBuffers(1)
        
        #Vertex Array Object
        self.VAO = glGenVertexArrays(1)
        
        self.position = glm.vec3(0,0,0)
        self.rotation = glm.vec3(0,0,0)
        self.scale = glm.vec3(1,1,1)
    
    def loadTexture(self, textureName):
        self.textureSurface = pygame.image.load(textureName)
        self.textureData = pygame.image.tostring(self.textureSurface, "RGB", True)
        self.textureBuffer = glGenTextures(1)
        
    def getModelMatrix(self):
        identity = glm.mat4(1)
        
        translateMat = glm.translate(identity, self.position)
        
        #Rotation X - Pitch
        #Rotation Y - Yaw
        #Rotation Z - Roll
        
        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
        yaw = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
        roll = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))
        
        rotationMat = pitch*yaw*roll
        
        scaleMat = glm.scale(identity, self.scale)
        
        return translateMat*rotationMat*scaleMat
         
    def render(self):
        
        #Atar buffers a la GPU
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)
        
        #Especificar info de vertices
        glBufferData(GL_ARRAY_BUFFER,
                     self.vertexBuffer.nbytes,
                     self.vertexBuffer,
                     GL_STATIC_DRAW)
        
        #Atributos
        #Especificar lo que representa el contenido del vertice
        
        #Atributo de posiciones
        glVertexAttribPointer(0,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              4*8,
                              ctypes.c_void_p(0))
    
        glEnableVertexAttribArray(0) 
               
        """ #Atributo de colores
        glVertexAttribPointer(1,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              4*8,
                              ctypes.c_void_p(4*3))
    
        glEnableVertexAttribArray(1) """
        
        #Atributo de coordenadas de textura
        glVertexAttribPointer(1,
                              2,
                              GL_FLOAT,
                              GL_FALSE,
                              4*8,
                              ctypes.c_void_p(4*3))
    
        glEnableVertexAttribArray(1)
        
        #Atributo de normales
        glVertexAttribPointer(2,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              4*8,
                              ctypes.c_void_p(4*5))
    
        glEnableVertexAttribArray(2)
        
        #Activar la textura
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textureBuffer)
        glTexImage2D(GL_TEXTURE_2D,
                     0,
                     GL_RGB,
                     self.textureSurface.get_width(),
                     self.textureSurface.get_height(),
                     0,
                     GL_RGB,
                     GL_UNSIGNED_BYTE,
                     self.textureData)
        
        #glGenerateMipmap(GL_TEXTURE_2D)
        glGenerateTextureMipmap(self.textureBuffer)

        
        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertexBuffer)/8))
        
        