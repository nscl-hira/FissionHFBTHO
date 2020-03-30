#!/bin/bash --login

#SBATCH --ntasks=10
#SBATCH --time=16:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=1G
#SBATCH --job-name hfbtho-PES-196Pb

#Setting environment variables
export PAT_RT_HWPC=0
export OMP_NUM_THREADS=16
export KMP_STACKSIZE=32M
ulimit -s unlimited

# Customization of names and places
EXEC=${HFBTHODIR}"/hfbtho_main"
DATADIR="/mnt/home/kendzi23/FissionHFBTHO/setq3to5/Pb196-newpoints255to300"
OUT=$DATADIR"/Pb196Out-255to300.txt"

#Running the job
cd $DATADIR
pwd


module purge
module load intel
#module swap GNU Intel/16.3 
#module load MKL/11.1


date
srun -n 10  ${EXEC} &> ${OUT}
date

scontrol show job $SLURM_JOB_ID

