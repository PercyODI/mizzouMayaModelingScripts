import maya.cmds as cmds
import sys
import re
from pythonScripts.PhRigging import ArmRigFkIk
from pythonScripts.PhRigging import ReverseFootLock

selection = cmds.ls(selection = True)

ArmRigFkIk.armRig()
cmds.select(selection)
ReverseFootLock.reverseFootLock()
