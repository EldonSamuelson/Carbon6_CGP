#!/usr/bin/python3

# Import modules required for linking to HTML forms, Oracle connection and templating
import cx_Oracle
import cgi
import cgitb
from jinja2 import Environment, FileSystemLoader
cgitb.enable(format='text/html')#do I still need this?


# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields and assign to variables
if form.getvalue('EDI'):
   EDIselected = int(form.getvalue('EDI'))
else:
   EDIselected = "Not entered"

if form.getvalue('ZONE'):
    zoneID = int(form.getvalue('ZONE'))
else:
    zoneID = "Not entered"


#condition for confirming valid options are selected in form
if EDIselected>0 and zoneID>0:
    #Oracle connection to extract values specific to each zone.
    conn = cx_Oracle.connect("s1624036/temppass4@geoslearn")
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

    #sets targets for each variable, dependant on user selection in form
    if EDIselected==1:
        HCtarget=0.05 #percentage High Carbon land cover
        MCtarget=0.2 #percentage Medium Carbon land cover
        NFItarget=0.03 #percentage Woodland Cover
        speciestarget=0.3 #Species Diversity
        juvtarget=0.2 #Juvenile trees per hectare
        treetarget=0.2 #Trees per hectare
        EDItarget=2 #EDI value out of 10 (EDI selected is a relative number)
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

    #standardising factors using to limit  factor to a scale ranging from 0 to 1 in the formation of the EDI.
    HCstandardiser=19.5
    MCstandardiser=27.65
    NFIstandardiser=20.13
    speciesstandardiser=0.41
    juvstandardiser=2.69
    treestandardiser=14.65

    def limit(n, minn, maxn):
        #Function to ensure all EDI factors do not exceed the maximum value (1)
        if n<minn:
            return minn
        elif n>maxn:
            return maxn
        else:
            return n

    #Filters out any zones which already meet the selected target
    if EDIrate>EDItarget or EDIrate==EDItarget:
        #assigns output to a variable which is later connected to a template
        Head="%s already meets the target selected."% ZONENAME
        if speciesrate < speciestarget:
            improve="To further improve and maintain carbon sequestration, more juvenile trees of different species to those already existing should be planted. Improving species diversity is important to make city trees resilient from pests and disease. Planting more trees ensures carbon stores are replaced when older trees become a risk or begin to die."
        elif juvrate < juvtarget:
            improve="To further improve and maintain carbon sequestration, continual protection and planting more juvenile tree ensures carbon stores are replaced when older trees become a risk or begin to die."#ensures aging trees have a replacement
        else:
            improve="To further improve and maintain carbon sequestration, continual protection and conservation is vital."
    #Remaining code is to increase the EDI score to reach target
    elif EDIrate<EDItarget:
        #increase tree count
        if treerate<treetarget:
            #calculates increase in trees per hectare required
            additionalTreeha=(treetarget-treerate)*treestandardiser
            #converts trees per hectares to number of trees for the zone.
            additionalTreecount=additionalTreeha*area
            #new rates for trees, juveniles and species recalculated
            newTreeCount=additionalTreecount+TREECOUNT
            newTreerate=(newTreeCount/area)/treestandardiser
            newJuvCount=additionalTreecount+JUVCOUNT
            #rate is limited to 1 (for consistency in calculating EDI)
            newJuvrate=limit(((newJuvCount/area)/juvstandardiser),0,1)
            #An additional species is added for every four trees
            #Total species is limited to 81 (current maximum for one zone)
            newSpeciesCount = limit((SPECIES+(additionalTreecount/4)),SPECIES,81)
            newSpeciesrate=limit((((newSpeciesCount)/newTreeCount)/speciesstandardiser),0,1)
            #Medium carbon land cover is added if more than 2 trees/ha are added
            if additionalTreeha>2:
                #assumption trees are planted in close proximity
                #can't assume >0.5ha are planted together so NFI not increased
                if additionalTreeha>3:
                    #one fieldwork plot area medium carbon is added
                    additionalMCperha=0.01
                elif additionalTreeha>2:
                    #half of one fieldwork plot area medium carbon is added
                    additionalMCperha=0.005
                newMCha=MCHA+(additionalMCperha*area)
                #Variable required for output
                newMCfromTrees=round((additionalMCperha*area),1)
                newMCrate=limit((((newMCha/area)*100)/MCstandardiser),0,1)
            else:
                newMCrate=MCrate
                newMCha=MCHA
                newMCfromTrees=0
            newHCrate=HCrate
            newNFIrate=NFIrate
            newHCha=HCHA
            newNFIha=NFIHA
        else: # ensures variables are consistent for next steps whilst retaining the original values
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
        #calculates new EDI rate following addition of trees
        newEDIrate=(2.5*newHCrate)+(1.5*newMCrate)+(newNFIrate*2)+ (newTreerate*0.667)+(newJuvrate*0.667)+(DBHrate*0.667)+(newSpeciesrate)+poprate
        #increase juvenile count to reach target
        if newJuvrate<juvtarget and newEDIrate<EDItarget:
            additionalJuvha = (juvtarget-newJuvrate)*juvstandardiser#calculates increase in juveniles per hectare required
            additionalJuvcount = additionalJuvha*area#converts juveniles per hectares in number of trees for the zone.
            newJuvCount = additionalJuvcount+newJuvCount
            newJuvrate = limit(((newJuvCount/area)/juvstandardiser),0,1)
            newTreeCount = additionalJuvcount+newTreeCount
            newTreerate = limit(((newTreeCount/area)/treestandardiser),0,1)
            newSpeciesCount = limit((SPECIES+(additionalJuvcount/4)),SPECIES,81)
            newSpeciesrate = limit(((newSpeciesCount/newTreeCount)/speciesstandardiser),0,1)
            if additionalJuvha>2:#medium carbon (scattered trees) land cover is increased only when there is at least 2 additional  trees per hectare.
                #introduces assumption trees are planted in close proximity
                #can't assume >0.5ha are planted together so NFI not increased
                if additionalJuvha>3:
                    additionalMCperha=0.01#equivalent to 1 fieldwork plot (conservative measure)
                elif additionalJuvha>2:
                    additionalMCperha=0.005
                newMCha=MCHA+(additionalMCperha*area)
                newMCfromTrees=newMCha+newMCfromTrees#used for results
                newMCrate=limit((((newMCha/area)*100)/MCstandardiser),0,1)
        else:
            pass
        #calculates new EDI rate following addition of juvenile trees
        newEDIrate=(2.5*newHCrate)+(1.5*newMCrate)+(newNFIrate*2)+ (newTreerate*0.667)+(newJuvrate*0.667)+(DBHrate*0.667)+(newSpeciesrate)+poprate
        #increase species diversity to reach target
        if newSpeciesrate<speciestarget and newEDIrate<EDItarget and newSpeciesCount<81:
            additionalSpeciesperTree=(speciestarget-newSpeciesrate)*speciesstandardiser
            additionalSpecies=additionalSpeciesperTree*newTreeCount
            #limits the total species count to 81 (which is the maximum currently recorded in every zone).
            #Otherwise, it would recommend unlimited numbers of new species which is not practical.
            if (newSpeciesCount+additionalSpecies)>81:
                additionalSpecies=81-newSpeciesCount
            else:
                pass
            newSpeciesCount=limit((newSpeciesCount+additionalSpecies),1,81)
            #four additional trees are added for every additional species.
            newJuvCount=newJuvCount+(additionalSpecies*4)
            newJuvrate=limit(((newJuvCount/area)/juvstandardiser),0,1)
            newTreeCount=newTreeCount+(additionalSpecies*4)
            newTreerate=limit(((newTreeCount/area)/treestandardiser),0,1)
            newSpeciesrate=limit(((newSpeciesCount/newTreeCount)/speciesstandardiser),0,1)

        else:
            pass
        newEDIrate=(2.5*newHCrate)+(1.5*newMCrate)+(newNFIrate*2)+ (newTreerate*0.667)+(newJuvrate*0.667)+(DBHrate*0.667)+(newSpeciesrate)+poprate
        #convert medium carbon land cover to high carbon
        if newEDIrate<EDItarget and newMCrate>(MCtarget*1.2):#MC minimum requirement if 20% converted to HC
            #Variable assigned to be used for the output
            sufficientMC=1
            #Medium carbon land cover is converted to high
            #Ensures medium carbon land cover remains greater than the target for the selected EDI
            if newMCrate>(MCtarget*1.3) and newHCrate<HCtarget:
                #calculates how much of the MC rate is to be converted into HC.
                convertMCtoHC = MCrate*0.3
            elif newMCrate>(MCtarget*1.2) and newHCrate<HCtarget:
                convertMCtoHC = MCrate*0.2
            else:
                #if high cabon land cover meets the target, no addtion is required
                convertMCtoHC=0
            newMCrate = newMCrate - convertMCtoHC
            #converts the rate to be changed in a ha value
            MCtochangeha = ((convertMCtoHC*MCstandardiser)/100)*area
            #assign conversion quantity to variable for output
            MCchangedtoHC = round(MCtochangeha,1)
            #new rates are calculated
            newHCha = newHCha + MCtochangeha
            newHCrate = limit((((newHCha/area)*100)/ HCstandardiser),0,1)
            newMCha = newMCha - MCtochangeha
            newMCrate = limit((((newMCha/area)*100)/ MCstandardiser),0,1)
            #Minimum requirement for NFI woodland is 0.5ha
            #only half of the additional high carbon is assumed to be NFI
            if ((NFIrate/NFItarget)*area)>0.5 and MCtochangeha>1:
                newNFIha = (MCtochangeha/2)+newNFIha
                #assigned to variable to be used in output
                newNFIfromconversion=round((MCtochangeha/2),1)
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
        #Final step to ensure the final EDI meets the selected target
        #NFI woodland, high carbon and medium carbon land cover are increased
        if newEDIrate<EDItarget:
            #remaining EDI increase required to meet target
            EDIincreaseRequired=EDItarget - newEDIrate
            #0.27 represents relative weighting contribution to EDI increase
            NFIincreaserequired=EDIincreaseRequired*0.27
            NFIdecimalrequired=(NFIincreaserequired*NFIstandardiser)/100
            #since NFI woodland is required to be at least 0.5ha, a minimum limit has been set
            NFIharequired = limit((NFIdecimalrequired*area),0.5,area)
            #new rates calculated
            newNFIha = newNFIha+NFIharequired
            newNFIrate = limit((((newNFIha/area)*100)/NFIstandardiser),0,1)
            #assume 50% woodland is high carbon and other 50% is medium carbon land cover
            newHCha = (NFIharequired/2)+newHCha
            newHCrate = limit((((newHCha/area)*100)/HCstandardiser),0,1)
            newMCha = (NFIharequired/2)+newMCha
            newMCrate = limit((((newMCha/area)*100)/MCstandardiser),0,1)
        else:
            pass
        newEDIrate = (newHCrate*2.5)+(newMCrate*1.5)+(newNFIrate*2)+(newTreerate*0.667)+(newJuvrate*0.667)+(DBHrate*0.667)+(newSpeciesrate)+poprate

        #process variables for output
        #tree result variable - calculated from the new tree and juvenile rates
        #rounding is required to give whole numbers for output.
        newTreeCount=round((newTreerate*treestandardiser)*area)
        newJuvCount=round((newJuvrate*juvstandardiser)*area)
        additionalTrees=(newTreeCount-TREECOUNT)
        additionalJuv=newJuvCount-JUVCOUNT
        #number of new trees is equal to the greatest number, either trees or juveniles
        if additionalTrees>additionalJuv:
            newTrees=additionalTrees
        elif additionalTrees<additionalJuv:
            newTrees=additionalJuv
        else:
            newTrees=additionalTrees

        #species result variable
        #the most recent record of Species count is the total number of species
        newSpeciesCount=round(newSpeciesCount)
        additionalSpecies=round(newSpeciesCount-SPECIES)

        #NFI result variable (cumulative NFI throughout process so can't be extracted directly from one step)
        newNFIha=round((((newNFIrate*NFIstandardiser)/100)*area),2)
        if newNFIfromconversion>0:
            newNFIharesult=round((newNFIha-newNFIfromconversion-NFIHA),1)
        else:
            #calculates how much additional NFI has been added compared to initial
            newNFIharesult=round((newNFIha-NFIHA),1)
        #identifies how much extra land is required that isn't derelict or landfill
        NFIadditionalland=round((newNFIharesult-EMPTYLAND),1)
        #High and Medium Carbon from NFI (final step) is assigned to variables
        newMCharesult=round((newNFIharesult/2),2)
        newHCharesult=round((newNFIharesult/2),2)

        #Assigning strings for output in template
        if newEDIrate>EDItarget or newEDIrate==EDItarget:
            Head="The EDI target of %s was reached using the following methods:"% EDIselected
            if newTrees>0:
                if additionalSpecies>0:#if new species are added, trees have also been added
                    if newMCfromTrees>0:#MC created from planting trees
                        Tree="Planting %s new trees including %s new species will increase carbon seqestration as they grow into juveniles in 10-20 years depending on the species. This creates %s ha of medium carbon sequestering land cover (scattered tree cover)." % (newTrees, additionalSpecies,newMCfromTrees)
                    else:
                        Tree="Planting %s new trees including %s new species will increase carbon seqestration as they grow into juveniles in 10-20 years depending on the species." % (newTrees, additionalSpecies)
                elif additionalSpecies==0:
                    if newMCfromTrees>0:#MC created from planting trees
                        Tree="Planting %s new trees of species already existing within the zone will increase carbon seqestration as they grow into juveniles in 10-20 years depending on the species. This creates %s ha of medium carbon sequestering land cover (scattered tree cover)." % (newTrees, newMCfromTrees)
                    else:
                        Tree="Planting %s new trees of species already existing within the zone will increase carbon seqestration as they grow into juveniles in 10-20 years depending on the species."% newTrees
                else:
                    pass
                if MCchangedtoHC>0:#converting MC to HC
                    if newNFIfromconversion>0 and newNFIharesult>0:#this only includes NFI created from changing MC to HC
                        Carbon="%s ha of medium carbon sequestering land cover (scattered tree cover) should be converted into high carbon sequestering land cover (dense canopy cover) to increase the amount of carbon sequstration without increasing area. This can be achieved by protecting trees allowing them to mature. Assuming the medium carbon sequestering land cover changed to high carbon sequestering land cover is clustered and in close proximity to already existing woodland, an additional %s ha of woodland will also be created."% (MCchangedtoHC,newNFIfromconversion)
                    else:
                        Carbon="%s ha of medium carbon sequestering land cover (scattered tree cover) should be converted into high carbon sequestering land cover (dense canopy cover) to increase the amount of carbon sequstration without increasing area. This can be achieved by protecting trees allowing them to mature."% MCchangedtoHC
                elif MCchangedtoHC==0:
                    if sufficientMC==1:
                        Carbon="There is already sufficient high carbon sequestering land cover (dense canopy cover) within this zone so it is not necessary to improve medium carbon sequestering land cover (scattered tree cover)."
                    elif sufficientMC==0:
                        Carbon="There is not enough medium carbon sequestering land cover (scattered tree cover) to be converted to high carbon sequestering land cover (dense canopy cover) within this zone."
            elif newTrees==0 and MCchangedtoHC>0:#has MC been changed to HC, with no additional council trees or species
                Tree="No more trees are required to reach this EDI target."
                if newNFIfromconversion>0:#this only includes NFI created from changing MC to HC
                    Carbon="%s ha of medium carbon sequestering land cover (scattered tree cover) should be converted into high carbon sequestering land cover (dense canopy cover) to increase the amount of carbon sequstration without increasing area. This can be achieved by protecting trees allowing them to mature. Assuming the medium carbon sequestering land cover changed to high carbon sequestering land cover is clustered and in close proximity to already existing woodland, an additional %s ha of woodland will also be created."% (MCchangedtoHC,newNFIfromconversion)
                else:
                    Carbon="%s ha of medium carbon sequestering land cover (scattered tree cover) should be converted into high carbon sequestering land cover (dense canopy cover) to increase the amount of carbon sequstration without increasing area. This can be achieved by protecting trees allowing them to mature."% MCchangedtoHC
            elif newTrees==0 and MCchangedtoHC==0:
                Tree="No more trees are required to reach this EDI target."
                if sufficientMC==1:
                    Carbon="There is already sufficient high carbon sequestering land cover (dense canopy cover) within this zone so it is not necessary to improve medium carbon sequestering land cover."
                elif sufficientMC==0:
                    Carbon="There is not enough medium carbon sequestering land cover (scattered tree cover) to be converted to high carbon sequestering land cover (dense canopy cover) within this zone."
            else:
                pass
            if newNFIharesult>0:
                Forest="%s ha of new woodland is required, consisting of %s ha of high carbon sequestering land cover (dense canopy cover) and %s ha of medium carbon sequestering land cover (scattered tree cover)."% (newNFIharesult,newHCharesult,newMCharesult)
                if newNFIharesult<EMPTYLAND and EMPTYLAND>0:
                    Forest1="There is sufficient empty land (derelict, vacant or landfill sites) in this zone that could be afforested to create this additional woodland."
                elif newNFIharesult>EMPTYLAND and EMPTYLAND>0:
                    Forest1="There is only %s ha of empty land (derelict, vacant or landfill sites) within this zone so an additional %s ha of another land use would need to be afforested to reach this EDI target."% (EMPTYLAND,NFIadditionalland)
                elif newNFIharesult>EMPTYLAND and EMPTYLAND==0 and NFIadditionalland>0:
                    Forest1="There is no empty land (derelict, vacant or landfill sites) within this zone so %s ha of another land use would need to be afforested to reach this EDI target."% NFIadditionalland
            elif newNFIharesult==0:
                if newNFIfromconversion>0:
                    Forest="Assuming the medium carbon sequestering land cover (scattered tree cover) changed to high carbon sequestering land cover (dense canopy cover) is clustered and in close proximity to already existing woodland, an additional %s ha of woodland will also be created."% newNFIfromconversion
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

#jinga2 links to templates
if EDIselected==0 or zoneID==0:
    #Used to ensure no errors occur and to give instruction to user.
    def printblank_html():
            env = Environment(loader=FileSystemLoader('.'))
            temp = env.get_template('edipredictformatblank.html')
            inpSelect="Please select"
            print(temp.render(name=inpSelect))

    if __name__ == '__main__':
    	       printblank_html()
elif EDIselected>EDIRANK:
    #link to template for improvements in the EDI
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
    #template for zone already meeting selected EDI selected
    def print1_html():
            env = Environment(loader=FileSystemLoader('.'))
            temp = env.get_template('edipredictformat1.html')
            inpName=ZONENAME
            impImprove = improve
            print(temp.render(name=inpName, improve = improve))

    if __name__ == '__main__':
    	       print1_html()
