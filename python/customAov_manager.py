import pymel.core as pm
import mtoa
'''
A lightgroup/ custom aovs managing tool that allows you to specify lightgroup name
for each selected lights as well as adding aovs w/ custom lpe code w/o looking into
attribute editor or render settings.
'''



# All the aov related features are located under AOVInterface
aiAovInterface = mtoa.aovs.AOVInterface()


# Make it an object cuz I wanna try out class
class Aov(object):
    def __init__(self, name, lpe):
        self.name = name
        self.lpe = lpe
        self.lpeGroup = None

    def __str__(self):
        return (self.name + ' | {}'.format(self.lpe))

    def specifyLightGroup(self, lightGroup):
        self.lpeGroup = self.lpe.replace('L.', "L.'{}'".format(lightGroup))



# add custom aov here
aovKeys = []

# Where you put your custom aov name and lpe code
def aovSetName():

    lpe_code = (pm.textField('ui_lpe_setName', query=True, text=True) + '<L.>')
    aov_name = pm.textField('ui_aov_setName', query=True, text=True)

    if lpe_code == '' or lpe_code == '<L.>':
        print 'Please give it a name.'
    elif aov_name ==  '':
        print 'Please give it a name.'
    else:
        aovKeys.append(Aov(aov_name, lpe = lpe_code))

        resetLpeInput()
        refreshAovKeys()
        print aovKeys

#######################################################################

# Clear Current AOVs list
def clearCustomAovs():

    for aovItem in getAovs():
        pm.delete(aovItem)
    refreshLpeBlock()

# Clear LPE Keys
def clearAovkeys():

    del aovKeys[:]
    print aovKeys
    refreshAovKeys()

# Update the scene
def refreshAovKeys():

    pm.textScrollList('ui_lpe_list', e=True, removeAll=True)

    for keys in aovKeys:
        pm.textScrollList('ui_lpe_list', e=True, append=keys)

# Refresh current aovs list
def refreshCurrentAovs():

    pm.textScrollList('ui_aov_list', e=True, removeAll=True)
    pm.textScrollList('ui_aov_list', e=True, append=getAovs())

# Refresh both
def refreshLpeBlock():

    refreshAovKeys()
    refreshCurrentAovs()

#######################################################################


# Get selected light
def getSelected():

    if len(pm.selected()) == 0:
        print('Nothing has been selected.')
    else:
        return pm.selected()


# For scrollList selection
def getItemInAovList():
    return pm.textScrollList('ui_aov_list', query=True, selectItem=True)

def getItemInLpeList():
    # convert "long" list to an "int" list
    lpeLongList = pm.textScrollList('ui_lpe_list', query=True, sii=True)
    lpeIntList = [int(item) for item in lpeLongList]
    return lpeIntList


def removeItemInList():

    getItemInAovList()
    getItemInLpeList()

    if len(getItemInAovList()) == 0:
        #print getItemInLpeList()

        for item in getItemInLpeList():
            index = (item - 1)

            aovKeys.pop(index)
            aovKeys.insert(index, 'none')

        while('none' in aovKeys):
            aovKeys.remove('none')

    elif len(getItemInLpeList()) == 0:
        pm.delete(getItemInAovList())
    else:
        print 'Please select only the items within the same block.'

    refreshLpeBlock()


# Get light group name of selected light
def getSingleLgAov():

    global single_LG_name

    if len(getSelected()) == 1:
        single_LG_name=(getSelected()[0].aiAov.get())
        print "LG name '{}'.".format(single_LG_name)

    else:
        print('Please select one light.')

    return single_LG_name

# Set light group
def applyLgAov():
    for light in getSelected():
        light.aiAov.set(single_LG_name)
        print "Applied LG name '{}' to {}.".format(single_LG_name, light)
    refreshList()

# Set selected LG to default
def removeLgAov():
    for light in getSelected():
        light.aiAov.set('default')
    refreshList()

def clearAllLG():
    for light in getLights():
        light.aiAov.set('default')
    refreshList()


# Create new light group name
def createNewLG():

    lgName = pm.textField('ui_lightGroup_setName', query=True, text=True)

    if len(getSelected()) == 0:
        print 'Please select at least one light.'
    elif lgName == '':
        print 'Please specify a light group name.'
    else:
        for light in getSelected():
            light.aiAov.set(lgName)

    resetLgNameInput()
    refreshList()
    print lgName


# reset LG name input
def resetLgNameInput():
    pm.textField('ui_lightGroup_setName', e=True, text='')

def resetLpeInput():
    pm.textField('ui_lpe_setName', e=True, text='')
    pm.textField('ui_aov_setName', e=True, text='')


# Return all arnold lights in the scene
def getLights():
    return pm.ls(type = ['aiAreaLight', 'aiSkyDomeLight', 'directionalLight', 'pointLight', 'aiMeshLight'])

# Return all aovs in the scene
def getAovs():

    global current_aovs

    current_aovs = pm.ls(type = 'aiAOV')

    return current_aovs

# Rename items in the light list
def lightListing():
    lightNameList = []
    for light in getLights():
        lightNameList.append(light + '| {}'.format(light.aiAov.get()))
    return lightNameList

# Return all light groups in the scene
def getLightGroups():

    groups = []
    for light in getLights():
        groups.append(light.aiAov.get())

    # delete duplicated
    lgList = set(groups)

    return lgList

# Loop thru all the light and create Aovs base on provided LPE
def createAov():

    clearCustomAovs()

    for aovKey in aovKeys:
        for lightGroup in getLightGroups():

            sceneAov = aiAovInterface.addAOV('{}_{}'.format(lightGroup, aovKey.name))
            aiAov = pm.PyNode(sceneAov.node)
            aovKey.specifyLightGroup(lightGroup)
            aiAov.lightPathExpression.set(aovKey.lpeGroup)

    refreshLpeBlock()


# Refresh Light list
def refreshList():
    # Clear all in the list
    pm.textScrollList('ui_light_list', e=True, removeAll=True)
    pm.textScrollList('ui_lightGroup_list', e=True, removeAll=True)
    # Reload list
    pm.textScrollList('ui_light_list', e=True, append=lightListing())
    pm.textScrollList('ui_lightGroup_list', e=True, append=getLightGroups())




###########################################################################



def create_ui():



    winID = 'aovUI'
    winWidth = 530
    winHeight = 725
    rowHeight = 30


    if pm.window(winID, exists=True):
        pm.deleteUI(winID)

    aovWin = pm.window(winID, title = 'Light Group / AOV Manager', widthHeight = (winWidth,580), sizeable=True)

    # Main layout refs

    mainCL = pm.columnLayout(adjustableColumn=False,
                            columnAttach=('both', 5),
                            rowSpacing=8,
                            columnWidth=530,
                            parent=winID
                            )

    # 1st block - LG Assignment
    pm.frameLayout(label='Light Group Assignment')
    topDivide_LG = pm.columnLayout(adjustableColumn=True, columnAlign='center', rowSpacing=8)

    pm.rowLayout(numberOfColumns=2)

    # 1st row - LG L
    pm.columnLayout(adjustableColumn=True, columnAlign='center', rowSpacing=8)
    pm.text(label='Lights')
    pm.textScrollList('ui_light_list', numberOfRows=20,h=winHeight*.25, allowMultiSelection=True,
                                        append=lightListing(), dcc="getItemInList()")

    pm.setParent('..')

    #1st row - LG R
    pm.columnLayout(adjustableColumn=True, columnAlign='center', rowSpacing=8)
    pm.text(label='Light Groups')
    pm.textScrollList('ui_lightGroup_list', numberOfRows=20,h=winHeight*.25, allowMultiSelection=True,
                            append=getLightGroups(), dcc="getItemInList()")

    pm.setParent('..')
    pm.setParent(topDivide_LG)

    #
    pm.separator()

    pm.gridLayout(numberOfColumns=3, cellWidthHeight=(winWidth*.33,30))

    pm.button(label='Refresh', command='refreshList()')
    pm.button(label='Remove', command='removeLgAov()')
    pm.button(label='Clear All', command='clearAllLG()')

    pm.setParent('..')

    pm.separator()

    pm.rowColumnLayout(numberOfRows=1, width=winWidth)

    pm.textField('ui_lightGroup_setName', height=30, width=310, pht='Light Group Name')
    pm.button(label='Create',w=winWidth*.2, command='createNewLG()')
    pm.button(label='Reset', w=winWidth*.2, command='resetLgNameInput()')

    pm.setParent('..')

    pm.separator()


    pm.gridLayout(numberOfColumns=3, cellWidthHeight=(winWidth*.5,30))
    pm.button(label='Get', command='getSingleLgAov()')
    pm.button(label='Set', command='applyLgAov()')

    pm.setParent('..')


    pm.separator()


    #2nd block - LPE assignment
    pm.frameLayout(label='LPE Assignment')
    topDivide_LPE = pm.columnLayout(adjustableColumn=True, columnAlign='center', rowSpacing=8)

    pm.rowLayout(numberOfColumns=2)

    #2nd Block aov list
    pm.columnLayout(adjustableColumn=True, columnAlign='center', rowSpacing=8)
    pm.text(label='Current AOVs')
    pm.textScrollList('ui_aov_list', numberOfRows=20, h=winHeight/4, allowMultiSelection=True,
                        append=getAovs())
    pm.setParent('..')

    pm.columnLayout(adjustableColumn=True, columnAlign='center', rowSpacing=8)

    #2nd block - lpe list
    pm.text(label='LPE Keys')
    pm.textScrollList('ui_lpe_list', numberOfRows=20, h=winHeight/4, allowMultiSelection=True,
                        append=aovKeys)
    pm.setParent('..')
    pm.setParent(topDivide_LPE)

    pm.rowLayout(numberOfColumns=2)
    pm.button(label='Clear Aovs', width=winWidth*.488, command='clearCustomAovs()')
    pm.button(label='Clear Keys', width=winWidth*.488, command='clearAovkeys()')

    pm.setParent('..')

    pm.separator()

    pm.gridLayout(numberOfColumns=2, cellWidthHeight=(winWidth*.492,30))

    pm.button(label='Refresh', command='refreshLpeBlock()')
    pm.button(label='Remove', command='removeItemInList()')

    pm.setParent('..')

    pm.separator()

    pm.rowColumnLayout(numberOfRows=1, width=winWidth, cs=(1,13))

    pm.textField('ui_aov_setName', height=30, width=winWidth*.25, pht='Aov Name')
    pm.textField('ui_lpe_setName', height=30, width=winWidth*.25, pht='Custom LPE')
    pm.button(label='Create',w=winWidth*.2, command='aovSetName()')
    pm.button(label='Reset', w=winWidth*.2, command='resetLpeInput()')

    pm.setParent('..')

    pm.separator()

    pm.gridLayout(numberOfColumns=1, cellWidthHeight=(winWidth,45))
    pm.button(label='Create Custom Aovs', width=winWidth,
                ann='Click the button to do the thing.',
                command='createAov()')

    pm.setParent('..')

    pm.showWindow(aovWin)
