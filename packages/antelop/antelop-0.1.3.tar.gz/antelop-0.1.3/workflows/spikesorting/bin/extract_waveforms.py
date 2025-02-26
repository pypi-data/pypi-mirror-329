import argparse
import json
import os
from pathlib import Path
import numpy as np
import pandas as pd
import spikeinterface as si
import decimal
from spikeinterface.postprocessing import (
    compute_spike_amplitudes,
    compute_principal_components,
    compute_unit_locations,
)
from spikeinterface.exporters import export_to_phy
import spikeinterface.preprocessing as spre
from scipy.spatial.transform import Rotation as R

# extract arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sortkey", type=str)
parser.add_argument("-p", "--probeid", type=str)
args = parser.parse_args()
sortkey = json.loads(args.sortkey)
probe = int(args.probeid)

# load paramaeters
with open("params.json") as f:
    params = json.load(f)

# set global job kwargs
num_cpus = int(os.environ["SLURM_CPUS_PER_TASK"]) - 1
mem = str(int((int(os.environ["SLURM_MEM_PER_NODE"]) / 1024) * 0.9)) + "G"
si.set_global_job_kwargs(n_jobs=num_cpus, total_memory=mem)

# use scratch space for sorting
scratch = os.environ["SLURM_SCRATCH_DIR"]

# first make subfolder
p = Path(f"data_{probe}")
p.mkdir()

# load recording objects
sorting = si.load_extractor(f"agreement_{probe}")
recording = si.load_extractor(f"preprocessed_{probe}")
raw = si.load_extractor(f"raw_{probe}")
sorting.register_recording(recording)

# annotations for later
sampling_frequency = recording.get_sampling_frequency()
ms_before = int(params["waveform"]["ms_before"])
ms_after = int(params["waveform"]["ms_after"])
lfp_sampling_frequency = int(params["lfp"]["sample_rate"])
probecoords = params["probecoords"]

# make rotation and translation arrays
angles = [
    float(probecoords["yaw"]),
    float(probecoords["pitch"]),
    float(probecoords["roll"]),
]
rotation = R.from_euler("zyx", angles, degrees=True)
rot_matrix = rotation.as_matrix()  # makes rotation matrix from euler angles
translation = np.array(
    [
        float(probecoords["ml_coord"]),
        float(probecoords["ap_coord"]),
        float(probecoords["total_dv"]),
    ]
)

# extract all waveforms
we = si.extract_waveforms(
    recording=recording,
    sorting=sorting,
    folder=f"{scratch}/waveforms_{str(probe)}",
    ms_before=params["waveform"]["ms_before"],
    ms_after=params["waveform"]["ms_after"],
    return_scaled=True,
    max_spikes_per_unit=None,
    sparse=False,
)

# make channel dataframe
# first we'll extract channel coordinates then transform them
coords = recording.get_probe().to_dataframe()[["x", "y", "z"]].to_numpy()
rot_coords = rot_matrix @ coords.T  # performs rotation about origin
trans_coords = rot_coords + translation[:, np.newaxis]  # performs translation
trans_coords = np.vectorize(decimal.Decimal.from_float, otypes="O")(trans_coords)
trans_coords = np.vectorize(lambda x: x.quantize(decimal.Decimal("1")), otypes="O")(
    trans_coords
)

# now add data to dataframe
channel_id = np.array(recording.get_channel_ids())
df = pd.DataFrame()
length = len(channel_id)
df["experimenter"] = np.full(length, fill_value=sortkey["experimenter"])
df["experiment_id"] = np.full(length, fill_value=sortkey["experiment_id"])
df["animal_id"] = np.full(length, fill_value=sortkey["animal_id"])
df["session_id"] = np.full(length, fill_value=sortkey["session_id"])
df["sortingparams_id"] = np.full(length, fill_value=sortkey["sortingparams_id"])
df["probe_id"] = np.full(length, fill_value=int(probe))
df["channel_id"] = channel_id
df["ap_coord"] = trans_coords[1]
df["ml_coord"] = trans_coords[0]
df["dv_coord"] = trans_coords[2]
df.to_pickle(f"data_{probe}/channel.pkl")
del df

# make unit dataframe
# first we'll estimate unit locations then transform them
coords = compute_unit_locations(we)
rot_coords = rot_matrix @ coords.T  # performs rotation about origin
trans_coords = rot_coords + translation[:, np.newaxis]  # performs translation
trans_coords = np.vectorize(decimal.Decimal.from_float, otypes="O")(trans_coords)
trans_coords = np.vectorize(lambda x: x.quantize(decimal.Decimal("1")), otypes="O")(
    trans_coords
)

# now add data to dataframe
unit_id = np.array(sorting.get_unit_ids())
df = pd.DataFrame()
length = len(unit_id)
df["experimenter"] = np.full(length, fill_value=sortkey["experimenter"])
df["experiment_id"] = np.full(length, fill_value=sortkey["experiment_id"])
df["animal_id"] = np.full(length, fill_value=sortkey["animal_id"])
df["session_id"] = np.full(length, fill_value=sortkey["session_id"])
df["sortingparams_id"] = np.full(length, fill_value=sortkey["sortingparams_id"])
df["probe_id"] = np.full(length, fill_value=int(probe))
df["unit_id"] = unit_id
df["ap_coord"] = trans_coords[1]
df["ml_coord"] = trans_coords[0]
df["dv_coord"] = trans_coords[2]
df.to_pickle(f"data_{probe}/unit.pkl")
del df

# extract LFPs
lfp = spre.bandpass_filter(raw, params["lfp"]["min_freq"], params["lfp"]["max_freq"])
lfp = spre.resample(lfp, lfp_sampling_frequency)
traces = lfp.get_traces(return_scaled=True)
del lfp
lfp_series = pd.Series(np.hsplit(traces, traces.shape[1]), name="lfp")
lfp_series = lfp_series.apply(np.squeeze)

# make lfp dataframe
df = pd.DataFrame()
length = len(channel_id)
df["experimenter"] = np.full(length, fill_value=sortkey["experimenter"])
df["experiment_id"] = np.full(length, fill_value=sortkey["experiment_id"])
df["animal_id"] = np.full(length, fill_value=sortkey["animal_id"])
df["session_id"] = np.full(length, fill_value=sortkey["session_id"])
df["sortingparams_id"] = np.full(length, fill_value=sortkey["sortingparams_id"])
df["probe_id"] = np.full(length, fill_value=int(probe))
df["channel_id"] = channel_id
df["lfp"] = lfp_series
df["lfp_sample_rate"] = np.full(length, fill_value=lfp_sampling_frequency)
df.to_pickle(f"data_{probe}/lfp.pkl")
del df

# extract spiketrains
sample_rate = recording.get_sampling_frequency()
spiketrains = []
for i in unit_id:
    spiketrains.append(sorting.get_unit_spike_train(unit_id=i) / sample_rate)
spiketrain_series = pd.Series(spiketrains, name="spiketrain")

# make spiketrain dataframe
df = pd.DataFrame()
length = len(unit_id)
df["experimenter"] = np.full(length, fill_value=sortkey["experimenter"])
df["experiment_id"] = np.full(length, fill_value=sortkey["experiment_id"])
df["animal_id"] = np.full(length, fill_value=sortkey["animal_id"])
df["session_id"] = np.full(length, fill_value=sortkey["session_id"])
df["sortingparams_id"] = np.full(length, fill_value=sortkey["sortingparams_id"])
df["probe_id"] = np.full(length, fill_value=int(probe))
df["unit_id"] = unit_id
df["spiketrain"] = spiketrain_series
df.to_pickle(f"data_{probe}/spiketrain.pkl")
del df

# make subfolder
p = Path(f"data_{probe}/waveforms")
p.mkdir()

# loop through units to make individual dataframes
for unit in unit_id:
    # get array from waveforms
    waveforms = we.get_waveforms(unit)

    # split array down channel axis
    wave_series = pd.Series(
        np.split(waveforms, waveforms.shape[2], axis=2), name="waveform"
    )
    del waveforms
    wave_series = wave_series.apply(np.squeeze)

    # make lfp dataframe
    df = pd.DataFrame()
    length = len(channel_id)
    df["experimenter"] = np.full(length, fill_value=sortkey["experimenter"])
    df["experiment_id"] = np.full(length, fill_value=sortkey["experiment_id"])
    df["animal_id"] = np.full(length, fill_value=sortkey["animal_id"])
    df["session_id"] = np.full(length, fill_value=sortkey["session_id"])
    df["sortingparams_id"] = np.full(length, fill_value=sortkey["sortingparams_id"])
    df["probe_id"] = np.full(length, fill_value=int(probe))
    df["unit_id"] = np.full(length, fill_value=int(unit))
    df["channel_id"] = channel_id
    df["waveform"] = wave_series
    df["waveform_sample_rate"] = np.full(length, sampling_frequency)
    df["ms_before"] = np.full(length, fill_value=ms_before)
    df["ms_after"] = np.full(length, fill_value=ms_after)
    df.to_pickle(f"data_{probe}/waveforms/{str(unit)}.pkl")
    del df
