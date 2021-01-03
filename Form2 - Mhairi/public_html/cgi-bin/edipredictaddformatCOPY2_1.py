#!/usr/bin/python3

# Import modules required for linking to HTML forms, Oracle connection and templating
import cx_Oracle
import cgi
import cgitb
from jinja2 import Environment, FileSystemLoader
cgitb.enable(format='text/html')#do I still need this?


# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
if form.getvalue('EDI'):
   EDIselected = int(form.getvalue('EDI'))
else:
   EDIselected = "Not entered"

if form.getvalue('ZONE'):
    zoneID = int(form.getvalue('ZONE'))
else:
    zoneID = "Not entered"

#names=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104]
#for name in names:
#    namea=name
#EDIselected=1
#zoneID=0
if EDIselected>0 and zoneID>0:
    #Oracle connection to extract values specific to each zone.
    conn = cx_Oracle.connect("s1624036/temppass4@geoslearn")#change to hide password once in final directory - get Form 1 code
    c = conn.cursor()
    c.execute("SELECT ZONENAME, EDIRANK, AREAHA, HIGHHA, MEDHA, NFIHA, SPECIES, JUVCOUNT, TREECOUNT, HCRATE, MCRATE, NFIRATE, SPECIESRATE, POPRATE, JUVRATE, TREERATE, DBHRATE, EDIRATE, EMPTYHA FROM EDIPREDICT WHERE ID=%s"% zoneID)
    for row in c:
        ZONENAME=row[0]
        EDIRANK=row[1]
        area=row[2]
        HCHA=row[3]
        MCHA=row[4]
        NFIHA=row[5]
        SPECIES=row[6]
        JUVCOUNT=row[7]
        TREECOUNT=row[8]
        HCrate=row[9]
        MCrate=row[10]
        NFIrate=row[11]
        speciesrate=row[12]
        poprate=row[13]
        juvrate=row[14]
        treerate=row[15]
        DBHrate=row[16]
        EDIrate=row[17]
        EMPTYLAND=round(row[18],1)

    #sets targets dependant on user selection in form
    if EDIselected==1:
        HCtarget=0.05
        MCtarget=0.2
        NFItarget=0.03
        speciestarget=0.3
        juvtarget=0.2
        treetarget=0.2
        EDItarget=2
    elif EDIselected==2:
        HCtarget=0.05
        MCtarget=0.25
        NFItarget=0.05
        speciestarget=0.3
        juvtarget=0.22
        treetarget=0.22
        EDItarget=2.5
    elif EDIselected==3:
        HCtarget=0.05
        MCtarget=0.3
        NFItarget=0.1
        speciestarget=0.3
        juvtarget=0.22
        treetarget=0.24
        EDItarget=2.75
    elif EDIselected==4:
        HCtarget=0.1
        MCtarget=0.4
        NFItarget=0.1
        speciestarget=0.3
        juvtarget=0.26
        treetarget=0.26
        EDItarget=3
    elif EDIselected==5:
        HCtarget=0.12
        MCtarget=0.4
        NFItarget=0.15
        speciestarget=0.3
        juvtarget=0.28
        treetarget=0.28
        EDItarget=3.25
    elif EDIselected==6:
        HCtarget=0.15
        MCtarget=0.45
        NFItarget=0.2
        speciestarget=0.3
        juvtarget=0.3
        treetarget=0.3
        EDItarget=3.5
    elif EDIselected==7:
        HCtarget=0.2
        MCtarget=0.45
        NFItarget=0.3
        speciestarget=0.3
        juvtarget=0.3
        treetarget=0.32
        EDItarget=4
    elif EDIselected==8:
        HCtarget=0.35
        MCtarget=0.5
        NFItarget=0.5
        speciestarget=0.3
        juvtarget=0.32
        treetarget=0.32
        EDItarget=4.5
    elif EDIselected==9:
        HCtarget=0.5
        MCtarget=0.5
        NFItarget=0.55
        speciestarget=0.3
        juvtarget=0.32
        treetarget=0.32
        EDItarget=5
    elif EDIselected==10:
        HCtarget=0.6
        MCtarget=0.6
        NFItarget=0.7
        speciestarget=0.3
        juvtarget=0.35
        treetarget=0.35
        EDItarget=6

    #standardising factors using to limit each EDI factor to a scale ranging from 0 to 1.
    HCstandardiser=19.5
    MCstandardiser=27.65
    NFIstandardiser=20.13
    speciesstandardiser=0.41
    popstanderdiser=209.69
    juvstandardiser=2.69
    treestandardiser=14.65
    DBHstandardiser=55

    def limit(n, minn, maxn):
        if n<minn:
            return minn
        elif n>maxn:
            return maxn
        else:
            return n


    if EDIrate>EDItarget or EDIrate==EDItarget:#Filters out any zones which already meet the selected target
        Head="%s already meets the target selected."% ZONENAME #assigns output to a variable which is later connected to a template
        if speciesrate < speciestarget:
            improve="To further improve and maintain carbon sequestration, more juvenile trees of different species to those already existing should be planted. Improving species diversity is important to make city trees resilient from pests and disease. Planting more trees ensures carbon stores are replaced when older trees become a risk or begin to die."#some lit with recommended species diversity (10%same, something for genius etc)
        elif juvrate < juvtarget:
            improve="To further improve and maintain carbon sequestration, continual protection and planting more juvenile tree ensures carbon stores are replaced when older trees become a risk or begin to die."#ensures aging trees have a replacement
        else:
            improve="To further improve and maintain carbon sequestration, continual protection and conservation is vital."
    elif EDIrate<EDItarget:
        if treerate<treetarget: #increase tree count to meet target - also increases juv and species   10yrs to increase tree numbers
            additionalTreeha=(treetarget-treerate)*treestandardiser
            additionalTreecount=additionalTreeha*area
            newTreeCount=additionalTreecount+TREECOUNT
            newTreerate=(newTreeCount/area)/treestandardiser
            newJuvCount=additionalTreecount+JUVCOUNT
            newJuvrate=limit(((newJuvCount/area)/juvstandardiser),0,1)
            newSpeciesCount = limit((SPECIES+(additionalTreecount/4)),SPECIES,81)#alternative to below-limits species count to 80 regardless of previous species total and gives 4 trees for every new species planted - this should be increase?
            newSpeciesrate=limit((((newSpeciesCount)/newTreeCount)/speciesstandardiser),0,1)
            if additionalTreeha>2:
                if additionalTreeha>3:#introduces assumption trees are planted in close proximity - can't assume >0.5ha are planted together so NFI not increased
                    additionalMCperha=0.01#one plot size
                elif additionalTreeha>2:
                    additionalMCperha=0.005#half plot size
                newMCha=MCHA+(additionalMCperha*area)
                newMCfromTrees=round((additionalMCperha*area),1)#used for results
                newMCrate=limit((((newMCha/area)*100)/MCstandardiser),0,1)
            else:
                newMCrate=MCrate
                newMCha=MCHA
                newMCfromTrees=0
            newHCrate=HCrate
            newNFIrate=NFIrate
            newHCha=HCHA
            newNFIha=NFIHA
        else: # need to ensure variable names are consistent for next steps whilst retaining the original values for calculating the change for results
            newEDIrate=EDIrate
            newJuvrate=juvrate
            newSpeciesrate=speciesrate
            newTreerate=treerate
            newMCrate=MCrate
            newHCrate=HCrate
            newNFIrate=NFIrate
            newSpeciesCount=SPECIES
            newJuvCount=JUVCOUNT
            newTreeCount=TREECOUNT
            newMCha=MCHA
            newHCha=HCHA
            newNFIha=NFIHA
            newMCfromTrees=0
        newEDIrate=(2.5*newHCrate)+(1.5*newMCrate)+(newNFIrate*2)+ (newTreerate*0.667)+(newJuvrate*0.667)+(DBHrate*0.667)+(newSpeciesrate)+poprate
        #juveniles/planting new trees
        if newJuvrate<juvtarget and newEDIrate<EDItarget:
            additionalJuvha = (juvtarget-newJuvrate)*juvstandardiser
            additionalJuvcount = additionalJuvha*area
            newJuvCount = additionalJuvcount+newJuvCount
            newJuvrate = limit(((newJuvCount/area)/juvstandardiser),0,1)
            newTreeCount = additionalJuvcount+newTreeCount
            newTreerate = limit(((newTreeCount/area)/treestandardiser),0,1)
            newSpeciesCount = limit((SPECIES+(additionalJuvcount/4)),SPECIES,81)
            newSpeciesrate = limit(((newSpeciesCount/newTreeCount)/speciesstandardiser),0,1)
            if additionalJuvha>2:
                if additionalJuvha>3:#introduces assumption trees are planted in close proximity - can't assume >0.5ha are planted together so NFI not increased
                    additionalMCperha=0.01#one plot size - is this too much?
                elif additionalJuvha>2:
                    additionalMCperha=0.005#half plot size - is this too much?
                newMCha=MCHA+(additionalMCperha*area)
                newMCfromTrees=newMCha+newMCfromTrees#used for results
                newMCrate=limit((((newMCha/area)*100)/MCstandardiser),0,1)
        else:
            pass
        newEDIrate=(2.5*newHCrate)+(1.5*newMCrate)+(newNFIrate*2)+ (newTreerate*0.667)+(newJuvrate*0.667)+(DBHrate*0.667)+(newSpeciesrate)+poprate
        #species
        if newSpeciesrate<speciestarget and newEDIrate<EDItarget and newSpeciesCount<81:
            additionalSpeciesperTree=(speciestarget-newSpeciesrate)*speciesstandardiser
            additionalSpecies=additionalSpeciesperTree*newTreeCount
            if (newSpeciesCount+additionalSpecies)>81:#limits the total species count to 81 (which is the maximim currently recorded in every zone). Otherwise, it would recommend unlimited numbers of new species which is not practical
                additionalSpecies=81-newSpeciesCount
            else:
                pass
            newSpeciesCount=limit((newSpeciesCount+additionalSpecies),1,81)
            newJuvCount=newJuvCount+(additionalSpecies*4)
            newJuvrate=limit(((newJuvCount/area)/juvstandardiser),0,1)
            newTreeCount=newTreeCount+(additionalSpecies*4)#gives 2 trees for every new species - increase??
            newTreerate=limit(((newTreeCount/area)/treestandardiser),0,1)
            newSpeciesrate=limit(((newSpeciesCount/newTreeCount)/speciesstandardiser),0,1)

        else:
            pass
        newEDIrate=(2.5*newHCrate)+(1.5*newMCrate)+(newNFIrate*2)+ (newTreerate*0.667)+(newJuvrate*0.667)+(DBHrate*0.667)+(newSpeciesrate)+poprate
        #converting medium carbon land cover to high carbon
        if newEDIrate<EDItarget and newMCrate>(MCtarget*1.2):#MC minimum requirement if 20% converted to HC
            sufficientMC=1#Used for results
            if newMCrate>(MCtarget*1.3) and newHCrate<HCtarget: #convert Mc to HC (for large amount of MC)
                convertMCtoHC = MCrate*0.3#calculates how much of the MC rate is to be converted into HC.
            elif newMCrate>(MCtarget*1.2) and newHCrate<HCtarget:
                convertMCtoHC = MCrate*0.2
            else:
                convertMCtoHC=0
            newMCrate = newMCrate - convertMCtoHC
            MCtochangeha = ((convertMCtoHC*MCstandardiser)/100)*area#converts the rate to be changed in a ha value
            MCchangedtoHC = round(MCtochangeha,1)  #USED IN RESULTS
            newHCha = newHCha + MCtochangeha
            newHCrate = ((newHCha/area)*100)/ HCstandardiser
            newMCha = newMCha - MCtochangeha
            newMCrate = ((newMCha/area)*100)/ MCstandardiser
            if ((NFIrate/NFItarget)*area)>0.5 and MCtochangeha>1:#Minimum requirement for NFI is 0.5ha and only half of the additional HC is assumed to be NFI
                newNFIha = (MCtochangeha/2)+newNFIha
                newNFIfromconversion=round((MCtochangeha/2),1)#for results section
                newNFIrate = limit((((newNFIha/area)*100)/NFIstandardiser),0,1)
            else:
                newNFIrate = newNFIrate
                newNFIfromconversion=0
        else:#trees,juv,species meet target and MC isn't enough to be converted
            MCtochangeha=0
            MCchangedtoHC=0
            newNFIfromconversion=0
            sufficientMC=0
        newEDIrate= (newHCrate*2.5)+(newMCrate*1.5)+(newNFIrate*2)+(newTreerate*0.667)+(newJuvrate*0.667)+(DBHrate*0.667)+(newSpeciesrate)+poprate
        #Final step to increase NFI, HC and MC to ensure the final EDI meets the selected target
        if newEDIrate<EDItarget:
            EDIincreaseRequired=EDItarget - newEDIrate
            NFIincreaserequired=EDIincreaseRequired*0.27 #need to check with other values, excel shows 0.26
            NFIdecimalrequired=(NFIincreaserequired*NFIstandardiser)/100
            NFIharequired = limit((NFIdecimalrequired*area),0.5,area)#since NFI woodland is required to be at least 0.5ha, a minimum limit has been set
            newNFIha = newNFIha+NFIharequired
            newNFIrate = limit((((newNFIha/area)*100)/NFIstandardiser),0,1)
            newHCha = (NFIharequired/2)+newHCha#assume 50%woodland is HC and other 50% is MC (conservative assumption)
            newHCrate = limit((((newHCha/area)*100)/HCstandardiser),0,1)
            newMCha = (NFIharequired/2)+newMCha#assume 50%woodland is HC and other 50% is MC
            newMCrate = limit((((newMCha/area)*100)/MCstandardiser),0,1)
        else:
            pass
        newEDIrate = (newHCrate*2.5)+(newMCrate*1.5)+(newNFIrate*2)+(newTreerate*0.667)+(newJuvrate*0.667)+(DBHrate*0.667)+(newSpeciesrate)+poprate
        #variables for output
        #tree result variable
        newTreeCount=round((newTreerate*treestandardiser)*area)
        newJuvCount=round((newJuvrate*juvstandardiser)*area)
        additionalTrees=(newTreeCount-TREECOUNT)
        additionalJuv=newJuvCount-JUVCOUNT
        if additionalTrees>additionalJuv:
            newTrees=additionalTrees
        elif additionalTrees<additionalJuv:
            newTrees=additionalJuv
        else:
            newTrees=additionalTrees
        #species result variable
        newSpeciesCount=round(newSpeciesCount)
        additionalSpecies=round(newSpeciesCount-SPECIES)

        #NFI result variable (cumulative NFI throughout process so can't be extracted directly from one step)
        newNFIha=round((((newNFIrate*NFIstandardiser)/100)*area),2)
        if newNFIfromconversion>0:
            newNFIharesult=round((newNFIha-newNFIfromconversion-NFIHA),1)
        else:
            newNFIharesult=round((newNFIha-NFIHA),1)#how much additional NFI has been added compared to initial
        NFIadditionalland=round((newNFIharesult-EMPTYLAND),1)#identifies how much extra land is required that isn't derelict or landfill
        newMCharesult=round((newNFIharesult/2),2)
        newHCharesult=round((newNFIharesult/2),2)

        #Assigning strings for output in template
        if newEDIrate>EDItarget or newEDIrate==EDItarget:
            Head="The EDI target of %s was reached using the following methods:"% EDIselected#change target to rank
            if newTrees>0:#tree count is increased if species is increased, not always vice versa
                if additionalSpecies>0:#if new species are added, trees have also been added
                    if newMCfromTrees>0:#MC created from planting trees
                        Tree="Planting %s new trees including %s new species will increase carbon seqestration as they grow into juveniles in 10-20 years depending on the species. This creates %s ha of medium carbon land cover (scattered tree cover)" % (newTrees, additionalSpecies,newMCfromTrees)
                    else:
                        Tree="Planting %s new trees including %s new species will increase carbon seqestration as they grow into juveniles in 10-20 years depending on the species." % (newTrees, additionalSpecies)
                elif additionalSpecies==0:
                    if newMCfromTrees>0:#MC created from planting trees
                        Tree="Planting %s new trees of species already existing within the zone will increase carbon seqestration as they grow into juveniles in 10-20 years depending on the species. This creates %s ha of medium carbon land cover (scattered tree cover)" % (newTrees, newMCfromTrees)
                    else:
                        Tree="Planting %s new trees of species already existing within the zone will increase carbon seqestration as they grow into juveniles in 10-20 years depending on the species."% newTrees
                else:
                    pass
                if MCchangedtoHC>0:#converting MC to HC
                    if newNFIfromconversion>0 and newNFIharesult>0:#this only includes NFI created from changing MC to HC
                        Carbon="%s ha of medium carbon land cover (scattered tree cover) should be converted into high carbon land cover (dense canopy cover) to increase the amount of carbon sequstration without increasing area. This can be achieved by protecting trees allowing them to mature. Assuming the medium carbon land cover (scattered tree cover) changed to high carbon land cover (dense canopy cover) is clustered and in close proximity to already existing woodland, an additional %s ha of woodland will also be created."% (MCchangedtoHC,newNFIfromconversion)
                    else:
                        Carbon="%s ha of medium carbon land cover (scattered tree cover) should be converted into high carbon land cover (dense canopy cover) to increase the amount of carbon sequstration without increasing area. This can be achieved by protecting trees allowing them to mature."% MCchangedtoHC
                elif MCchangedtoHC==0:
                    if sufficientMC==1:
                        Carbon="There is already sufficient high carbon land cover (dense canopy cover) within this zone so it is not necessary to improve medium carbon land cover (scattered tree cover)"
                    elif sufficientMC==0:
                        Carbon="There is not enough medium carbon land cover (scattered tree cover) to be converted to high carbon land cover (dense canopy cover) within this zone."
            elif newTrees==0 and MCchangedtoHC>0:#has MC been changed to HC, with no additional council trees or species
                Tree="No more trees are required to reach this EDI target"
                if newNFIfromconversion>0:#this only includes NFI created from changing MC to HC
                    Carbon="%s ha of medium carbon land cover (scattered tree cover) should be converted into high carbon land cover (dense canopy cover) to increase the amount of carbon sequstration without increasing area. This can be achieved by protecting trees allowing them to mature. Assuming the medium carbon land cover (scattered tree cover) changed to high carbon land cover (dense canopy cover) is clustered and in close proximity to already existing woodland, an additional %s ha of woodland will also be created."% (MCchangedtoHC,newNFIfromconversion)
                else:
                    Carbon="%s ha of medium carbon land cover (scattered tree cover) should be converted into high carbon land cover (dense canopy cover) to increase the amount of carbon sequstration without increasing area. This can be achieved by protecting trees allowing them to mature."% MCchangedtoHC
            elif newTrees==0 and MCchangedtoHC==0:
                Tree="No more trees are required to reach this EDI target"
                if sufficientMC==1:
                    Carbon="There is already sufficient high carbon land cover (dense canopy cover) within this zone so it is not necessary to improve medium carbon land cover"
                elif sufficientMC==0:
                    Carbon="There is not enough medium carbon land cover (scattered tree cover) to be converted to high carbon land cover (dense canopy cover) within this zone."
            else:
                pass
            if newNFIharesult>0:#results for NFI
                Forest="%s ha of new woodland is required, consisting of %s ha of high carbon land cover (dense canopy cover) and %s ha of medium carbon (scattered tree cover)."% (newNFIharesult,newHCharesult,newMCharesult)
                if newNFIharesult<EMPTYLAND and EMPTYLAND>0:
                    Forest1="There is sufficient empty land (derelict, vacant or landfill sites) in this zone that could be afforested to create this additional woodland."
                elif newNFIharesult>EMPTYLAND and EMPTYLAND>0:
                    Forest1="There is only %s ha of empty land (derelict, vacant or landfill sites) within this zone so an additional %s ha of another land use would need to be afforested to reach this EDI target"% (EMPTYLAND,NFIadditionalland)
                elif newNFIharesult>EMPTYLAND and EMPTYLAND==0 and NFIadditionalland>0:
                    Forest1="There is no empty land (derelict, vacant or landfill sites) within this zone so %s ha of another land use would need to be afforested to reach this EDI target"% NFIadditionalland
            elif newNFIharesult==0:
                if newNFIfromconversion>0:
                    Forest="Assuming the medium carbon land cover (scattered tree cover) changed to high carbon land cover (dense canopy cover) is clustered and in close proximity to already existing woodland, an additional %s ha of woodland will also be created."% newNFIfromconversion
                    Forest1=""
                else:
                    Forest="No additional woodland is required to reach the EDI target selected."
                    Forest1=""
        else:
            error=TRUE
    else:
        error=TRUE
else:
    pass

#jinga2 links to templates - there are two templates depending on the selected EDI target
if EDIselected==0 or zoneID==0:
    def printblank_html():
            env = Environment(loader=FileSystemLoader('.'))
            temp = env.get_template('edipredictformatblank.html')
            inpSelect="Please select"
            print(temp.render(name=inpSelect))

    if __name__ == '__main__':
    	       printblank_html()
elif EDIselected>EDIRANK:
    def print_html():
            env = Environment(loader=FileSystemLoader('.'))
            temp = env.get_template('edipredictformatting.html')
            inpHead=Head
            inpName=ZONENAME
            inpTarget=EDIselected
            inpForest = Forest
            inpForest1 = Forest1
            inpTree = Tree
            inpCarbon = Carbon
            print(temp.render(head=inpHead, name = inpName, edi=inpTarget,forest=inpForest, forest1=inpForest1, tree=inpTree, carbon=inpCarbon))

    if __name__ == '__main__':
	       print_html()
elif EDIselected<=EDIRANK:
    def print1_html():
            env = Environment(loader=FileSystemLoader('.'))
            temp = env.get_template('edipredictformat1.html')
            inpName=ZONENAME
            impImprove = improve
            print(temp.render(name=inpName, improve = improve))

    if __name__ == '__main__':
    	       print1_html()
