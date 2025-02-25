import argparse
import yaml
import json
import os
import zipfile
from pathlib import Path
import sys
import datajoint as dj

sys.path.append("/app")

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--key")
args = parser.parse_args()

# convert key to dict
key = json.loads(args.key)

# run start script to form database connection
import antelope.scripts.start_workflows as db

# check that the key is correct
if "behaviourrig_deleted" in key.keys():
    del key["behaviourrig_deleted"]
assert set(list(key.keys())) == set(
    ["experimenter", "experiment_id", "behaviourrig_id", "dlcmodel_id"]
)
p = Path("dlc")
p.mkdir()
(p / "dlc-models").mkdir()
(p / "labeled-data").mkdir()
(p / "training-datasets").mkdir()
(p / "videos").mkdir()

# download data
with db.conn.transaction:
    data = (db.LabelledFrames & key).fetch1()
    db.LabelledFrames.update1({**key, "labelledframes_in_compute": "True"})

# write config to file
config = data["dlcparams"]["config"]
config["project_path"] = str(p.resolve())
with open(p / "config.yaml", "w") as f:
    yaml.dump(config, f)

compute = data["dlcparams"]["compute"]
with open(p / "compute.json", "w") as f:
    json.dump(compute, f)

# unzip data
videos = data["labelled_frames"]
with zipfile.ZipFile(videos, "r") as zip_ref:
    zip_ref.extractall(p / "labeled-data")
