"""
Script run on the hpc inside the antelope-python singularity container
Input parameters: primary key for the session we want to spike sort
Function: downloads the session raw data, spikesorting parameters,
equipment type, and probefile into working directory
"""

import json
from antelop.load_connection import *

# convert key to dict
with open("session.json", "r") as f:
    session = json.load(f)

# load params from session
params = list(session["paramslist"])
del session["paramslist"]

# fetch raw session data
query = Recording & session
sessions = query.fetch1(download_path="recording")

# fetch equip_type
query = Recording & session
equip_type = query.fetch1("ephys_acquisition")
with open("equip.txt", "w") as f:
    f.write(equip_type)

# fetch probe
query = ProbeGeometry * ProbeInsertion * Recording.proj() & session
probefile = query.fetch1("probe")
with open("probe.json", "w") as f:
    json.dump(probefile, f)

# fetch probe transformation
query = ProbeInsertion * Recording.proj() & session
probecoords = query.fetch1()
probecoords = {
    key: float(val)
    for key, val in probecoords.items()
    if key in ["yaw", "pitch", "roll", "ap_coord", "ml_coord", "dv_coord"]
}

# need to also sum over DV increment for all sessions
session_timestamp = (Session & session).fetch1("session_timestamp")
animal = {key: val for key, val in session.items() if key != "session_id"}
query = (
    Session * Recording & animal & f'session_timestamp <= "{str(session_timestamp)}"'
).proj("session_timestamp", "probe_dv_increment")  # all increments less than timestamp
total_dv = float(query.fetch("probe_dv_increment").sum()) + probecoords["dv_coord"]
probecoords["total_dv"] = float(total_dv)

# write params to file
with open("params.txt", "w") as f:
    for i in params:
        # fetch parameter
        param = (SortingParams & session & {"sortingparams_id": i}).fetch1()
        param["params"]["probecoords"] = probecoords
        paramdict = {"sortingparams_id": i, "params": param["params"]}
        json.dump(paramdict, f)
        f.write("\n")

# write session key to file
with open("session.json", "w") as f:
    json.dump(session, f)
