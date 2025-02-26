#!/bin/bash

#SBATCH --job-name=inference_dlc_master
#SBATCH --partition=cpu
#SBATCH --cpus-per-task=1
#SBATCH --ntasks=1

# add alternatives to path
export PATH=/usr/sbin:$PATH

# JAVA
JAVA=$(alternatives --display java | awk '/family java-17/ { print $1}')
JAVA_HOME=${JAVA%%/bin/java}
export PATH=${JAVA%%/java}:$PATH

# Nextflow
export PATH=/public/singularity/containers/antelop/bin/nextflow:$PATH

# Nextflow cache
export NXF_HOME=/cephfs/$USER/.antelop/nfx_home

# print key to disk
echo "Key for this job: $1"

# run job
nextflow run /public/singularity/containers/antelop/workflows/inference_dlc/main.nf --key $1
