
"""
Mål:
    Lav nogle hurtig assets som eleven kan hente ind
    Assets burde være plug and play

"""

import pygame as pg
from .refs import globalEngine
from .visual import Image

class Tilemap:
    """
    Tilemap består af flere forskellige tiles
    """

    def __init__(self, tiles:tuple, size:tuple, static:bool=False):
        self.width = tiles[0]
        self.height = tiles[1]
        self.tiles = []
        self.x = 0
        self.y = 0
        self.static = static

        self.size = size

        self.tileSizes = (
            self.size[0]/self.width,
            self.size[1]/self.height
        )

        # create one image
        if static:

            pass
            # self.image = pgl.image.create(*size)
            
    
    def create(self, image, pos):
        x, y = (
            pos[0]*self.tileSizes[0], 
            pos[1]*self.tileSizes[1]
        )
        tile = Tile(image, x, y, *self.tileSizes)

        self.tiles.append(tile)

        if self.static:
            
            pass
            # texture.blit_into(self.image, *pos, 0)

    
    def draw(self, x, y):
        
        if self.static and False:
            pass
        
        else:
            
            for tile in self.tiles:
                tile.draw(x, y)


class Tile:

    def __init__(self, image, x, y, width, height):
        self.x = x
        self.y = y

        self.width = width
        self.height = height
        
        self.image = Image(image)
        self.image.size = (self.width, self.height)


    def draw(self, ox, oy, texture=None):

        if not texture:
            texture = globalEngine[0].screen
        
        self.image.draw(self.x+ox,self.y+oy, texture)