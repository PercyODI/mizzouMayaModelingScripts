import maya.cmds as cmds;
import sys;
import re;
import pythonScripts.PhHelpers.curveHelpers as curveHelpers;

def reverseFootLock():
	### Important!                                                    ###
	# Make sure that the character is facing in the Z axis, until fixed #


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
			name=location + "_AnkleIK",
			startJoint=legsDict[location]["Hip"],
			endEffector=legsDict[location]["Ankle"])
		BallIK = cmds.ikHandle(
			name=location + "_BallIK",
			startJoint=legsDict[location]["Ankle"],
			endEffector=legsDict[location]["Ball"])
		ToeIK = cmds.ikHandle(
			name=location + "_ToeIK",
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
			name=location + "_RFHeel",
			absolute=True,
			position=(
				anklePosition[0], # X Position
				ballPosition[1],  # Y Position
				anklePosition[2]) # Z Position
			)
		# Save position of Heel in same format as other original joints
		heelPosition = cmds.xform(
			RFHeel,
			query=True,
			worldSpace=True,
			translation=True)

		# Freeze Transformations on the RFHeel
		cmds.makeIdentity(apply=True)

		RFToe = cmds.joint(
			name=location + "_RFToe",
			absolute=True,
			position=toePosition)
		RFBall = cmds.joint(
			name=location + "_RFBall",
			absolute=True,
			position=ballPosition)
		RFAnkle = cmds.joint(
			name=location + "_RFAnkle",
			absolute=True,
			position=anklePosition)

		# *IK[0] is the IKHandle. This leaves the endEffector where it was set originally
		cmds.parent(ToeIK[0], RFToe)
		cmds.parent(BallIK[0], RFBall)
		cmds.parent(AnkleIK[0], RFAnkle)

		# Create the control curve
		controlCurve = cmds.rename(
			cmds.curve(
				d=3, 
				ws=True, 
				per=True, 
				p=[ (toePosition[0], 		toePosition[1], 	toePosition[2] + 1),		# In front of toe
					(toePosition[0] + 1.25, toePosition[1], 	toePosition[2]),			# Left of toe
					(ballPosition[0] + 1, 	ballPosition[1], 	ballPosition[2]),			# Left of Ball
					(heelPosition[0] + 1, 	heelPosition[1], 	heelPosition[2]),			# Left of Heel
					(heelPosition[0], 		heelPosition[1], 	heelPosition[2] - 1),		# Behind Heel
					(heelPosition[0] - 1, 	heelPosition[1], 	heelPosition[2]),			# Right of Heel
					(ballPosition[0] - 1, 	ballPosition[1], 	ballPosition[2]),			# Right of Ball
					(toePosition[0] - 1.25, toePosition[1], 	toePosition[2]),			# Right of toe
					(toePosition[0], 		toePosition[1], 	toePosition[2] + 1),		# In front of toe
					(toePosition[0] + 1.25, toePosition[1], 	toePosition[2]),			# Left of toe
					(ballPosition[0] + 1, 	ballPosition[1], 	ballPosition[2])],			# Left of Ball
				k=[-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 
			location + "_FootControl");

		# Set the pivot from origin to center of curve
		cmds.xform(controlCurve, centerPivots=True)
		# Parent the Reverse Foot to the control curve
		cmds.parent(RFHeel, controlCurve);

		# Add attributes to control curve

		# Tap attribute
		cmds.addAttr(
			controlCurve,
			longName="tap", 
			attributeType="float",
			defaultValue=0.0,
			minValue=-5.0,
			maxValue=10.0)

		# TipToe attribute
		cmds.addAttr(
			controlCurve,
			longName="tipToe",
			attributeType="float",
			defaultValue=0.0,
			minValue=-5.0,
			maxValue=10.0)

		# ballLift attribute
		cmds.addAttr(
			controlCurve,
			longName="ballLift",
			attributeType="float",
			defaultValue=0.0,
			minValue=-5.0,
			maxValue=10.0)

		# ballLift attribute
		cmds.addAttr(
			controlCurve,
			longName="legLift",
			attributeType="float",
			defaultValue=0.0,
			minValue=-5.0,
			maxValue=10.0)

		# Set driven keys to control curve attributes 
		# TODO: Refactor setting these driven keys into their own function / module

		# Tap Driven Keys
		cmds.setDrivenKeyframe(    ### This one must be first for tap ###
			RFHeel + ".rx",
			currentDriver=controlCurve + ".tap",
			driverValue=0,
			inTangentType="linear",
			outTangentType="linear")
		cmds.setDrivenKeyframe(
			RFHeel + ".rx",
			currentDriver=controlCurve + ".tap",
			driverValue=-5.0,
			value=45.0,
			inTangentType="linear",
			outTangentType="linear")
		cmds.setDrivenKeyframe(
			RFHeel + ".rx",
			currentDriver=controlCurve + ".tap",
			driverValue=10.0,
			value=-60.0,
			inTangentType="linear",
			outTangentType="linear")

		# Tip Toe Driven Keys
		cmds.setDrivenKeyframe(    ### This one must be first for tipToe ###
			RFToe + ".rx",
			currentDriver=controlCurve + ".tipToe",
			driverValue=0,
			inTangentType="linear",
			outTangentType="linear")
		cmds.setDrivenKeyframe(
			RFToe + ".rx",
			currentDriver=controlCurve + ".tipToe",
			driverValue=-5.0,
			value=-50.0,
			inTangentType="linear",
			outTangentType="linear")
		cmds.setDrivenKeyframe(
			RFToe + ".rx",
			currentDriver=controlCurve + ".tipToe",
			driverValue=10.0,
			value=90.0,
			inTangentType="linear",
			outTangentType="linear")

		# Ball Lift Driven Keys
		cmds.setDrivenKeyframe(    ### This one must be first for ballLift ###
			RFBall + ".rx",
			currentDriver=controlCurve + ".ballLift",
			driverValue=0,
			inTangentType="linear",
			outTangentType="linear")
		cmds.setDrivenKeyframe(
			RFBall + ".rx",
			currentDriver=controlCurve + ".ballLift",
			driverValue=-5.0,
			value=-45.0,
			inTangentType="linear",
			outTangentType="linear")
		cmds.setDrivenKeyframe(
			RFBall + ".rx",
			currentDriver=controlCurve + ".ballLift",
			driverValue=10.0,
			value=65.0,
			inTangentType="linear",
			outTangentType="linear")

		# Leg Lift Driven Keys
		cmds.setDrivenKeyframe(    ### This one must be first for legLift ###
			RFHeel + ".ty",
			currentDriver=controlCurve + ".legLift",
			driverValue=0,
			inTangentType="linear",
			outTangentType="linear")
		cmds.setDrivenKeyframe(
			RFHeel + ".ty",
			currentDriver=controlCurve + ".legLift",
			driverValue=-5.0,
			value=-5.0,
			inTangentType="linear",
			outTangentType="linear")
		cmds.setDrivenKeyframe(
			RFHeel + ".ty",
			currentDriver=controlCurve + ".legLift",
			driverValue=10.0,
			value=10.0,
			inTangentType="linear",
			outTangentType="linear")

	# cmds.curve(d=3, p=curveHelpers.getCurvePointsByType('foot'))
