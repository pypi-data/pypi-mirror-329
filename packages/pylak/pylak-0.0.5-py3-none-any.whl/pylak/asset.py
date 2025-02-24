
from PIL import Image
import pygame as pg


class AssetCollection:

    def __init__(self, fpath:str, width:int, height:int):
        self.image = Image.open(fpath)
        self.width = width
        self.height = height

        self.widthPerRegion = self.image.width/self.width
        self.heightPerRegion = self.image.height/self.height


    def get(self, x, y):
        """
        burde ikke køre i loops
        """

        spriteSheet = self.image.crop((
            x * self.widthPerRegion, 
            y * self.heightPerRegion,
            (x + 1) * self.widthPerRegion,
            (y + 1) * self.heightPerRegion,
        ))
        rawImage = spriteSheet.tobytes()
        spriteSheet = pg.image.frombytes(rawImage, (spriteSheet.width, spriteSheet.height), 'RGBA')

        return spriteSheet

