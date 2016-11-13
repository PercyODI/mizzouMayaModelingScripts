import maya.cmds as cmds;
import sys;
import re;

# Find the currently selected object
selection = cmds.ls(selection=True);
# Add all of the currently selected object's decendants to selection
selection.extend(reversed(cmds.listRelatives(selection, allDescendents=True)))
# Filters the selection to only joints
selection = cmds.ls(selection, type="joint")

legPattern = re.compile('^(?P<location>\w+?)(?:_| |)(?P<name>Hip|Knee|Ankle|Ball|Toe)$')
legsDict = dict(); # Creates a dictionary of legs by location.

# ?? Use re.compile ??
# http://stackoverflow.com/questions/28856238/how-to-get-group-name-of-match-regular-expression-in-python

# Creates a 2d dictionary. The first key is the location of the leg (L, Right, etc)
# The second key is matched with the joint name. This allows riggers to name the leg
# by any arbitrary location name, as long as the joint name is one of the list given in the pattern
for joint in selection:
	regexMatch = legPattern.match(joint)
	if(regexMatch):
		jointLocation = regexMatch.groupdict()['location']
		jointName = regexMatch.groupdict()['name']
		if jointLocation in legsDict:
			legsDict[jointLocation][jointName] = joint
		else:
			legsDict[jointLocation] = dict()
			legsDict[jointLocation][jointName] = joint
for location in legsDict:
	# Create the ikHandles for the leg
	AnkleIK = cmds.ikHandle(
		name="AnkleIK",
		startJoint=legsDict[location]["Hip"],
		endEffector=legsDict[location]["Ankle"])
	BallIK = cmds.ikHandle(
		name="BallIK",
		startJoint=legsDict[location]["Ankle"],
		endEffector=legsDict[location]["Ball"])
	ToeIK = cmds.ikHandle(
		name="ToeIK",
		startJoint=legsDict[location]["Ball"],
		endEffector=legsDict[location]["Toe"])

	# Create Reverse Foot Joints

	# Find the positions of ankle, ball, and toe joints
	cmds.select(clear=True);
	anklePosition = cmds.xform(
		legsDict[location]["Ankle"],
		query=True,
		worldSpace=True,
		translation=True)
	ballPosition = cmds.xform(
		legsDict[location]["Ball"],
		query=True,
		worldSpace=True,
		translation=True)
	toePosition = cmds.xform(
		legsDict[location]["Toe"],
		query=True,
		worldSpace=True,
		translation=True)

	# Create new joints at specific positions
	RFHeel = cmds.joint(
		name="RFHeel",
		absolute=True,
		position=(
			anklePosition[0], # X Position
			ballPosition[1],  # Y Position
			anklePosition[2]) # Z Position
		)
	RFToe = cmds.joint(
		name="RFToe",
		absolute=True,
		position=toePosition)
	RFBall = cmds.joint(
		name="RFBall",
		absolute=True,
		position=ballPosition)
	RFAnkle = cmds.joint(
		name="RFAnkle",
		absolute=True,
		position=anklePosition)

	cmds.parent(ToeIK[0], RFToe)
	cmds.parent(BallIK[0], RFBall)
	cmds.parent(AnkleIK[0], RFAnkle)

