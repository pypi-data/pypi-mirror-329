
# Den her kode base er en simpel version af en game engine.
# Den er skrevet i Python og bruger Pyglet til at håndtere vinduer og grafik.

import pygame as pg
from typing import DefaultDict
import numpy as np
import math
from time import time
import pymunk
import pymunk.pyglet_util
from .refs import globalEngine
from .visual import Text

pg.init()
pg.font.init()

###########################################
# Engine
# TODO:
# - Smooth scene transitions
###########################################
class Engine:
    def __init__(self, width=600, height=600, caption="Spil"):
        globalEngine[0] = self # use global reference
        pg.display.set_caption(caption)

        self._width = width
        self._height = height
        
        self.screen = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        self._currentScene = None
        # self.__keyNames = {v: k for k, v in pgl.window.key._key_names.items()}

        self._colliders = []
        self._physicsObjects = []
        self._flags = {"debug":False, "debugPhysics":False}

        self.last = time()
        self.frames = 0
        
        self.font = pg.font.SysFont('Times New Roman', 64)

        self.fps_text = Text('Unknown', color=(0,0,0,255))
        self._physicsSpace = pymunk.Space()


    # flags
    def setFlag(self, flag:str, value:bool) -> None:
        self._flags[flag] = value

    def getFlag(self, flag:str) -> bool:
        return self._flags[flag]


    # event handling
    def isKeyPressed(self, key:str) -> bool:

        keyCode = pg.key.key_code(key)
        return pg.key.get_pressed()[keyCode]
        
    
    # collider handling
    def addCollider(self, collider):
        self._colliders.append(collider)
    

    # add physics object
    def addPhysicsObject(self, physicsObject):
        self._physicsSpace.add(physicsObject.body, physicsObject.poly)
        self._physicsObjects.append(physicsObject)

    # get collisions O(1)
    def isColliding(self, collider1, collider2) -> bool:
        return self.collisions[collider1].__contains__(collider2)

    
    # scene handling
    def setCurrentScene(self, scene):
        self._currentScene = scene
        self._colliders = []
        self._physicsObjects = []
        
        self._physicsSpace = pymunk.Space()
        self.__physicsDebugOtions = pymunk.pyglet_util.DrawOptions()
        self.__physicsDebugOtions.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES

        scene.setup()


    def __calculateCollisions__(self):
        
        self.collisions = DefaultDict(set)

        rows = 100
        cols = 100

        w, h = self._width/rows + 1, self._height/cols + 1

        matrix = [[[] for _ in range(cols)] for _ in range(rows)]

        # divide
        for collider in self._colliders:
            
            x0 = int(collider.x / w)
            y0 = int(collider.y / h)

            x1 = int((collider.x + collider.width) / w) + 1
            y1 = int((collider.y + collider.height) / h) + 1

            for x in range(x0, x1):
                for y in range(y0, y1):
                    
                    if x < 0 or x >= cols or y < 0 or y >= rows:
                        continue

                    matrix[x][y].append(collider)

        # check collision
        for x in range(cols):
            
            for y in range(rows):

                colliders = matrix[x][y]

                for i in range(len(colliders)):
                    for j in range(i+1, len(colliders)):
                        if colliders[i].isColliding(colliders[j]):
                            self.collisions[colliders[i]].add(colliders[j])
                            self.collisions[colliders[j]].add(colliders[i])

    # loop
    def __update__(self, dt):
        
        self.__calculateCollisions__()

        steps = 10
        for _ in range(steps):
            self._physicsSpace.step(dt/steps)

        for obj in self._physicsObjects:
            obj.update()

        # i få situationer er der ikke sat en scene
        if self._currentScene:
            self._currentScene.update(dt)
        
        self.fps_text.text = str(round(1/dt))

    
    def __draw__(self):
        
        # i få situationer er der ikke sat en scene
        if self._currentScene:
            self._currentScene.draw()

        if self._flags["debugPhysics"]:
            self._physicsSpace.debug_draw(self.__physicsDebugOtions)

        if self._flags["debug"]:
        
            self.fps_text.draw(0,0)


    def __loop__(self):
        
        running = True
        dt = 1
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            self.screen.fill("white")

            self.__update__(dt/1000)
            self.__draw__()

            pg.display.flip()
            dt = self.clock.tick(60)


    def start(self):
        """
        start loopet og start spillet 🕹️🕹️🕹️

        """

        self.__loop__()
