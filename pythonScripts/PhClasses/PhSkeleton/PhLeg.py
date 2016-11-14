import maya.cmds as cmds
import sys
import pythonScripts.PhClasses.PhSkeleton.PhJoint as PhJoint

class PhLeg(object):
	def __init__(
		self, hipName = None, kneeName = None, ankleName = None, ballname = None, toeName = None):
		self.hip = hipName != None ? PhJoint(hipName) : None
		self.knee = kneeName != None ? PhJoint(kneeName) : None
		self.ankle = ankleName != None ? PhJoint(ankleName) : None
		self.ball = ballName != None ? PhJoint(ballName) : None
		self.toe = toeName != None ? PhJoint(toeName) : None

		self.rfHeel = None
		self.rfToe = None
		self.rfBall = None
		self.rfAnkle = None

	def setHip(hipName):
		self.hip = PhJoint(hipName)

	def setKnee(kneeName):
		self.knee = PhJoint(kneeName)

	def setAnkle(ankleName):
		self.hip = PhJoint(ankleName)

	def setBall(ballName):
		self.knee = PhJoint(ballName)

	def setToe(toeName):
		self.knee = PhJoint(toeName)
