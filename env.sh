#!/bin/bash

# Load all of the required modules to run the code
module purge
module load intel
module load powertools

#Set the directories for HFBTHO
export HFBTHODIR="/mnt//home/antho121/HFBTHO/newBuild/hfbtho-master/src/hfbtho"

export PATH=`pwd`/bin:${PATH}
