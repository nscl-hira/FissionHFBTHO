#!/usr/bin/env python3
# Program to make a plot of some Q vs anything
# in the summary.json

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import sys

SMALL_SIZE = 15
MEDIUM_SIZE = 20
LARGE_SIZE = 30

plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=SMALL_SIZE)
plt.rc('axes', labelsize=MEDIUM_SIZE)
plt.rc('xtick', labelsize=SMALL_SIZE)
plt.rc('ytick', labelsize=SMALL_SIZE)
#plt.rc('legend', fontsize=SMALL_SIZE)
plt.rc('figure', titlesize=LARGE_SIZE)





def usage():
    print("""\
Usage: printQ.py xAxis yAxis [yAxis2...yAxisN] [fileName]
    xAxis:    The value to use on the yAxis. can have the form val,sub where
              val is the key value and sub is the index of the list
    yAxis:    The value to use on the yAxis. can have the form val,sub where
              val is the key value and sub is the index of the list
    fileName: (default: summary.json) the name of the json file to load
              If there is more than one yAxis, must be present
""")


# Validate the input
try:
    # validate the number of parameters
    argc = len(sys.argv)
    if len(sys.argv) < 3:
        raise NameError("Invalid number of arguments: {}".
                        format(len(sys.argv)))
    
    # Get the number of yAxis and if filename was passed
    numY = 1 if argc == 3 else argc - 3
    fName = "summary.json" if argc == 3 else sys.argv[argc-1]
    
    
    # Validate the file name
    with open(fName, 'r') as fIn:
        # Load in the dictionary
        runs = json.load(fIn)

        # Generate the error string to use in validation
        error = """\
{} not a valid option. Valid options: 
"""
        # Loop through and get all valid keys
        key = list(runs.keys())[0]
        for op in runs[key].keys():
            addition = "{}".format(op)
            if type(runs[key][op]) == type([]):
                addition += ",n"
            error += addition
            error += "\n"

        # Validate the xAxis option
        xOpt = sys.argv[1]
        if "," in xOpt:
            xOpt = xOpt.split(",")
            xAxis = xOpt[0]
            xSub = int(xOpt[1])
            # Validate index
            if not xSub < len(runs[key][xAxis]):
                raise NameError(error.format(xAxis))

        else:
            xAxis = xOpt
            xSub  = -1
            # Validate index
            if type(runs[key][xAxis]) == type([]):
                raise NameError(error.format(xAxis))

        # Validate X Axis name
        if not xAxis in runs[key]:
            raise NameError(error.format(xAxis))

        # Validate the yAxis options
        yAxis = []
        ySub = []
        for yOpt in [ sys.argv[i] for i in range(2, 2 + numY) ]:
            if "," in yOpt:
                yOpt = yOpt.split(",")
                yAxis.append(yOpt[0])
                ySub.append(int(yOpt[1]))
                if not ySub[-1] < len(runs[key][yAxis[-1]]):
                    raise NameError(error.format(yAxis[-1]))

            else:
                yAxis.append(yOpt)
                ySub.append(-1)
                if type( runs[key][yAxis[-1]] ) == type( [] ):
                    raise NameError(error.format(yAxis[-1]))

            if not yAxis[-1] in runs[key]:
                raise NameError(error.format(yAxis[-1]))
            
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("%s at line %d" % (str(e), exc_tb.tb_lineno) )
    usage()
    exit(1)

#####################################################################
# The input has been validated and stored in xAxis, yAxis, pn, ySub #
# The data is stored in runs                                        #
#####################################################################

# Create the data structures to hold the information
xData = []
xDataSorted = []
yData = []
for i in range(numY):
    yData.append( [] )

# Load the data from each run
for run in runs:
    run = runs[run]

    # Get the xData
    if xSub < 0:
        xData.append(float(run[xAxis]))
    else:
        xData.append(float(run[xAxis][xSub]))

    # Loop through the yAxis and get the data
    for i in range(numY):
        if ySub[i] < 0:
            yData[i].append(float(run[yAxis[i]]))
        else:
            yData[i].append(float(run[yAxis[i]][ySub[i]]))

# Sort the data for each yAxis
for i in range(numY):
    xDataSorted, yData[i] = (list(x) for x in zip(*sorted(zip(xData, yData[i]))))


# Get interpolated data for each yAxis
xInterp = np.linspace(xDataSorted[0], xDataSorted[-1], 10*len(xData))


fig = plt.figure()
subPlot = []

title = ""
for i in range(numY):
    # Create a new sublot
    subPlot.append( fig.add_subplot(numY,1,i+1) )
    # Update the title
    title += "{}, ".format(yAxis[i])

    #Interpolate the yData and add both to the plot
    yInterp = interp1d(xDataSorted, yData[i], kind="cubic")
    subPlot[-1].plot(xDataSorted, yData[i], 'o', xInterp, yInterp(xInterp), "--")
    
    # Add a legend and label axis
    #subPlot[-1].legend(["data"], loc="best")
    subPlot[-1].set_ylabel(yAxis[i] + " (b^3/2)")

title = title[:-2] + " vs " + xAxis
#title = "HFBTHO Observables"

# Set the title and x axis label
fig.suptitle(title)
subPlot[-1].set_xlabel(xAxis + " (b)")

# Show the plot
plt.show()

