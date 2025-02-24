
from .engine import Engine
from .collider import Collider
from .physics import PhysicsObject
from .visual import Rectangle


class ControllablePlayer:

    def __init__(self, engine:Engine, x=300, y=300, w=50, h=50, mass=60, maxSpeed=1000):
        self.x = y
        self.y = x
        self.w = w
        self.h = h

        # F-v*c=0
        # F=v*c
        # F/v=c
        self.force = 2*10**6
        self.drag = self.force/maxSpeed

        self.rect = Rectangle(w, h, color=(198, 39, 114))
        self.collider = Collider(x, y, w, h, self)
        self.physics = PhysicsObject(self, self.w, self.h, mass, friction=1)

        # reference
        self.engine = engine
        
        self.physics.addVelocityFunction(self.__velocityFunction__)

    
    def __velocityFunction__(self):
        # tilføjer maks hastighed

        max_velocity = 200
        if self.physics.speed > max_velocity:
            scale = max_velocity / self.physics.speed
            return self.physics.velocity * scale


    def draw(self):
        self.rect.draw(self.x, self.y)


    def update(self):
        
        # bevæg den
        if self.engine.isKeyPressed('w'):
            self.physics.addForce(0, self.force)

        if self.engine.isKeyPressed('s'):
            self.physics.addForce(0, -self.force)
        
        if self.engine.isKeyPressed('a'):
            self.physics.addForce(-self.force, 0)
        
        if self.engine.isKeyPressed('d'):
            self.physics.addForce(self.force, 0)

        if self.physics.speed > 0:
            drag = -self.drag * self.physics.velocity
            self.physics.addForce(*drag)

