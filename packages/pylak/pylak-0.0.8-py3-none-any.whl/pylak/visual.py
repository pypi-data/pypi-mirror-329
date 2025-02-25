
from .refs import globalEngine
import pygame as pg


class Text:

    def __init__(self, text, color=(0,0,0,255)):

        self.color = color
        self.text = text


    def getText(self): 
        return self._text
       
    # function to set value of _age 
    def setText(self, text): 
        self._text = text
        self.textSurface = globalEngine[0].font.render(self._text, False, self.color)
        self.textSize = self.textSurface.get_size()

    # function to delete _age attribute 
    def delText(self): 
        del self._text

    text = property(getText, setText, delText)

    def draw(self, x, y, texture=None):
        """
        Tegn teksten i (x,y)
        Hvis texture er givet tegnes teksten til den texture. Ellers tegnes den bare
        til skærmen
        """

        screen, camera = globalEngine[0].screen, globalEngine[0].camera
        x, y = camera.pos(x, y)
        pos = (x, globalEngine[0]._height-y-self.textSize[1])

        if texture:
            self.texture.blit(texture, pos)
            return

        globalEngine[0].screen.blit(self.textSurface, pos)


class Image:

    def __init__(self, image):
        self.image = image
        self.imageSize = (0,0)

    def draw(self, x, y, texture=None):
        
        screen, camera = globalEngine[0].screen, globalEngine[0].camera
        x, y = camera.pos(x, y)
        pos = (x, globalEngine[0]._height-y-self.imageSize[1])

        if texture is None:
            texture = screen
        
        texture.blit(self.image, pos)


    def open(fpath):
        return Image(pg.image.load(fpath))


    def getSize(self):
        return self.image.get_size()


    def setSize(self, size:tuple|list):
        self.image = pg.transform.smoothscale(self.image, size)

    size = property(getSize, setSize)


class Rectangle:

    def __init__(self, width, height, color=(0,0,0,255)):
        self.color = color
        self.width = width
        self.height = height


    def draw(self, x, y, texture=None):
        """
        
        """

        screen, camera = globalEngine[0].screen, globalEngine[0].camera

        x, y = camera.pos(x, y)
        
        pos = (x, globalEngine[0]._height-y-self.height)

        if texture is None:
            texture = screen

        pg.draw.rect(texture, self.color, [*pos, self.width, self.height])


class Circle:

    def __init__(self, radius, color=(0,0,0,255)):

        self.color = color
        self.radius = radius

    def draw(self, x, y, texture=None):
        """
        
        """
        screen, camera = globalEngine[0].screen, globalEngine[0].camera

        x, y = camera.pos(x, y)
        pos = (x+self.radius, globalEngine[0]._height-y-self.radius)

        if texture is None:
            texture = screen

        pg.draw.circle(texture, self.color, pos, self.radius)
