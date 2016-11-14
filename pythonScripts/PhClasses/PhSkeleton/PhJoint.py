import maya.cmds as cmds
import sys

class PhJoint(object):
	

	def __init__(self, name):
		self.shortName = name
		self.position = None

	def getPosition():
		if position == None:
			getPositionFromMaya()
		return position

	def getPositionFromMaya(worldSpace=True):
		self.position =  cmds.xform(
			self.name,
			query=True,
			worldSpace=worldSpace,
			translation=True)

	def getXPosition():
		position = self.getPosition();
		return position[0]

	def getYPosition():
		position = self.getPosition();
		return position[1]

	def getZPosition():
		position = self.getPosition();
		return position[2]
