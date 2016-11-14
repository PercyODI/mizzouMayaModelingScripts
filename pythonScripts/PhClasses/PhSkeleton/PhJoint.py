import maya.cmds as cmds
import sys

class PhJoint(object):
	

	def __init__(self, name):
		self.shortName = name
		self.position = None

	def getPosition():
		if position == None:
			findPos()
		return position

	def findPosition(worldSpace=True):
		self.position =  cmds.xform(
				self.name,
				query=True,
				worldSpace=worldSpace,
				translation=True)

