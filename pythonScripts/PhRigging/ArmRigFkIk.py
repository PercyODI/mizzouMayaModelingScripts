import maya.cmds as cmds
import sys
import re


def armRig(modelScale = None):
    # Set up default parameters
    if modelScale is None:
        modelScale = 1


    # Include an FK and IK arm control 0.0
    selection = cmds.ls(selection=True)
    selection.extend(cmds.listRelatives(selection, allDescendents=True))
    selection = cmds.ls(selection, type="joint")

    armPattern = re.compile('^(?P<location>\w+?)(?:_| |)(?P<name>Shoulder|Elbow|Forearm|Wrist|ArmEnd)$')
    armsDict = dict()

    for joint in selection:
        regexMatch = armPattern.match(joint)
        if (regexMatch):
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
            if (regexMatch):
                jointLocation = regexMatch.groupdict()['location']
                jointName = regexMatch.groupdict()['name']
                newJointName = cmds.rename(joint, jointLocation + "_" + jointName + "Fk")
                armFk[jointName] = newJointName

        # For Ik Arm
        dupArm = cmds.duplicate(armsDict[location]["Shoulder"], renameChildren=True);
        dupArmPattern = re.compile('^(?P<location>\w+?)(?:_| |)(?P<name>Shoulder|Elbow|Forearm|Wrist|ArmEnd)\d*$')
        for joint in dupArm:
            regexMatch = dupArmPattern.match(joint)
            if (regexMatch):
                jointLocation = regexMatch.groupdict()['location']
                jointName = regexMatch.groupdict()['name']
                newJointName = cmds.rename(joint, jointLocation + "_" + jointName + "Ik")
                armIk[jointName] = newJointName

        # Create orient contstraints
        orientConstraintDict = dict()
        orientConstraintDict["Shoulder"]= cmds.orientConstraint(
            armFk["Shoulder"],
            armIk["Shoulder"],
            armsDict[location]["Shoulder"],
            maintainOffset=True)[0]
        orientConstraintDict["Elbow"]= cmds.orientConstraint(
            armFk["Elbow"],
            armIk["Elbow"],
            armsDict[location]["Elbow"],
            maintainOffset=True)[0]
        orientConstraintDict["Forearm"]= cmds.orientConstraint(
            armFk["Forearm"],
            armIk["Forearm"],
            armsDict[location]["Forearm"],
            maintainOffset=True)[0]
        orientConstraintDict["Wrist"]= cmds.orientConstraint(
            armFk["Wrist"],
            armIk["Wrist"],
            armsDict[location]["Wrist"],
            maintainOffset=True)[0]

        # Creates IK
        ikWristPosition = cmds.xform(
            armIk["Wrist"],
            query=True,
            worldSpace=True,
            translation=True)

        ikElbowPosition = cmds.xform(
            armIk["Elbow"],
            query=True,
            worldSpace=True,
            translation=True)

        ForearmIK = cmds.ikHandle(
            name=location + "_ForearmIK",
            startJoint=armIk["Shoulder"],
            endEffector=armIk["Forearm"],
            solver="ikRPsolver")

        # Move EndEffector to Wrist
        cmds.move(
            ikWristPosition[0],
            ikWristPosition[1],
            ikWristPosition[2],
            ForearmIK[1] + ".rotatePivot",  # Would be great in an IK Class...
            absolute=True,
            worldSpace=True)

        # Add Rotate Plane with constraint
        ## Create a Cube
        elbowConstraintCube = cmds.polyCube(
            name=location + "_elbowConstraintCube",
            depth= (0.75 * modelScale),
            height = (0.75 * modelScale),
            width = (0.75 * modelScale))[0]

        cmds.move(
            ikElbowPosition[0],
            ikElbowPosition[1],
            ikElbowPosition[2] - (3 * modelScale),
            elbowConstraintCube,
            absolute=True,
            worldSpace=True)

        ### Hide Cube in Render
        print elbowConstraintCube + ".primaryVisibility"
        cmds.setAttr(elbowConstraintCube + ".primaryVisibility", 0)

        ## Constraint rotate plane to cube
        cmds.poleVectorConstraint(elbowConstraintCube, ForearmIK[0])

        # Create FK IK Locator
        wristPosition = cmds.xform(
            armsDict[location]["Wrist"],
            query=True,
            worldSpace=True,
            translation=True
        )



        fkIkLocator = cmds.spaceLocator(
            absolute=True,
            position=(
                wristPosition[0],
                wristPosition[1] + 2,
                wristPosition[2]),
            name=location + "_fkIkLocator")[0];

        cmds.parentConstraint(
            armsDict[location]["Wrist"], fkIkLocator,
            maintainOffset=True
        )

        # Set connections to modify weights
        cmds.addAttr(
            fkIkLocator,
            shortName="fkToIk",
            attributeType="float",
            minValue=0.0,
            maxValue=1.0,
            defaultValue=0.5,
            keyable=True
        )

        # Connect all IK joints to fkToIk
        for name in orientConstraintDict:
            cmds.connectAttr(
                fkIkLocator + ".fkToIk",
                orientConstraintDict[name] + "." + armIk[name] + "W1"
            )

            reverseShoulder = cmds.createNode("reverse")

            cmds.connectAttr(
                fkIkLocator + ".fkToIk",
                reverseShoulder + ".inputX"
            )

            cmds.connectAttr(
                reverseShoulder + ".outputX",
                orientConstraintDict[name] + "." + armFk[name] + "W0"
            )

        # Set conditions to hide arms
        ## FKs
        IkCondition = cmds.createNode("condition")
        cmds.setAttr(IkCondition + ".secondTerm", 0)
        cmds.setAttr(IkCondition + ".colorIfTrueR", 1)
        cmds.setAttr(IkCondition + ".colorIfFalseR", 0)
        cmds.setAttr(IkCondition + ".operation", 2)
        cmds.connectAttr(
            fkIkLocator + ".fkToIk",
            IkCondition + ".firstTerm"
        )
        cmds.connectAttr(
            IkCondition + ".outColorR",
            armIk["Shoulder"] + ".visibility"
        )
        cmds.connectAttr(
            IkCondition + ".outColorR",
            ForearmIK[0] + ".visibility"
        )

        ## IKs
        FkCondition = cmds.createNode("condition")
        cmds.setAttr(FkCondition + ".secondTerm", 1)
        cmds.setAttr(FkCondition + ".colorIfTrueR", 1)
        cmds.setAttr(FkCondition + ".colorIfFalseR", 0)
        cmds.setAttr(FkCondition + ".operation", 4)
        cmds.connectAttr(
            fkIkLocator + ".fkToIk",
            FkCondition + ".firstTerm"
        )
        cmds.connectAttr(
            FkCondition + ".outColorR",
            armFk["Shoulder"] + ".visibility"
        )

        # Move IK Handle to wrist
        cmds.move(
            wristPosition[0],
            wristPosition[1],
            wristPosition[2],
            ForearmIK[0],
            absolute=True,
            worldSpace=True
        )
