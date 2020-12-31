import os

import maya.cmds as mc

from ....lib import crvLib
from ....lib import jntLib
from ....lib import connect
from ....lib import attrLib
from ....lib import trsLib
from ....lib import strLib
from ....lib import deformLib
from ....lib import control
from . import funcs
from . import eyebrowsTemplate

reload(eyebrowsTemplate)
reload(funcs)
reload(control)
reload(crvLib)
reload(jntLib)
reload(connect)
reload(attrLib)
reload(trsLib)
reload(strLib)
reload(deformLib)


class BuildEyebrow(eyebrowsTemplate.EyebrowsTemplate):
    """Class for creating eyebrows"""
    def __init__(self,  **kwargs ):
        super(BuildEyebrow, self).__init__(**kwargs)

        self.aliases = { 'Flood': 'Flood',
                         'browin': 'browin',
                         'currogator': 'currogator',
                         'currogatorY': 'currogatorY',
                         'browMid': 'browMid',
                         'browOut': 'browOut',}

    def createBlueprint(self):
        super(BuildEyebrow, self).createBlueprint()
        self.blueprints['Flood'] = '{}_Flood_BLU'.format(self.name)
        if not mc.objExists(self.blueprints['Flood']):
            mc.joint(self.blueprintGrp, name=self.blueprints['Flood'])
            mc.xform(self.blueprints['Flood'], ws=True, t=(17.136, 313.175, -3))

        self.blueprints['browin'] = '{}_browin_BLU'.format(self.name)
        if not mc.objExists(self.blueprints['browin']):
            mc.joint(self.blueprintGrp, name=self.blueprints['browin'])
            mc.xform(self.blueprints['browin'], ws=True, t=(18.251, 314.467, 4.289))

        self.blueprints['currogator'] = '{}_currogator_BLU'.format(self.name)
        if not mc.objExists(self.blueprints['currogator']):
            mc.joint(self.blueprintGrp, name=self.blueprints['currogator'])
            mc.xform(self.blueprints['currogator'], ws=True, t=(18.666, 314.549, 4.264))

        self.blueprints['currogatorY'] = '{}_currogatorY_BLU'.format(self.name)
        if not mc.objExists(self.blueprints['currogatorY']):
            mc.joint(self.blueprintGrp, name=self.blueprints['currogatorY'])
            mc.xform(self.blueprints['currogatorY'], ws=True, t=(18.783, 314.29, 4.324))

        self.blueprints['browMid'] = '{}_browMid_BLU'.format(self.name)
        if not mc.objExists(self.blueprints['browMid']):
            mc.joint(self.blueprintGrp, name=self.blueprints['browMid'])
            mc.xform(self.blueprints['browMid'], ws=True, t=(19.821, 314.485, 3.883))

        self.blueprints['browOut'] = '{}_browOut_BLU'.format(self.name)
        if not mc.objExists(self.blueprints['browOut']):
            mc.joint(self.blueprintGrp, name=self.blueprints['browOut'])
            mc.xform(self.blueprints['browOut'], ws=True, t=(21.153, 314.534, 3.117))



    def createJoints(self):
        par = self.moduleGrp
        self.browJnts = []
        for alias, blu in self.blueprints.items():
            jnt = '{}_{}_JNT'.format(self.name, self.aliases[alias])
            jnt = mc.joint(par, n=jnt, rad = 0.3)
            self.browJnts.append(jnt)
            trsLib.setTRS(jnt, self.blueprintPoses[alias], space='world')
            self.joints[alias] = jnt


    def build(self):
        super(BuildEyebrow, self).build()

        self.currogatorOrientGrp = mc.createNode('transform', name = self.side + '_currogatorOrient_GRP', p = self.browJnts[1])
        trsLib.match(self.currogatorOrientGrp, self.browJnts[2])
        self.currogatorMod = mc.createNode('transform', name = self.side + '_currogatorModify_GRP', p = self.currogatorOrientGrp)
        mc.parent(self.browJnts[2],self.currogatorMod)

        self.currogatorYOrientGrp = mc.createNode('transform', name = self.side + '_currogatorYOrient_GRP', p = self.browJnts[1])
        trsLib.match(self.currogatorYOrientGrp, self.browJnts[3])
        self.currogatorYMod = mc.createNode('transform', name = self.side + '_currogatorYModify_GRP', p = self.currogatorYOrientGrp)
        mc.parent(self.browJnts[3],self.currogatorYMod)

        # create ctls
        self.mainCtls = []
        self.mainCtlGrps = []
        orientGrps = [self.browOutCtlOrientGrp, self.browInCtlOrientGrp, self.browMidCtlOrientGrp]
        for i in range(3):
            ctl,grp = funcs.createCtl(parent = orientGrps[i],side = self.side)
            name = orientGrps[i].replace('Orient', 'Modify')
            grp = mc.rename(grp, name)
            self.mainCtlGrps.append(grp)
            name = grp.replace('CtrlModify_GRP', '_CTL')
            ctl = mc.rename(ctl,name)
            self.mainCtls.append(ctl)
            mc.parent(grp, orientGrps[i])

        self.currogatorCtrlOrientGrp = mc.createNode('transform', name  = self.side + '_currogatorCtrlOrient_GRP', p = self.mainCtls[1])
        trsLib.match(self.currogatorCtrlOrientGrp,self.browJnts[2] )

        ctl, grp = funcs.createCtl(parent=self.currogatorCtrlOrientGrp, side=self.side,scale = [0.5, 0.5, 0.5])
        self.currogatorCtl = mc.rename(ctl, self.side + '_currogator_CTL')
        self.currogatorGrp = mc.rename(grp, self.side + '_currogatorMod_GRP')
        mc.parent(self.currogatorGrp,self.currogatorCtrlOrientGrp )


