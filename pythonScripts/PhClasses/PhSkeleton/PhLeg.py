import maya.cmds as cmds
import sys

from pythonScripts.PhClasses.PhSkeleton.PhJoint import PhJoint


class PhLeg(object):
    def __init__(self):
        self.hip = None
        self.knee = None
        self.ankle = None
        self.ball = None
        self.toe = None

        self.rfHeel = None
        self.rfToe = None
        self.rfBall = None
        self.rfAnkle = None

    def setHip(self, hipName):
        self.hip = PhJoint(hipName)

    def setKnee(self, kneeName):
        self.knee = PhJoint(kneeName)

    def setAnkle(self, ankleName):
        self.hip = PhJoint(ankleName)

    def setBall(self, ballName):
        self.knee = PhJoint(ballName)

    def setToe(self, toeName):
        self.knee = PhJoint(toeName)
