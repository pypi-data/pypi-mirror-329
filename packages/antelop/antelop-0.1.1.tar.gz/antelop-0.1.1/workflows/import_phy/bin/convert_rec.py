"""
Script to run on the hpc in the spikeinterface container
Reads in rawdata and the probe file, and splits into probegroups and writes
them to probes folder
"""

import spikeinterface as si
import spikeinterface.extractors as se
import probeinterface as pi
import glob
import os

# set global job kwargs
num_cpus = int(os.environ["SLURM_CPUS_PER_TASK"]) - 1
mem = str(int((int(os.environ["SLURM_MEM_PER_NODE"]) / 1024) * 0.9)) + "G"
si.set_global_job_kwargs(n_jobs=num_cpus, total_memory=mem)

# read equip_type
with open("equip.txt") as f:
    equip_type = f.read()

# extract read function
read_func = getattr(se, f"read_{equip_type}")

# define dictionary of extensions to look for
# this should be updated as you add filetypes - maybe read in an external conf file
extdict = {"axona": ".bin"}

# check unzipped data folder for file with correct extension
path = f"""recording/*{extdict[equip_type]}"""
datafile = glob.glob(path)
assert len(datafile) == 1, f"""More than one {extdict[equip_type]} in folder"""

# read data
recording = read_func(datafile[0])

# read probe
probe = pi.read_probeinterface("probe.json")
recording = recording.set_probegroup(probe, group_mode="by_probe")

# split recordings into groups
recs = recording.split_by(property="group")

# write recordings to file
for key, val in recs.items():
    val.save(folder=f"split_recordings/{key}")
