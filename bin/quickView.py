#!/usr/bin/env python3
# Quick and dirty script to pull out the important information from 
# the output files of HFBTHO
# As an input it takes the number of files to process
# Adam Anthony 4/3/2019


import matplotlib.pyplot as plt
import sys

if len(sys.argv)< 2:
    print("""\
Usage: quixkView.py num flag
     num\tnumber of output files to process
     flag\tIf there don't show graphs\
""")
    exit(1)

for i in range(1,int(sys.argv[1])+1,1):
    with open ("thoout_{0:0>6}.dat".format(i)) as file:
        # Split file and get the table of values
        fIn = file.read().split("REGULAR STAGE")
    
    #Get the table of itertions
    enTable = fIn[-1].split("si=")[0].split("\n")
    
    #Figure out if this converged
    conv = "converged" in enTable[-1]

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

    #Dictionary of observables
    resTable = {}

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
        
    for key in resTable:
        print("{}: {}".format(key, resTable[key]))
        

    
    #Print the number of iterations and if it timed out
    if not timeOut:
        print("%d %s in %d iterations in %.2f %s" % (i, "converged" if conv else "did not converge",len(enTable), time, timeUnits) )
    else:
        print( "%d timed out after %d iterations" % (i, len(enTable)) )

        
    minVal = 50 if len(energies) > 50 else int(len(energies)/2)
    #Create Diff(E) subplot
    if len(sys.argv) != 2:
        continue

    plt.subplot(2,2,1)
    plt.title("Convergence properties")
    plt.plot([abs(energies[-1] - e) for e in energies ])
    plt.axis([0,len(energies),10**-7,10**4])
    plt.yscale("log")
    plt.ylabel(r"$log(|E_f - E_n|)$")
    
    plt.subplot(2,2,2)
    plt.title("Last {0:d}".format(minVal))
    plt.plot([energies[-minVal] -e for e in energies[-minVal:] ])
    plt.ylabel("-{0:.5f} Energy (MeV)".format(energies[-minVal]))
    plt.ticklabel_format(axis='y', style='sci', scilimits=(-5,-4))
        
    #Create stablity subplot
    plt.subplot(2,2,3)
    plt.plot(si)
    plt.axis([0,len(si),10**-5,10**2])
    plt.yscale("log")
    plt.ylabel(r"$log(Si)$")
    plt.xlabel("Iteration number")
    
    plt.subplot(2,2,4)
    plt.plot(si[-minVal:])
    #plt.axis([0,50,10**-5,10**-3])
    plt.yscale("log")
    plt.ylabel(r"$log(Si)$")
    plt.xlabel("Iteration number")
    
    
    #Show the plots
    plt.show()
        
