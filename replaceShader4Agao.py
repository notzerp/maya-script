#replaceShader4Agao.py
'''
This script only works for redsift 2.5.XX and older version.
The rsNormalMap node has been removed in 2.6.XX and newer version.
'''

import pymel.core as pm
shaders = pm.selected()

for shader in shaders:

    rsShader = pm.rendering.shadingNode('RedshiftMaterial', asShader = True, name = 'rs_' + shader.getName())

    rsShader.refl_weight.set(0.5)
    rsShader.refl_roughness.set(0.25)

    baseColor = shader.color.get()

    fileNode = None

    if shader.color.isConnected():

        fileNode = shader.color.listConnections()[0]

    rsShader.diffuse_color.set(baseColor)

    if fileNode:

        fileNode.outColor >> rsShader.diffuse_color

    if shader.normalCamera.isConnected():

        bump2d = shader.normalCamera.listConnections()[0]
        oldNormalTex = bump2d.bumpValue.listConnections()[0]
        oldPlace2d = oldNormalTex.uvCoord.listConnections()[0]

        newPath = oldNormalTex.getAttr('fileTextureName')

        rsNormal = pm.rendering.shadingNode('RedshiftNormalMap', asTexture = True)

        pm.setAttr('.tex0', newPath, type='string')

        rsNormal.outDisplacementVector >> rsShader.bump_input
        oldPlace2d.outUV >> rsNormal.uvCoord

        pm.delete(oldNormalTex)
        pm.delete(bump2d)

    shaderSG = shader.outColor.listConnections()[0]
    rsShader.outColor >> shaderSG.surfaceShader


    pm.delete(shader)
