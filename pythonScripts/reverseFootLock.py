import maya.cmds as cmds;
import sys;

# Find the currently selected object
selection = cmds.ls(selection=True);
# Add all of the currently selected object's decendants to selection
selection.extend(reversed(cmds.listRelatives(selection, allDescendents=True)))
# Filters the selection to only joints
selection = cmds.ls(selection, type="joint")

hipJoint = u'Hip'
kneeJoint = u'Knee'
ankleJoint = u'Ankle'
ballJoint = u'Ball'
toeJoint = u'Toe'


# Create the ikHandles for the leg
AnkleIK = cmds.ikHandle(
	name="AnkleIK",
	startJoint=hipJoint,
	endEffector=ankleJoint)
BallIK = cmds.ikHandle(
	name="BallIK",
	startJoint=ankleJoint,
	endEffector=ballJoint)
ToeIK = cmds.ikHandle(
	name="ToeIK",
	startJoint=ballJoint,
	endEffector=toeJoint)

# Create Reverse Foot Joints

# Find the positions of ankle, ball, and toe joints
cmds.select(clear=True);
anklePosition = cmds.xform(
	ankleJoint,
	query=True,
	worldSpace=True,
	translation=True)
ballPosition = cmds.xform(
	ballJoint,
	query=True,
	worldSpace=True,
	translation=True)
toePosition = cmds.xform(
	toeJoint,
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

print(ToeIK)