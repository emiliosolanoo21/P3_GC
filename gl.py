#No se necesita libreria de mate propia
#pip install PyGLM
#Libreria matematica compatible con OpenGL.

from typing import Self
import glm
from obj import Obj
from model import Model

#pip install PyOpenGL

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        
        _, _, self.width, self.height = screen.get_rect()
        
        self.clearColor = [0,0,0]
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glViewport(0,0,self.width, self.height)
        
        self.elapsedTime = 0.0
        
        self.target = glm.vec3(0,0,0)
        
        self.fatness = 0.0
        
        self.filledMode = True

        self.scene = []
        
        self.activeShader = None
        
        self.dirLight = glm.vec3(1,0,0)
        
        #View Matrix
        self.camPosition = glm.vec3(0,0,0)
        self.camRotation = glm.vec3(0,0,0)
        self.viewMatrix = self.update()      

        #Projection Matrix
        self.projectionMatrix = glm.perspective(glm.radians(60),            #FOV
                                                self.width/self.height,     #Aspect Ratio
                                                0.1,                        #Near Plane
                                                1000)                       #Far Plane
    
    def toggleFilledMode(self):
        self.filledMode = not self.filledMode
        
        if self.filledMode:
            glEnable(GL_CULL_FACE)
            glPolygonMode(GL_FRONT, GL_FILL)
        else:
            glDisable(GL_CULL_FACE)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            
    def getViewMatrix(self):
        identity = glm.mat4(1)
        
        translateMat = glm.translate(identity, self.camPosition)
        
        #Rotation X - Pitch
        #Rotation Y - Yaw
        #Rotation Z - Roll
        
        pitch = glm.rotate(identity, glm.radians(self.camRotation.x), glm.vec3(1,0,0))
        yaw = glm.rotate(identity, glm.radians(self.camRotation.y), glm.vec3(0,1,0))
        roll = glm.rotate(identity, glm.radians(self.camRotation.z), glm.vec3(0,0,1))
        
        rotationMat  = pitch*yaw*roll
        
        camMatrix = translateMat*rotationMat
        
        return glm.inverse(camMatrix)
        
    def setShaders(self, vertexShader, fragmentShader):
        if vertexShader is not None and fragmentShader is not None:
            self.activeShader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
                                               compileShader(fragmentShader, GL_FRAGMENT_SHADER))
        else:
            self.activeShader = None
    

    def update(self):
        #self.viewMatrix = self.getViewMatrix()
        self.viewMatrix = glm.lookAt(self.camPosition, self.target, glm.vec3(0,1,0))
        
    def loadModel(self, filename, texture, position = (0,0,-5), rotation = (0,0,0), scale = (1,1,1)):
        model = Obj(filename)
        
        objectData = []

        for face in model.faces:
            # Revisamos cuantos vertices tiene esta cara. Si tiene cuatro
            # vertices, hay que crear un segundo triangulo por cara
            vertCount = len(face)

            # Obtenemos los vertices de la cara actual.
            v0 = model.vertices[ face[0][0] - 1]
            v1 = model.vertices[ face[1][0] - 1]
            v2 = model.vertices[ face[2][0] - 1]
            if vertCount == 4:
                v3 = model.vertices[ face[3][0] - 1]
                
            # Obtenemos las coordenadas de textura de la cara actual
            vt0 = model.texcoords[face[0][1] - 1]
            vt1 = model.texcoords[face[1][1] - 1]
            vt2 = model.texcoords[face[2][1] - 1]
            if vertCount == 4:
                vt3 = model.texcoords[face[3][1] - 1]
                
            #Obtenemos las normales de la cara actual.
            vn0 = model.normals[face[0][2] - 1]
            vn1 = model.normals[face[1][2] - 1]
            vn2 = model.normals[face[2][2] - 1]
            if vertCount == 4:
                vn3 = model.normals[face[3][2] - 1]
                
            [objectData.append(i) for i in v0]
            [objectData.append(vt0[i]) for i in range (2)]
            [objectData.append(i) for i in vn0]
            
            [objectData.append(i) for i in v1]
            [objectData.append(vt1[i]) for i in range (2)]
            [objectData.append(i) for i in vn1]

            [objectData.append(i) for i in v2]
            [objectData.append(vt2[i]) for i in range (2)]
            [objectData.append(i) for i in vn2]
            
            if vertCount == 4:
                [objectData.append(i) for i in v0]
                [objectData.append(vt0[i]) for i in range (2)]
                [objectData.append(i) for i in vn0]
            
                [objectData.append(i) for i in v2]
                [objectData.append(vt2[i]) for i in range (2)]
                [objectData.append(i) for i in vn2]

                [objectData.append(i) for i in v3]
                [objectData.append(vt3[i]) for i in range (2)]
                [objectData.append(i) for i in vn3]
        
        newModel = Model(objectData)
        newModel.loadTexture(texture)
        newModel.position = glm.vec3(position)
        newModel.rotation = glm.vec3(rotation)
        newModel.scale = glm.vec3(scale)

        self.scene.append(newModel)
        
        return newModel

    def render(self):
        glClearColor(self.clearColor[0], self.clearColor[1], self.clearColor[2], 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        if self.activeShader is not None:
            glUseProgram(self.activeShader)
            
            glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "viewMatrix"),
                               1, GL_FALSE, glm.value_ptr(self.viewMatrix))
            
            glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "projectionMatrix"),
                               1, GL_FALSE, glm.value_ptr(self.projectionMatrix))

            glUniform1f(glGetUniformLocation(self.activeShader, "time"), self.elapsedTime)
            glUniform1f(glGetUniformLocation(self.activeShader, "fatness"), self.fatness)
            
            glUniform3fv(glGetUniformLocation(self.activeShader, "dirLight"), 1, glm.value_ptr(self.dirLight))
                    
        for obj in self.scene:
            if self.activeShader is not None:
                glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "modelMatrix"),
                                   1, GL_FALSE, glm.value_ptr(obj.getModelMatrix()))
                    
            obj.render()
            