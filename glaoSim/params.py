# Dependencies
import util.tel
import util.guideStar
import util.elong
import util.sci
import numpy
import base.readConfig
from util.atmos import geom,layer,source
from util.dm import dmOverview,dmInfo
# Base inheritance
this=base.readConfig.init(globals())
# ========================== LOAD CONFIGURABLE PARAMETERS =========================================================
if hasattr(this.globals,"resFile"):
    resFile=this.globals.resFile
else:
    resFile="resSCAO__500nm_pruebas.csv"
if hasattr(this.globals,"thetaSci"):
    thetaSci = this.globals.thetaSci
else:
    thetaSci = 0.
if hasattr(this.globals, "phiSci"):
    phiSci = this.globals.phiSci
else:
    phiSci = 0.
if hasattr(this.globals, "rcond "):
    rcond  = this.globals.rcond
else:
    rcond  = 0.05
if hasattr(this.globals, "gainFactor"):
    gainFactor = this.globals.gainFactor
else:
    gainFactor = 0.65
if hasattr(this.globals, "decayFactor"):
    decayFactor = this.globals.decayFactor
else:
    decayFactor = 0.98
if hasattr(this.globals, "centroidPower"):
    centroidPower = this.globals.centroidPower
else:
    centroidPower = 0.1
if hasattr(this.globals, "nlyer"):
    nlyer = this.globals.nlyer
else:
    nlyer = 1
if hasattr(this.globals, "strList"):
    strList = this.globals.strList
    print ("strList is intrduced as input, str(0km)= % ",strList[0])
else:
    strList  = [0.9,0.04,0.02,0.01,0.01,0.01,0.01]
if hasattr(this.globals, "r0"):
        r0= this.globals.r0
else:
    print ("ERROR: no R0 value included-->R0=10cm used!")
    r0 = 0.1
nthreads=32
interpolationNthreads=4
# ============================ SIMULATION DATA ===========================================================
tstep = 1/2000.#Simulation timestep in seconds (2kHz).
AOExpTime = 120000.# (use --iterations=xxx to modify)--> texp = tstep * AOExpTime
# ============================ TELESCOPE DATA ============================================================
#npup & ntel defined later depending on WFS parameters!
worstR0 = 0.08 # in meters
telDiam=1.5 #Telescope diameter: numSubaps computed so that: numSubaps = ceil(telDiam / worstR0)
telSec=0. #Central obscuration
ngsLam=500.#NGS wavelength
lgsLam=500.#LGS wavelength
sciLam=500.#Science wavelength
ngsAsterismRadius=12.5#arcseconds
nsci=7
nlgs=0
nngs=7
# ============================ ATMOSPHERE DATA ============================================================

atmosDict={}
nlayer=1 # atmospheric layers
strList = [ 1.0,0.04,0.02,0.01,0.01,0.01,0.01] # strength list [1.0]#
hList=[0,5000,7000,10000,12000,15000,20000] # height list [0]#
vList=[5.6,6.25,7.57,13.31,19.06,12.14,13.52] # wind speed list [5.6]#
dirList=numpy.arange(nlayer)*73
layerList={"allLayers":["L%d"%x for x in range(nlayer)]}
l0=25. #outer scale

# ==================================== WFS DATA ===========================================================
Kpix=1 #factor para conseguir mas pixeles en la subapertura sin cambiar la resolucion
wfs_nsubx= int(numpy.ceil(telDiam/worstR0)) #Number of subaps
wfs_sig=1e6
fov_wfs=10.#
nFieldX_wfs=3
phasesize = 5 # between 3 and 6 is the ideal, less than 3 can cause problems.
npup = wfs_nsubx * phasesize
ntel=npup#Telescope diameter in pixels
fftsize_wfs=int(Kpix*phasesize*2 )#16
widefieldImageBoundary_wfs=Kpix*4# The extra rows/cols added to the psf. This will ideally depend on pixel scale and seeing
                        # - i.e. should be equal to likely maximum spot motion

# ============================== PUPIL DEFINITION AND SUBAPERTURE SAMPLING ================================
# -----------------------------------
#  ---- Create a pupil function
# -----------------------------------
spider=None
pupil=util.tel.Pupil(npup,ntel/2,ntel/2*telSec/telDiam,spider=spider)
# ------------------------------------
#  ---- Create the WFS overview
# ------------------------------------
sourceTheta=0.
radius1=12.5
radius2=25
wfs_central=1
wfs_1ring=6
wfs_2ring=12

nwfs=wfs_central+ wfs_1ring+ wfs_2ring
wdict={}
wfs_i=1

if wfs_central==1:
    #wdict["%d" %wfs_i] = util.guideStar.NGS("%d" %wfs_i, wfs_nsubx, 0, 0, npup / wfs_nsubx, sig=wfs_sig, sourcelam=ngsLam, fov=fov, pupil=pupil, reconList=["recon"],magicCentroiding=1)
    wdict["%d" % wfs_i] = util.guideStar.NGS("%d" % wfs_i, wfs_nsubx, 0, 0, npup / wfs_nsubx, sig=wfs_sig, sourcelam=ngsLam, fov=fov_wfs, pupil=pupil, reconList=["recon"])
    print("WFS%d  (%d,%d,)" % (wfs_i,0,0,))
    wfs_i=wfs_i+1

for i in range(wfs_1ring):
    #wdict["%d"%wfs_i]=util.guideStar.NGS("%d"%wfs_i,wfs_nsubx,radius1, i*360./wfs_1ring, npup/(wfs_nsubx),sig=wfs_sig,sourcelam=ngsLam,fov=fov, pupil=pupil,reconList=["recon"],magicCentroiding=1)
    wdict["%d" % wfs_i] = util.guideStar.NGS("%d" % wfs_i, wfs_nsubx, radius1, i * 360. / wfs_1ring, npup / (wfs_nsubx),sig=wfs_sig, sourcelam=ngsLam, fov=fov_wfs, pupil=pupil, reconList=["recon"])
    print("WFS%d  (%d,%d,)" % (wfs_i,radius1, i*360./wfs_1ring))
    wfs_i = wfs_i + 1


wfsOverview=util.guideStar.wfsOverview(wdict)

sourceList=[]
sourceList+=wfsOverview.values()

# ================================== DM & RECONSTRUCTOR DATA ==============================================
nAct=int(wfs_nsubx+1)#Number of actuators across the DM
# ------------------------------------
# ------   Create a Science overview.
# ------------------------------------

sciDict={}
#for i in range(nsci):
#    id="sci%d"%(i+1)
#    sciDict[id]=util.sci.sciInfo(id,theta=radius1,phi=i*360./nngs,pupil=pupil,sourcelam=sciLam,phslam=sciLam,calcRMS=1, summaryFilename=resFile)
#    sourceList.append(sciDict[id])
#sciOverview=util.sci.sciOverview(sciDict)
i = 0
sciOverview=util.sci.sciOverview({"sci%d"%(i+1):util.sci.sciInfo("sci%d"%(i+1),thetaSci,phiSci,pupil,sciLam,calcRMS=1,summaryFilename=resFile)})
sourceList+=sciOverview.values()

# -------------------------------------------
# ------ Create atmos with all the layers
# ---------------------------------------

for i in range(nlayer):
    atmosDict["L%d"%i]=layer(hList[i],dirList[i],vList[i],strList[i],seed=10+i)

atmosGeom=geom(atmosDict,sourceList,ntel,npup,telDiam,r0,l0)

# -------------------------------------------
# ------  Create DM
# -------------------------------------------
#Now DM stuff.  2 DM objects needed here, even though there is only 1.  The first one generates the entire DM surface.  The second is for the DM metapupil - i.e. for non-ground-conjugate DMs, will select only the relevant line of sight.

dmHeight=0.
dmDict={}

dmDict["dm"]=dmInfo('dm',['1'],dmHeight,wfs_nsubx+1,minarea=0.5,actuatorsFrom="recon",pokeSpacing=None,maxActDist=1.5,decayFactor=decayFactor)
dmDict["dmNFb"] = dmInfo('dmNF',['b'],dmHeight,wfs_nsubx+1,minarea=0.5,actuatorsFrom="Nothing",pokeSpacing=None,maxActDist=1.5,decayFactor=decayFactor,sendFullDM=0,reconLam=ngsLam)


ndm=this.getVal("ndm",1)
if ndm>1:
    dmHeight=numpy.arange(ndm)*(hList[-1]/(ndm-1.))
else:
    dmHeight=[0]

dmInfoList=[]

for i in range(ndm):
    dmInfoList.append(dmInfo('dm%dpath'%i,[x.idstr for x in sourceList],dmHeight[i],nAct,minarea=0.5,actuatorsFrom="recon",pokeSpacing=(None if wfs_nsubx<20 else 10),maxActDist=1.5,decayFactor=0.95))
    #dmInfoList.append(dmInfo('dmNFb%dpath' % i, [x.idstr for x in sourceList], dmHeight[i], nAct, minarea=0.5, actuatorsFrom="Nothing",pokeSpacing=(None if wfs_nsubx < 20 else 10), maxActDist=1.5, decayFactor=0.95,sendFullDM=0,reconLam=ngsLam))
dmOverview=dmOverview(dmInfoList,atmosGeom)

#reconstructor
this.tomoRecon=new()
r=this.tomoRecon
r.rcond=0.05 #condtioning value for SVD
r.recontype="pinv" #reconstruction type
r.pokeval=1. #strength of poke
r.gainFactor=0.5 #Loop gain
r.computeControl=1 #To compute the control matrix after poking
r.abortAfterPoke=0 # exits sim after computing the reconstruction matrix, if it is computed (does not affect when the poke is skipped with nopoke option)
r.reconmxFilename="rmx.fits"#control matrix name (will be created)
r.pmxFilename="pmx.fits"#interation matrix name (will be created)
