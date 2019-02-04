class Pedestrian:
    def __init__(self, x, y, age):
        self.x = x
        self.y = y
        self.age = age
    
    def getXCoord(self):
        return self.x
    
    def setXCoord(self, xCoord):
        self.x = xCoord

    def getYCoord(self):
        return self.y

    def setYCoord(self, yCoord):
        self.y = yCoord

    def getAge(self):
        return self.age

    def setAge(self):
        self.age += 1

    def updatePosition(self, xn, yn):
        self.x = xn
        self.y = yn