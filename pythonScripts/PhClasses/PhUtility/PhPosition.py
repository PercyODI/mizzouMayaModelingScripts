import sys;

class PhPosition(object):
    def __init__(self, rawPosition=None):
        if isinstance(rawPosition, tuple):
            self.x = rawPosition[0]
            self.y = rawPosition[1]
            self.z = rawPosition[2]
        else:
            self.x = None
            self.y = None
            self.z = None

    def getTuple(self):
        return (self.x, self.y, self.z)

    def updatePosition(self, rawPosition):
        self.x = rawPosition[0]
        self.y = rawPosition[1]
        self.z = rawPosition[2]
        