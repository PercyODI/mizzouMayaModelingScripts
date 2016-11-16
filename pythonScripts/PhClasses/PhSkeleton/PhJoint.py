import maya.cmds as cmds
import sys
import pythonScripts.PhClasses.PhUtility.PhPosition as PhPosition;


class PhJoint(object):
    def __init__(self, name):
        self.shortName = name
        self.position = None

    def setPosition(self):
        if self.position == None:
            self.getPositionFromMaya()

    def getPositionFromMaya(self, worldSpace=True):
        self.position = cmds.xform(
            self.name,
            query=True,
            worldSpace=worldSpace,
            translation=True)

    def getXPosition(self):
        position = self.getPosition();
        return position[0]

    def getYPosition(self):
        position = self.getPosition();
        return position[1]

    def getZPosition(self):
        position = self.getPosition();
        return position[2]
