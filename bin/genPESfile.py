#!/usr/bin/env python3
# Python script to create the PES input file for HFBTHO v3.00
# Adam Anthony 4/12/2019

# Input: genPESFile.py NumConstraints Const1 Const2 ...
# Const1 has form \lambda,min,max,\delta

# Get the number of arguments and make sure it matches

import sys

def usage():
    print("""\
Usage: genPESfile.py beta2 Const1 Const2 ...

    beta2: The beta2 to impose on the calculation
    Const#: Constraint # in the form "lambda,min,max,delta"
""")


# Validate the input and get the number of constraints
constraints = []
try:
    beta2 = float(sys.argv[1])
    validInput = True
except:
    validInput = False

# If input is good so far validate the constraints
for c in sys.argv[2:]:
    # Make sure the constraint is formated properly
    try:
        const = [float(i) for i in c.split(",")]
        const[0] = int(c.split(",")[0])
        validInput &= len(const) == 4
    except:
        validInput = False
    
    # Check the formating and return if bad else append to list
    if validInput:
      constraints.append(const)

# If the input was not valid print usage
if not validInput:
    usage()
    exit(1)

# Everythin was good so format the file

# Get the number of points
nPoints = 1
for constraint in constraints:
    if constraint[3] != 0:
        constraint.append((constraint[2] - constraint[1])\
                          / constraint[3] + 1)
    else:
        constraint.append(1)
    nPoints *= constraint[4]

# Get the number of defs
nDefs = len(constraints)


# Print out the number of points and number of constraints
print("# nPts   nDefs")
print("%d   %d" %(nPoints, nDefs))

# Print out the lamdas to constrain
print("# lambda")
line = ""
for constraint in constraints:
    line += "{} ".format(constraint[0])
print(line)

# Format the header
header = "# Z  N"
for i in range(nDefs):
    header += "  q{}".format(constraints[i][0])
header += "  bet2  bet4"

# Print the header
print(header)


# Print out the data
# Loop through the points

for i in range(int(nPoints)):
    nUp = 0
    n = nPoints
    line = "82  114  "

    # Loop through the contraints
    for con in range(int(nDefs)):
        n = n/constraints[con][4]
        if con != 0:
            i -= nUp * int(i/nUp)
        offset = int(i/n)

        line += "{}  ".format(offset*constraints[con][3]+constraints[con][1])
        nUp = n

    # Add the bet2 and bet4 and mystery
    line += "{}  {}  {}".format(beta2, 0.01, 0.0)
    print(line)
