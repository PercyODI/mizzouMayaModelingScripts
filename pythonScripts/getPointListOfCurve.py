import maya.cmds as cmds
import sys

selection = cmds.ls(selection=True)
if(cmds.objectType(selection) != 'nurbsCurve'):
	curve = cmds.listRelatives(selection, type="nurbsCurve", allDescendents=True)[0]
else:
	curve = selection

print(curve)
controlVerticies = cmds.getAttr(curve + ".cv[*]")
print controlVerticies