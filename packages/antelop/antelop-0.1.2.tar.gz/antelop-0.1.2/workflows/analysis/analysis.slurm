#!/bin/bash

#SBATCH --job-name=antelope_analysis
#SBATCH --partition=cpu
#SBATCH --ntasks=1

analysis=/public/singularity/containers/antelop/workflows/analysis/
container=/public/singularity/containers/antelop/containers/antelop-python.sif
envstr="DB_USER=$DB_USER,DB_PASS=$DB_PASS,DB_HOST=$DB_HOST,S3_USER=$S3_USER,S3_PASS=$S3_PASS,S3_HOST=$S3_HOST"

apptainer exec --env $envstr -B $analysis:/scripts $container python /scripts/run_analysis.py --save "$1" --funclocation "$2" --funcfolder "$3" --funcname "$4" --restriction "$5" --args "$6" --numcpus "$7" 
