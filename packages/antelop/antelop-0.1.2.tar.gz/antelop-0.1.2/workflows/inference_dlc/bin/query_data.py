import argparse
import json
import os
import pathlib
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

# make sure only pull non-deleted keys
key["world_deleted"] = "False"

# perform all the following in a single transaction
with db.conn.transaction:
    # fetch trial keys
    query = db.World * db.DLCModel * db.Video.proj() - db.Kinematics.proj() & key
    worlds = query.proj().fetch(as_dict=True)

# write data to disk
with open("data.txt", "w") as f:
    for world in worlds:
        json.dump(world, f)
        f.write("\n")
