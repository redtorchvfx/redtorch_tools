"""
name: rigLib.py

Author: Ehsan Hassani Moghaddam

"""
import os
import re

import maya.cmds as mc

from ..lib import attrLib
from ..lib import trsLib
from .component import template

reload(template)
reload(trsLib)


def addRigInfoToTopNode(topGroup='rig_GRP'):
    rig_UI_version = os.getenv('RIG_UI_VERSION')
    attrLib.addString(topGroup, ln='rig_UI_version', v=rig_UI_version,
                      lock=True, force=True)


def duplicateBlueprint(bluGrp):
    bluSide = mc.getAttr(bluGrp + '.blu_side')
    bluPrefix = mc.getAttr(bluGrp + '.blu_prefix')

    number = (re.findall(r'\d+', bluPrefix) or ['1'])[0]
    prefixNoNumber = bluPrefix.replace(number, '')
    i = int(number)
    while True:
        newPrefix = '{}{}'.format(prefixNoNumber, i)
        dupName = '{}_{}_blueprint_GRP'.format(bluSide, newPrefix)
        if not mc.objExists(dupName):
            break
        i += 1

    dup = mc.duplicate(bluGrp, name=dupName)[0]
    children = mc.listRelatives(dup, ad=True, fullPath=True)
    children.sort(key=lambda x: x.count('|'), reverse=True)
    for child in children:
        tokens = child.split('|')[-1].split('_')
        newName = '_'.join([bluSide, newPrefix] + tokens[2:])
        mc.rename(child, newName)

    attrLib.setAttr(dup + '.blu_prefix', newPrefix)
    return dup

def mirrorBlueprint(bluGrp):
    attr = mc.listAttr(bluGrp)
    attrs = []
    for i in attr:
        if i.startswith('blu') or i.startswith('out'):
            attrs.append(i)

    bluSide = mc.getAttr(bluGrp + '.blu_side')
    bluPrefix = mc.getAttr(bluGrp + '.blu_prefix')

    if bluSide not in 'LR':
        mc.warning('blueprint side must be either L or R to mirror, skipped!')
        return

    otherSide = 'R' if bluSide == 'L' else 'L'

    dupName = '{}_{}_blueprint_GRP'.format(otherSide, bluPrefix)
    if mc.objExists(dupName):
        mc.warning('blueprint "{}" exists, deleting the old one!'.format(dupName))
        mc.delete(dupName)

    dup = mc.duplicate(bluGrp, name=dupName)[0]
    children = mc.listRelatives(dup, ad=True, fullPath=True)
    children.sort(key=lambda x: x.count('|'), reverse=True)

    for child in children:
        tokens = child.split('|')[-1].split('_')
        newName = '_'.join([otherSide, bluPrefix] + tokens[2:])
        trsLib.mirror(child, children=False)
        mc.rename(child, newName)

    attrLib.setAttr(dup + '.blu_side', otherSide)
    for i in attrs:
        if i.startswith('blu') or i.startswith('out'):
            if i not in ('blu_type'):
                at = mc.getAttr(dup + '.' + i)
                isString = isinstance(at, basestring)
                if isString:
                    if 'L' in at:
                        niceName = at.replace('L', 'R')
                        isLock = mc.getAttr(dup + '.' + i, lock = True)
                        if isLock:
                            mc.setAttr(dup + '.' + i, lock = False)
                        mc.setAttr(dup + '.' + i, niceName, type = 'string')
                        if isLock:
                            mc.setAttr(dup + '.' + i, lock = True)

    return dup
