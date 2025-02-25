
import numpy as np
import pymunk
import pymunk.pyglet_util


###########################################
# PhysicsObject
###########################################
class PhysicsObject:

    def __init__(self, object, width, height, mass=10, isRotatable=False, immovable=False):
        
        self.o = object
        self.immovable = immovable
        self.width = width
        self.height = height

        self.mass = mass
        self.isRotatable = isRotatable

        if immovable:
            self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        else:
            self.body = pymunk.Body(self.mass)
    
        self.body.position = self.o.x + self.width/2, self.o.y + self.height/2

        self.poly = pymunk.Poly.create_box(self.body, (self.width, self.height))
        self.poly.mass = self.mass
        
    
    def addForce(self, x, y):
        self.body.apply_force_at_local_point((x,y))

    
    def update(self):
        if not self.isRotatable:
            self.body.angular_velocity = 0
            self.body.angle = 0

        if not self.immovable:
            self.o.x, self.o.y = self.body.position[0] - self.width/2, self.body.position[1] - self.height/2


    @property
    def velocity(self):
        return self.body.velocity

    @property
    def speed(self):
        return self.body.velocity.length


    def getPos(self):
        return self.body.position

    def setPos(self, pos):
        self.body.position = pos

    pos = property(getPos, setPos)


    def __baseVelocityFunction__(self, func, body, gravity, damping, dt):
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        res = func()

        if res:
            body.velocity = res


    def addVelocityFunction(self, func):
        self.body.velocity_func = lambda body, gravity, damping, dt: self.__baseVelocityFunction__(func, body, gravity, damping, dt)