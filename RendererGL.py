import pygame
from pygame.locals import *
import glm
from gl import Renderer
from model import Model
from OpenGL.GL import *
from shaders import *

width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)

clock = pygame.time.Clock()

rend = Renderer(screen)

rend.setShaders(complex_shader, fragment_shader)

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

#---------------------------------------------------------------
#Montaje de lista con renderizado de figuras

modelList = [rend.loadModel(filename = "axe.obj", texture = "axe.bmp", position = (0,-2,-5)),
             rend.loadModel(filename = "hand.obj", texture = "skin.bmp", position = (0,-1.5,-5), scale = (0.1,0.1,0.1)),
             rend.loadModel(filename = "vpot.obj", texture = "terracota.bmp", position = (0,-1.5,-5), scale = (0.2,0.2,0.2)),
             rend.loadModel(filename = "notepad.obj", texture = "notepad.bmp", position = (0,-2,-5), scale = (0.15,0.15,0.15))
             ]

token = 0

rend.scene.append(modelList[token])

isRunning = True

r = 5
theta = 0.0

while isRunning:
    
    deltaTime = clock.tick(60)/1000
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_SPACE:
                rend.toggleFilledMode()
                
            elif event.key == pygame.K_1:
                token = 0
            elif event.key == pygame.K_2:
                token = 1
            elif event.key == pygame.K_3:
                token = 2
            elif event.key == pygame.K_4:
                token = 3
            
            elif event.key == pygame.K_7:
                rend.setShaders(complex_shader, chess_shader)
            elif event.key == pygame.K_8:
                rend.setShaders(complex_shader, golden_shader)
            elif event.key == pygame.K_9:
                rend.setShaders(complex_shader, disco_shader)
            elif event.key == pygame.K_0:
                rend.setShaders(complex_shader, pattern_shader)            
    
    actualModel = modelList[token]
    rend.scene = [actualModel]
    
    rend.target = actualModel.position
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    #5 unidades por segundo
    if keys[K_d]:
        theta += 0.3 * deltaTime
        rend.camPosition.x = actualModel.position.x + r * glm.cos(theta)
         
    elif keys[K_a]:
        theta -= 0.3 * deltaTime
        rend.camPosition.x = actualModel.position.x + r * glm.cos(theta)
    
    if keys[K_w]:
        theta += 0.3 * deltaTime
        rend.camPosition.y = actualModel.position.x + r * glm.sin(theta)
         
    elif keys[K_s]:
        theta -= 0.3 * deltaTime
        rend.camPosition.y = actualModel.position.x + r * glm.sin(theta)
            
    if keys[K_q]:
        if rend.camPosition.z > -1.7:
            rend.camPosition.z -= 5 * deltaTime
            
    elif keys[K_e]:
        if rend.camPosition.z < 1.7:
            rend.camPosition.z += 5 * deltaTime
        
    #actualModel.rotation.y += 45 * deltaTime
    
    if keys[K_RIGHT]:
        actualModel.rotation.y += 45 * deltaTime 
         
    elif keys[K_LEFT]:
        actualModel.rotation.y -= 135 * deltaTime #135 con rotacion constante
        
    if keys[K_f]:
        if rend.fatness <1.0:
            rend.fatness += 1 *deltaTime
            
    elif keys[K_t]:
        if rend.fatness >0.0:
            rend.fatness -= 1 *deltaTime
            
    rend.elapsedTime += deltaTime
        
    rend.update()
    rend.render()
    
    pygame.display.flip()

pygame.quit()