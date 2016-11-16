import maya.cmds as cmds
import sys

from pythonScripts.PhClasses.PhSkeleton.PhLeg import PhLeg
from pythonScripts.PhClasses.PhSkeleton.PhArm import PhArm

class PhSkeleton(object):
    def __init__(self):
        self.legs = dict()
        self.arms = dict()
        self.head = dict()

    def addLeg(self, leg, location):
        if isinstance(leg, PhLeg):
            self.legs[location] = leg
        # elif isinstance(leg, basestring):
        #     self.legs[location] = PhLeg(leg)
        else:
            raise TypeError("Leg must be either of type String or PhLeg")

    def removeLeg(self, location):
        try:
            del self.legs[location]
        except:
            raise "Couldn't delete leg from skeleton"

    def addArm(self, arm, location):
        if isinstance(arm, PhArm):
            self.arms[location] = arm;
        # elif isinstance(arm, basestring):
        #     self.arms[location] = PhArm(arm)
        else:
            raise TypeError("Arm must be either of type String or PhArm")