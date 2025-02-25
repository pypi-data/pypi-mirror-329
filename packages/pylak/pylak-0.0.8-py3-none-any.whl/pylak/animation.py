
"""

References

https://pyglet.readthedocs.io/en/latest/programming_guide/image.html#animations

For some reason binding animations to texture atlas creates problems

"""

from .visual import Image
from .asset import AssetCollection
import pygame as pg
from time import time

class Animation:

    def __init__(self, images:list[Image], period, size):
        self.images = images
        self.currentIndex = 0
        self.__last = time()
        self.period = period
    
    def draw(self, x, y, texture=None):
        if time() - self.__last > self.period:
            self.currentIndex += 1
            self.__last = time()

        self.images[self.index].draw(x,y,texture)

    @property
    def index(self):
        return self.currentIndex%len(self.images)


class Animations:

    
    def __addAnimationState__(self, 
                                assetCollection:AssetCollection, 
                                row, 
                                period,
                                size,
                                flipx=False,
                                flipy=False
                              ):

        # chop images into diffrent textures
        images = [assetCollection.get(col, row) for col in range(assetCollection.width)]
        
        for i, frame in enumerate(images):
            images[i] = Image(pg.transform.flip(frame, flipx, flipy))
            images[i].size = (size, size)

        return Animation(images, period, size)


    def __init__(self, assetCollection:AssetCollection, period=1/15, size=100):
        """
        uses center pos
        """

        self.size = size
        
        self.cols = assetCollection.width
        self.rows = assetCollection.height

        self.animations = {
            "default":[],
            "flipx":[],
            "flipy":[]
        }

        self.collection = assetCollection

        self._forceNext = None
        self._forceNextActive = False

        for i in range(self.rows):

            self.animations["default"].append(self.__addAnimationState__(
                assetCollection, 
                i, 
                period, 
                self.size,
            ))

        for i in range(self.rows):

            self.animations["flipx"].append(self.__addAnimationState__(
                assetCollection, 
                i, 
                period,
                self.size,
                flipx=True
            ))
        
        for i in range(self.rows):

            self.animations["flipy"].append(self.__addAnimationState__(
                assetCollection, 
                i, 
                period,
                self.size,
                flipy=True
            ))

        self._currentAnimation = [0, 'default']
        self._nextAnimationIndex = 0
        self._reachedEndOfCycle = False
        
        self.x = 0 # center pos
        self.y = 0



    def open(fpath, width:int, height:int, period=1/15, size=100):
        return Animations(AssetCollection(fpath, width, height), period, size)


    def switch(self, index:int, flipx:bool=False, flipy:bool=False):
        """
        Bruges til states
        """
        
        if flipx and flipy:
            raise NotImplemented('Both flips can not happened at once')

        state = 'default'
        if flipx: state = 'flipx'
        if flipy: state = 'flipy'

        self._nextAnimationIndex = index
        self._currentAnimation[1] = state


    def do(self, index:int, flipx:bool=False, flipy:bool=False):
        
        self.switch(index, flipx, flipy)

        self._forceNext = self._nextAnimationIndex


    def draw(self, x, y):

        
        index, state = self._currentAnimation

        sprite:Image = self.animations[state][index]
        sprite.x = x + (state == "flipx") * self.size - self.size/2
        sprite.y = y + (state == "flipy") * self.size - self.size/2

        # denne burde kun køre en gang per cyklus men bliver kørt flere gange 
        # hver gang der tegnes og man er på det sidste frame
        if sprite.index == self.cols - 1 and not self._reachedEndOfCycle:
            
            # hvis der er en ny forced animation som ikke er igang
            if self._forceNext and not self._forceNextActive:
                # så skal den sættes på nu, da animations cyklussen er klar 
                self._forceNextActive = True
                self._currentAnimation[0] = self._forceNext
            
            # hvis den forced animation er der og har været igang
            elif self._forceNext and self._forceNextActive:
                # så skal den sættes fjerens nu da animationen er done
                self._forceNext = None
                self._forceNextActive = False
                self._currentAnimation[0] = self._nextAnimationIndex

            # hvis der ingen forced er
            else:
                self._currentAnimation[0] = self._nextAnimationIndex
            
        self._reachedEndOfCycle = sprite.index == self.cols - 1

        sprite.draw(x, y + self.size)
