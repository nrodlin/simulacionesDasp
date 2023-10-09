#mpirun -np 1 -hostlist n1-c437  /usr/local/bin/mpipython $PWD/thisfile.py
#Python code created using the simulation setup GUI...
#Order of execution may not be quite optimal - you can always change by hand
#for large simulations - typically, the order of sends and gets may not be
#quite right.  Anyway, enjoy...
import numpy
import util.Ctrl
import science.iscrn
import science.tomoRecon
import science.iatmos
import science.xinterp_dm
import science.wfscent
import science.science
ctrl=util.Ctrl.Ctrl(globals=globals())
print "Rank %d imported modules"%ctrl.rank
#Set up the science modules...
iscrnList=[]
reconList=[]
iatmosList=[]
dmList=[]
wfscentList=[]
scienceList=[]
if not "nopoke" in ctrl.userArgList:ctrl.doInitialPokeThenRun()
#Add any personal code after this line and before the next, and it won't get overwritten
if ctrl.rank==0:
    iscrnList.append(science.iscrn.iscrn(None,ctrl.config,args={},idstr="allLayers"))
    iatmosList.append(science.iatmos.iatmos({"allLayers":iscrnList[0],},ctrl.config,args={},idstr="1"))
    dmList.append(science.xinterp_dm.dm(None,ctrl.config,args={},idstr="dm0path1"))
    wfscentList.append(science.wfscent.wfscent(dmList[0],ctrl.config,args={},idstr="1"))
    iatmosList.append(science.iatmos.iatmos({"allLayers":iscrnList[0],},ctrl.config,args={},idstr="2"))
    dmList.append(dmList[0].addNewIdObject(None,"dm0path2"))
    wfscentList.append(science.wfscent.wfscent(dmList[1],ctrl.config,args={},idstr="2"))
    iatmosList.append(science.iatmos.iatmos({"allLayers":iscrnList[0],},ctrl.config,args={},idstr="3"))
    dmList.append(dmList[0].addNewIdObject(None,"dm0path3"))
    wfscentList.append(science.wfscent.wfscent(dmList[2],ctrl.config,args={},idstr="3"))
    iatmosList.append(science.iatmos.iatmos({"allLayers":iscrnList[0],},ctrl.config,args={},idstr="4"))
    dmList.append(dmList[0].addNewIdObject(None,"dm0path4"))
    wfscentList.append(science.wfscent.wfscent(dmList[3],ctrl.config,args={},idstr="4"))
    iatmosList.append(science.iatmos.iatmos({"allLayers":iscrnList[0],},ctrl.config,args={},idstr="5"))
    dmList.append(dmList[0].addNewIdObject(None,"dm0path5"))
    wfscentList.append(science.wfscent.wfscent(dmList[4],ctrl.config,args={},idstr="5"))
    iatmosList.append(science.iatmos.iatmos({"allLayers":iscrnList[0],},ctrl.config,args={},idstr="6"))
    dmList.append(dmList[0].addNewIdObject(None,"dm0path6"))
    wfscentList.append(science.wfscent.wfscent(dmList[5],ctrl.config,args={},idstr="6"))
    iatmosList.append(science.iatmos.iatmos({"allLayers":iscrnList[0],},ctrl.config,args={},idstr="7"))
    dmList.append(dmList[0].addNewIdObject(None,"dm0path7"))
    wfscentList.append(science.wfscent.wfscent(dmList[6],ctrl.config,args={},idstr="7"))
    reconList.append(science.tomoRecon.recon({"1":wfscentList[0],"2":wfscentList[1],"3":wfscentList[2],"4":wfscentList[3],"5":wfscentList[4],"6":wfscentList[5],"7":wfscentList[6],},ctrl.config,args={},idstr="recon"))
    iatmosList.append(science.iatmos.iatmos({"allLayers":iscrnList[0],},ctrl.config,args={},idstr="sci1"))
    dmList.append(dmList[0].addNewIdObject(None,"dm0pathsci1"))
    scienceList.append(science.science.science(dmList[7],ctrl.config,args={},idstr="sci1"))
    """iatmosList.append(science.iatmos.iatmos({"allLayers":iscrnList[0],},ctrl.config,args={},idstr="sci2"))
    dmList.append(dmList[0].addNewIdObject(None,"dm0pathsci2"))
    scienceList.append(science.science.science(dmList[8],ctrl.config,args={},idstr="sci2"))
    iatmosList.append(science.iatmos.iatmos({"allLayers":iscrnList[0],},ctrl.config,args={},idstr="sci3"))
    dmList.append(dmList[0].addNewIdObject(None,"dm0pathsci3"))
    scienceList.append(science.science.science(dmList[9],ctrl.config,args={},idstr="sci3"))
    iatmosList.append(science.iatmos.iatmos({"allLayers":iscrnList[0],},ctrl.config,args={},idstr="sci4"))
    dmList.append(dmList[0].addNewIdObject(None,"dm0pathsci4"))
    scienceList.append(science.science.science(dmList[10],ctrl.config,args={},idstr="sci4"))
    iatmosList.append(science.iatmos.iatmos({"allLayers":iscrnList[0],},ctrl.config,args={},idstr="sci5"))
    dmList.append(dmList[0].addNewIdObject(None,"dm0pathsci5"))
    scienceList.append(science.science.science(dmList[11],ctrl.config,args={},idstr="sci5"))
    iatmosList.append(science.iatmos.iatmos({"allLayers":iscrnList[0],},ctrl.config,args={},idstr="sci6"))
    dmList.append(dmList[0].addNewIdObject(None,"dm0pathsci6"))
    scienceList.append(science.science.science(dmList[12],ctrl.config,args={},idstr="sci6"))
    iatmosList.append(science.iatmos.iatmos({"allLayers":iscrnList[0],},ctrl.config,args={},idstr="sci7"))
    dmList.append(dmList[0].addNewIdObject(None,"dm0pathsci7"))
    scienceList.append(science.science.science(dmList[13],ctrl.config,args={},idstr="sci7"))"""
    dmList[0].newParent({"1":reconList[0],"2":iatmosList[0],},"dm0path1")
    dmList[1].newParent({"1":reconList[0],"2":iatmosList[1],},"dm0path2")
    dmList[2].newParent({"1":reconList[0],"2":iatmosList[2],},"dm0path3")
    dmList[3].newParent({"1":reconList[0],"2":iatmosList[3],},"dm0path4")
    dmList[4].newParent({"1":reconList[0],"2":iatmosList[4],},"dm0path5")
    dmList[5].newParent({"1":reconList[0],"2":iatmosList[5],},"dm0path6")
    dmList[6].newParent({"1":reconList[0],"2":iatmosList[6],},"dm0path7")
    dmList[7].newParent({"1":reconList[0],"2":iatmosList[7],},"dm0pathsci1")
    """dmList[8].newParent({"1":reconList[0],"2":iatmosList[8],},"dm0pathsci2")
    dmList[9].newParent({"1":reconList[0],"2":iatmosList[9],},"dm0pathsci3")
    dmList[10].newParent({"1":reconList[0],"2":iatmosList[10],},"dm0pathsci4")
    dmList[11].newParent({"1":reconList[0],"2":iatmosList[11],},"dm0pathsci5")
    dmList[12].newParent({"1":reconList[0],"2":iatmosList[12],},"dm0pathsci6")
    dmList[13].newParent({"1":reconList[0],"2":iatmosList[13],},"dm0pathsci7")"""
    #execOrder=[iscrnList[0],iatmosList[0],dmList[0],wfscentList[0],iatmosList[1],dmList[1],wfscentList[1],iatmosList[2],dmList[2],wfscentList[2],iatmosList[3],dmList[3],wfscentList[3],iatmosList[4],dmList[4],wfscentList[4],iatmosList[5],dmList[5],wfscentList[5],iatmosList[6],dmList[6],wfscentList[6],reconList[0],iatmosList[7],dmList[7],scienceList[0],iatmosList[8],dmList[8],scienceList[1],iatmosList[9],dmList[9],scienceList[2],iatmosList[10],dmList[10],scienceList[3],iatmosList[11],dmList[11],scienceList[4],iatmosList[12],dmList[12],scienceList[5],iatmosList[13],dmList[13],scienceList[6],]
    execOrder=[iscrnList[0],iatmosList[0],dmList[0],wfscentList[0],iatmosList[1],dmList[1],wfscentList[1],iatmosList[2],dmList[2],wfscentList[2],iatmosList[3],dmList[3],wfscentList[3],iatmosList[4],dmList[4],wfscentList[4],iatmosList[5],dmList[5],wfscentList[5],iatmosList[6],dmList[6],wfscentList[6],reconList[0],iatmosList[7],dmList[7],scienceList[0],]

    ctrl.mainloop(execOrder)
print "Simulation finished..."
#Add any personal code after this, and it will not get overwritten
