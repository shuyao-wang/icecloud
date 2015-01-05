from omega import *
from omegaToolkit import *
import icecloud

groups = {}
groupToggleButtons = {}
groupMenuButtons = {}
dives = {}

# Initialize menu
mm = MenuManager.createAndInitialize()
diveMenu = mm.getMainMenu().addSubMenu('Dives')
diveDisplayMenu = mm.getMainMenu().addSubMenu('Dive Display Mode')

diveDisplayMenu.addLabel("Point Size")
ss = diveDisplayMenu.addSlider(10, "icecloud.DiveMenu.onPointSizeSliderValueChanged(%value%)")
ss.getSlider().setValue(4)
ss.getWidget().setWidth(200)

abtn = diveDisplayMenu.addButton("Additive", "icecloud.DiveMenu.setAdditive(%value%)")
abtn.getButton().setCheckable(True)
diveDisplayMenu.addLabel("------------------")
diveDisplayMenu.addButton("Color By Dive", "icecloud.DiveMenu.colorByDive()")
diveDisplayMenu.addButton("Color By Angle", "icecloud.DiveMenu.colorByAngle()")
diveDisplayMenu.addButton("Color By Range", "icecloud.DiveMenu.colorByRange()")
diveDisplayMenu.addButton("Color By Depth", "icecloud.DiveMenu.colorByDepth()")

# cc = Container.create(ContainerLayout.LayoutHorizontal, UiModule.createAndInitialize().getUi())

# diveDisplayMenu.show()
# diveMenu.show()
# cc.addChild(diveDisplayMenu.getContainer())
# cc.addChild(diveMenu.getContainer())


#-------------------------------------------------------------------------------
def setAdditive(value):
    for key,dive in dives.iteritems():
        if(dive.pointsObject != None):
            pom = dive.pointsObject.getMaterial()
            pom.setAdditive(value)
            #pom.setTransparent(value)
            pom.setDepthTestEnabled(not value)
		
#-------------------------------------------------------------------------------
def colorByAngle():
    dl = icecloud.diveLayer
    dl.w1.setFloat(1)
    dl.w2.setFloat(0)
    dl.w3.setFloat(0)
    dl.w4.setFloat(0)
    dl.fieldMin.setFloat(dl.attribMinBound.x)
    dl.fieldMax.setFloat(dl.attribMaxBound.x)

#-------------------------------------------------------------------------------
def colorByRange():
    dl = icecloud.diveLayer
    dl.w1.setFloat(0)
    dl.w2.setFloat(1)
    dl.w3.setFloat(0)
    dl.w4.setFloat(0)
    dl.fieldMin.setFloat(dl.attribMinBound.y)
    dl.fieldMax.setFloat(dl.attribMaxBound.y)

#-------------------------------------------------------------------------------
def colorByDepth():
    dl = icecloud.diveLayer
    dl.w1.setFloat(0)
    dl.w2.setFloat(0)
    dl.w3.setFloat(1)
    dl.w4.setFloat(0)
    # HACK
    dl.fieldMin.setFloat(0)
    dl.fieldMax.setFloat(50)
	
#-------------------------------------------------------------------------------
def colorByDive():
    dl = icecloud.diveLayer
    dl.w1.setFloat(0)
    dl.w2.setFloat(0)
    dl.w3.setFloat(0)
    dl.w4.setFloat(1)

#-------------------------------------------------------------------------------
def addDives(dives):
    for d in dives:
        addDive(d)

#-------------------------------------------------------------------------------
def onPointSizeSliderValueChanged(value):
    dl = icecloud.diveLayer
    size = ((value + 1) ** 2) * 0.01
    dl.pointScale.setFloat(size)

#-------------------------------------------------------------------------------
def addDive(dive):
    dives[dive.id] = dive
    groupName = dive.id.split('-')[0]
    if(not groupName in groups):
        groupMenu = diveMenu.addSubMenu(groupName)
        evt = 'icecloud.DiveMenu.onSelectAllToggle("{0}")'.format(groupName)
        b = groupMenu.addButton('Select All', evt)
        b.getButton().setCheckable(True)
        groups[groupName] = groupMenu
        groupToggleButtons[groupName] = b.getButton()
        groupMenuButtons[groupName] = []
    
    evt = 'icecloud.DiveMenu.onDiveToggle("{0}", %value%)'.format(dive.id)
    b = groups[groupName].addButton(dive.label, evt)
    b.getButton().setCheckable(True)
    b.getButton().setName(dive.id)
    groupMenuButtons[groupName].append(b.getButton())
    dives[dive.id] = dive

    
#-------------------------------------------------------------------------------
def onSelectAllToggle(name):
    v = groupToggleButtons[name].isChecked()
    for b in groupMenuButtons[name]:
        b.setChecked(v)
        onDiveToggle(b.getName(), v)

#-------------------------------------------------------------------------------
def onDiveToggle(name, value):
    d = dives[name]
    if(value):
        d.showPose()
        d.showPoints()
    else:
        d.hidePose()
        d.hidePoints()
    