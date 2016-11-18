import maya.cmds as cmds
import sys
import re

def armRig():
	# Include an FK and IK arm controll 0.0
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
		ForearmIK = cmds.ikHandle(
			name=location + "_ForearmIK",
			startJoint=armsDict[location]["Shoulder"],
			endEffector=armsDict[location]["Forearm"])

		wristPosition = cmds.xform(
			armsDict[location]["Wrist"],
			query=True,
			worldSpace=True,
			translation=True)

		# Move EndEffector to Wrist
		cmds.move(
			wristPosition[0],
			wristPosition[1],
			wristPosition[2],
			ForearmIK[1] + ".rotatePivot", # Would be great in an IK Class...
			absolute=True,
			worldSpace=True,)

armRig()