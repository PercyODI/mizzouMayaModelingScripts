import maya.cmds as cmds
import sys
import pythonScripts.PhClasses.PhExceptions.PhMayaError as PhMayaError

class PhPosition(object):
    def __init__(self, rawPosition=None, attachedName=None):
        self.attachedName = attachedName

        if isinstance(rawPosition, tuple):
            self.updatePosition(rawPosition)
        elif isinstance(attachedName, basestring):
            self.getPositionFromMayaObj(attachedName)
        else:
            self.x = None
            self.y = None
            self.z = None

    def attachName(self, name):
        if isinstance(name, basestring):
            self.attachedName = name

    def unattachName(self):
        self.attachName = None

    def getTuple(self):
        return (self.x, self.y, self.z)

    def updatePosition(self, rawPosition):
        if isinstance(rawPosition, tuple):
            self.x = rawPosition[0]
            self.y = rawPosition[1]
            self.z = rawPosition[2]
        
    def getPositionFromMayaObj(self, mayaObj=None, worldSpace=True):
        if !isinstance(mayaObj, basestring): # If mayaObj is None or not a string
            if self.attachedName is not None: # Attempt to use the positions attached name
                mayaObj = attachedName
            else:
                raise ValueError("Cannot determine maya object name") # Otherwise, don't bother calling maya
        else: 
            raise TypeError("mayaObj must be a string!")

        try:
            rawPosition = cmds.xform(
                mayaObj,
                query=True,
                worldSpace=worldSpace,
                translation=True)
            self.updatePosition(rawPosition)
        except Exception:
            raise PhMayaError("Error getting raw position. Attempted xform")

    def getXPosition(self):
        if self.x != None and isinstance(self.x, float):
            return self.x
        else:
            raise ValueError("Missing Value for x")

    def getYPosition(self):
        if self.y != None and isinstance(self.y, float):        
            return self.y
        else:
            raise ValueError("Missing Value for y")

    def getZPosition(self):
        if self.z != None and isinstance(self.z, float):        
            return self.z
        else:
            raise ValueError("Missing Value for z")