
import pyglet as pgl

###########################################
# Collider 
###########################################
class Collider:
    
    def __init__(self, x, y, width, height, referenceObject):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pgl.shapes.Rectangle(x, y, width, height, color=(255, 0, 0))

        self.referenceObject = referenceObject


    def draw(self):
        self.rect.x = self.x
        self.rect.y = self.y

        self.rect.draw()


    def isColliding(self, other):
        isColliding = not (self.x + self.width < other.x or
                self.x > other.x + other.width or
                self.y + self.height < other.y or
                self.y > other.y + other.height)

        if isColliding:
            self.rect.color = (255, 0, 0)
        else:
            self.rect.color = (0, 0, 255)

        return isColliding
