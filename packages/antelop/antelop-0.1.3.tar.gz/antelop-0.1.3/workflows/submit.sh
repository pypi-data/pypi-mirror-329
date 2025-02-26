#!/bin/bash

logdir=/cephfs/$USER/.antelop/logs
mkdir -p $logdir/$2
cd $logdir/$2

sbatch --export=$4 -t $5 --parsable /public/singularity/containers/antelop/workflows/$3/main.slurm $1
