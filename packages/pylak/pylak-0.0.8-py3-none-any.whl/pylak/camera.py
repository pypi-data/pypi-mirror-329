

class Camera:

    def __init__(self, engine):
        self.x = 0
        self.y = 0
        self.engine = engine
        self.limits = None


    def pos(self, x, y):
        return x+self.x, y+self.y


    def setLimit(self, x, y, w, h):
        self.limits = [x,y, w, h]


    def checkLimit(self):
        if self.limits is None:
            return

        self.x = min(max(self.x, -self.limits[2]+self.engine._width), self.limits[0])
        self.y = min(max(self.y, -self.limits[3]+self.engine._height), self.limits[1])


    def follow(self, ox, oy, margin=100):
        x, y = self.pos(ox, oy)
        
        if x < margin:
            self.x -= x - margin
            
        if x > self.engine._width - margin:
            self.x -= x - self.engine._width + margin
        
        if y < margin:
            self.y -= y - margin

        if y > self.engine._height - margin:
            self.y -= y - self.engine._height + margin
        
        self.checkLimit()

    
    def center(self, x, y):
        self.x = -x + self.engine._width//2
        self.y = -y + self.engine._height//2

        self.checkLimit()


    def shake(self):
        """
        virker ikke 🚧🚧🚧
        """


    def zoom(self):
        """
        virker ikke 🚧🚧🚧
        """
