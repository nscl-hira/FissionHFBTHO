#!/usr/bin/env python3
# Quick and dirty script to pull out the important information from 
# the output files of HFBTHO in this directory
# and place it in a json file
# Adam Anthony 4/3/2019


import matplotlib.pyplot as plt
import sys
import glob
import json

if len(sys.argv) > 3:
    print("""\
Usage: datToJson.py [name]
    Converts all of the thoout*.dat files in this directory
    to a JSON file with [name]
    If [name] is not given then summary.json is used
""")
    exit(1)

#Get a list of files to load
fileList = glob.glob("thoout*.dat")
outDict = {}

for fName in fileList:
    with open(fName) as file:
        # Split file and get the table of values
        fIn = file.read().split("REGULAR STAGE")
    print("Processing %s" % fName)
    #Dictionary to hold information about the run
    resTable = {}

    #Get characteristics of the run
    runInfo = fIn[0].split("Characteristics of the run")[-1]\
                    .split("---------------------------------------")[1]\
                    .split("\n")

    # Nucleus: 2
    # Basis deformation 5
    # Energy functional 14
    # Constraint 18-18+1+N
    # Temp 18+2+N 
    
    resTable["Nucleus"] = runInfo[2].split(":")[-1].strip()
    resTable["BasisDeformation.beta0"] = float(runInfo[5].split()[-3])
    resTable["BasisDeformation.q"] = float(runInfo[5].split()[-1])
    
    #Look if there are constraints
    if runInfo[18].split()[-1].strip() == "ON":
        resTable["Constraints"] = {}        
        for line in runInfo[19:]:
            if "Constraint" in line:
                resTable["Constraints"][int(line.split("=")[-2].split()[0])]\
                    = float(line.split("=")[-1].strip())
            else:
                break

    nConst = len(resTable.get("Constraints", {}))

    #Get the table of itertions
    enTable = fIn[-1].split("si=")[0].split("\n")
    
    #Figure out if this converged
    conv = "converged" in enTable[-1]
    resTable["Converged"] = conv
    #Try to get the time if it didn't time out
    try:
        #Get the CPU time it took
        time = fIn[-1].split("si=")[1].split("\n")[2].split()[3]
        time = float(time)
        timeUnits = fIn[-1].split("si=")[1].split("\n")[2].split()[4]
        timeOut = False
    except:
        timeOut = True

    #take the enTable and split it up
    enTable = [enTable[ind].split() for ind in range(5,len(enTable)-3,2)]
    
    #Get the energies and stability parameters[1] is si, [4] is energy
    energies = [-float(enTable[ind][4]) for ind in range(len(enTable))]
    si = [float(enTable[ind][1]) for ind in range(len(enTable))]


    #If it didn't finish, get the last computed energy and beta2
    if timeOut:
        resTable["En"] = -energies[-1]
        resTable["beta2"]= float(enTable[-1][3])
    else:
        #If it didn't timeout, get the final energy and multipole moments
        info = fIn[-1].split("UNPROJECTED RESULTS")[-1].split("\n")
        
        #Look for the lines that contain the relevant information
        
        #Pull out the one off componenets
        # 3 is Force model used
        # 20 is rms
        # 22 beta2
        # 23 dipole
        # 24 quad
        # 27 q5
        # 52 En
        # 53 En+LN
        #Result table is a dictionary of the form {"ParamName": (float)[p/n/t]} or {"ParamName":"Value"}
        resTable["model"] = info[3].split()[-1]
        resTable["rms"] = [float(val) for val in info[20].split()[-3:]]
        resTable["beta2"] = [float(val) for val in info[22].split()[-3:]]
        resTable["En"] = float(info[52].split()[-1])
        resTable["En+LN"] = float(info[53].split()[-1])

        #Pull out the multipole momnets
        for ind in range(23, 31, 1):
            resTable["q{}".format(ind-22)] = [float(val) for val in info[ind].split()[-3:]]
        #End else statement
    
    #Save the dictionary
    outDict[fName] = resTable
    
#Save the file as a json file
outName = "summary.json" if len(sys.argv) == 1 else sys.argv[1]
with open(outName, 'w') as outJson:
    json.dump(outDict, outJson, indent=4)

        
