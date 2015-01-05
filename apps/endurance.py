# IceCloud 3D viewer
import icecloud

divePath = "X:/ENDURANCE/dttools/trunk/data-mh/bonney/"
posePath = "X:/ENDURANCE/test-dives/bonney_2009/"
lod = icecloud.LODInfo(10000,1, 10, 1, 10)

diveFile = divePath + "bonney-09-dive27.xyzb"
poseFile = posePath + "Dive27/derived_data/Dive27_02Dec09_poseCorrected.0.txt"
d = icecloud.Dive("09-27", "Dive27", diveFile, poseFile, lod)

diveFile = divePath + "bonney-09-dive17.xyzb"
poseFile = posePath + "Dive17/derived_data/Dive17_21Nov09_poseCorrected.0.txt"
d2 = icecloud.Dive("09-17", "Dive17", diveFile, poseFile, lod)

icecloud.DiveMenu.addDives([d, d2])
icecloud.sondeLayer.load()

# load a mesh
icecloud.meshLayer.loadMesh("Sonde Bathymetry", "endurance/data/bonney-sonde-bathy.obj")

uim = UiModule.createAndInitialize()
sp = icecloud.SectionPanel(icecloud.uiroot, 400)
sp.addDives([d, d2])

getDefaultCamera().getController().setSpeed(100)

icecloud.sectionManager.dives = [d, d2]
