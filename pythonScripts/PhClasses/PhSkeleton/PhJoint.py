import maya.cmds as cmds
import sys
import pythonScripts.PhClasses.PhUtility.PhPosition as PhPosition;


class PhJoint(object):
    def __init__(self, name):
        self.shortName = name
        self.position = PhPosition()
        
        self.position.getPositionFromMayaObj(mayaObj=name)

    
