import maya.cmds as cmds
import maya.mel as mel

selected = cmds.ls(sl=True)

ls_type = [2, 6, 3, 7]
type_name = ['Direct', 'Indirect', 'Specular', 'Reflect']


def setupLs():
    if len(selected) == 0:
        print('You need to select something.')
    else:
        for light in selected:
            shapeNode = cmds.listRelatives(light)
            if len(shapeNode) > 1:
                sunShape = shapeNode[1]
                for vrlsTypes in ls_type:
                    numb = ls_type.index(vrlsTypes)
                    type_name[numb]
                    vrLsNode = mel.eval('vrayAddRenderElement("LightSelectElement")')
                    cmds.sets(sunShape, addElement = vrLsNode)
                    cmds.setAttr(vrLsNode + '.vray_type_lightselect', vrlsTypes)
                    cmds.setAttr(vrLsNode + '.vray_name_lightselect',
                                 '{}_{}'.format(light, type_name[numb]), type='string')
                    cmds.rename(vrLsNode, 'vrayRE_{}_{}'.format(sunShape, type_name[numb]))
            else:
                for vrlsTypes in ls_type:
                    numb = ls_type.index(vrlsTypes)
                    type_name[numb]
                    vrLsNode = mel.eval('vrayAddRenderElement("LightSelectElement")')
                    cmds.sets(light, addElement = vrLsNode)
                    cmds.setAttr(vrLsNode + '.vray_type_lightselect', vrlsTypes)
                    cmds.setAttr(vrLsNode + '.vray_name_lightselect',
                                 '{}_{}'.format(light, type_name[numb]), type='string')
                    cmds.rename(vrLsNode, 'vrayRE_{}_{}'.format(light, type_name[numb]))


setupLs()
