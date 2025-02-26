import argparse
import yaml
import json
import os
import zipfile
from pathlib import Path
import sys
import csv
import shutil
import datajoint as dj

sys.path.append("/app")

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--key")
parser.add_argument("-d", "--data")
args = parser.parse_args()

key = json.loads(args.key)
p = Path(args.data)

# run start script to form database connection
import antelope.scripts.start_workflows as db

# load eval results
results = p / "evaluation-results" / "iteration-0" / "CombinedEvaluation-results.csv"
with open(results, "r") as f:
    for line in csv.DictReader(f):
        eval_dict = line
        break
if "" in eval_dict.keys():
    del eval_dict[""]

# zip metrics
images = list(p.glob("evaluation-results/iteration-0/*/*"))
for i in images:
    if i.is_dir():
        image_folder = i
eval_name = "evaluation_images"
for v in key.values():
    eval_name += f"_{v}"
shutil.make_archive(eval_name, "zip", image_folder)

# zip model
model_name = "model"
for v in key.values():
    model_name += f"_{v}"
shutil.make_archive(model_name, "zip", p / "dlc-models")

# upload data
if "behaviourrig_deleted" in key.keys():
    del key["behaviourrig_deleted"]
data = key.copy()
data["dlcmodel"] = Path(f"{model_name}.zip").resolve()
data["evaluated_frames"] = Path(f"{eval_name}.zip").resolve()
data["evaluation_metrics"] = eval_dict
data["dlcmodel_deleted"] = "False"
key["labelledframes_in_compute"] = "False"
with db.conn.transaction:
    db.DLCModel.insert1(data, allow_direct_insert=True)
    db.LabelledFrames.update1(key)
