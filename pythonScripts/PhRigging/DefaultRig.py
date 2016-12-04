import maya.cmds as cmds
import sys
import re
import pythonScripts.PhRigging as PhRigging

reload(PhRigging)

selection = cmds.ls(selection=True)
PhRigging.armRig(0.3)
cmds.select(selection)
PhRigging.reverseFootLock(0.3)

# Create global transform
globalTransform = cmds.rename(
    cmds.curve(
        d=1,
        ws=True,
        p=[(-4, 0, 0), (-2, 0, -1.5), (-2, 0, -0.5), (-0.5, 0, -0.5), (-0.5, 0, -2), (-1.5, 0, -2), (0, 0, -4),
           (1.5, 0, -2), (0.5, 0, -2), (0.5, 0, -0.5), (2, 0, -0.5), (2, 0, -1.5), (4, 0, 0), (2, 0, 1.5), (2, 0, 0.5),
           (0.5, 0, 0.5), (0.5, 0, 2), (1.5, 0, 2), (0, 0, 4), (-1.5, 0, 2), (-0.5, 0, 2), (-0.5, 0, 0.5), (-2, 0, 0.5),
           (-2, 0, 1.5), (-4, 0, 0)]
    ),
    "GlobalTransform#")
