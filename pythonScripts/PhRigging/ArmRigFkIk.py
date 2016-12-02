import maya.cmds as cmds
import sys
import re

def armRig():
	# Include an FK and IK arm control 0.0
	selection = cmds.ls(selection=True)
	selection.extend(cmds.listRelatives(selection, allDescendents=True))
	selection = cmds.ls(selection, type="joint")

	armPattern = re.compile('^(?P<location>\w+?)(?:_| |)(?P<name>Shoulder|Elbow|Forearm|Wrist|ArmEnd)$')
	armsDict = dict()

	for joint in selection:
		regexMatch = armPattern.match(joint)
		if(regexMatch):
			jointLocation = regexMatch.groupdict()['location']
			jointName = regexMatch.groupdict()['name']
			if jointLocation in armsDict:
				armsDict[jointLocation][jointName] = joint
			else:
				armsDict[jointLocation] = dict()
				armsDict[jointLocation][jointName] = joint

	for location in armsDict:
		armIk = dict()
		armFk = dict()

		# For Fk Arm
		dupArm = cmds.duplicate(armsDict[location]["Shoulder"], renameChildren=True);
		dupArmPattern = re.compile('^(?P<location>\w+?)(?:_| |)(?P<name>Shoulder|Elbow|Forearm|Wrist|ArmEnd)\d*$')
		for joint in dupArm:
			regexMatch = dupArmPattern.match(joint)
			if(regexMatch):
				jointLocation = regexMatch.groupdict()['location']
				jointName = regexMatch.groupdict()['name']
				newJointName = cmds.rename(joint, jointLocation + "_" + jointName + "Fk")
				armFk[jointName] = newJointName;

		# For Ik Arm
		dupArm = cmds.duplicate(armsDict[location]["Shoulder"], renameChildren=True);
		dupArmPattern = re.compile('^(?P<location>\w+?)(?:_| |)(?P<name>Shoulder|Elbow|Forearm|Wrist|ArmEnd)\d*$')
		for joint in dupArm:
			regexMatch = dupArmPattern.match(joint)
			if(regexMatch):
				jointLocation = regexMatch.groupdict()['location']
				jointName = regexMatch.groupdict()['name']
				newJointName = cmds.rename(joint, jointLocation + "_" + jointName + "Ik")
				armIk[jointName] = newJointName;

		# Create orient contstraints
		cmds.orientConstraint(armFk["Shoulder"], armIk["Shoulder"], armsDict[location]["Shoulder"])
		cmds.orientConstraint(armFk["Elbow"], armIk["Elbow"], armsDict[location]["Elbow"])
		cmds.orientConstraint(armFk["Forearm"], armIk["Forearm"], armsDict[location]["Forearm"])
		cmds.orientConstraint(armFk["Wrist"], armIk["Wrist"], armsDict[location]["Wrist"])

		# Create FK IK Locator
		

		fkIkLocator = cmds.spaceLocator(
			absolute=True,
			position=(
				wristPosition[0],
				wristPosition[1],
				wristPosition[2]),
			name=location + "_fkIkLocator");

		cmds.parentConstraint(armsDict[location]["Wrist"], fkIkLocator)

		# Set connections to modify weights

		# Creates IK
		ikWristPosition = cmds.xform(
			armIk["Wrist"],
			query=True,
			worldSpace=True,
			translation=True)

		ForearmIK = cmds.ikHandle(
			name=location + "_ForearmIK",
			startJoint=armIk["Shoulder"],
			endEffector=armIk["Forearm"])

		# Move EndEffector to Wrist
		cmds.move(
			ikWristPosition[0],
			ikWristPosition[1],
			ikWristPosition[2],
			ForearmIK[1] + ".rotatePivot", # Would be great in an IK Class...
			absolute=True,
			worldSpace=True,)

armRig()