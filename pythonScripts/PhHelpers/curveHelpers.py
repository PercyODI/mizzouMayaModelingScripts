import maya.cmds as cmds
import sys

def getCurvePointsByType(type):
	return {
		'foot': [(0.0, 0.0, -2.384252504430984), (0.0, 0.0, -2.3842525044309846), (0.0, 0.0, -2.384252504430984), (-0.602914426407835, 0.0, -1.397665261218163), (-0.41107801800534216, 0.0, -0.10962080480142444), (-0.2192416096028491, 0.0, 0.4110780180053426), (-0.10962080480142411, 0.0, 0.5481040240071229), (-0.10962080480142422, 0.0, 0.5481040240071229), (0.0, 0.0, 0.739940432409616), (0.0, 0.0, 0.7399404324096159), (0.0, 0.0, 0.7399404324096158), (0.1733769464540671, 0.0, 0.7792732859458779), (0.31785773516578864, 0.0, 0.634792497234156), (0.41107801800534105, 0.0, 0.3014572132039176), (0.7125352312092592, 0.0, 0.0), (0.7947508348103279, 0.0, -1.4524756636188751)]
	}.get(type, [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)])

def getPointListOfCurve(selection=cmds.ls(selection=True)):
	# selection = cmds.ls(selection=True)
	if(cmds.objectType(selection) != 'nurbsCurve'):
		curve = cmds.listRelatives(selection, type="nurbsCurve", allDescendents=True)[0]
	else:
		curve = selection

	print(curve)
	controlVerticies = cmds.getAttr(curve + ".cv[*]")
	print controlVerticies