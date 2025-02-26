#!/bin/bash

logdir=/cephfs/$USER/.antelop/logs
mkdir -p $logdir/$1
cd $logdir/$1

sbatch --export=$2 -t $3 -c $4 --parsable /public/singularity/containers/antelop/workflows/analysis/analysis.slurm "$5" "$6" "$7" "$8" "$9" "${10}" "$4"
