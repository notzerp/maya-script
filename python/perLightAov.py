#PER LIGHT AOV SETUP.py

'''Arnold per light aov setup for Beached.'''
import pymel.core as pm
import mtoa

interface = mtoa.aovs.AOVInterface()

class Aov(object):
	def __init__(self, name, lpe):
		self.name = name
		self.lpe = lpe
		self.lpeGroup = None

	def addLightGroup(self, lightGroup):
		self.lpeGroup = self.lpe.replace('L.', "L.'{}'".format(lightGroup))

aovKeys = [ Aov('beauty', lpe = "C.*<L.>")
			Aov('diffuse', lpe = "C<RD>.*<L.>"),
		    Aov('specular', lpe = "C<RS[^'coat']>.*<L.>"),
		    Aov('coat', lpe = "C[DSV]<L.>"),
		    Aov('transmission', lpe = "C<TS>.*<L.>")

		     ]

def getLights():
	return pm.ls(type = ['aiAreaLight'])

def getLightGroups():
	groups = []
	for light in getLights():
		groups.append(light.aiAov.get())
	return groups

for aovKey in aovKeys:

	for lightGroup in getLightGroups():
		sceneAov = interface.addAOV('{}_{}'.format(lightGroup, aovKey.name))
		aiAov = pm.PyNode(sceneAov.node)
		aovKey.addLightGroup(lightGroup)
		aiAov.lightPathExpression.set(aovKey.lpeGroup)
