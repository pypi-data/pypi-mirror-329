-- Create the Experimenter table
CREATE TABLE Experimenter (
    experimenter varchar(40) PRIMARY KEY,
    full_name varchar(40),
    group varchar(40),
    institution varchar(40)
);

-- Create the Probes table
CREATE TABLE Probes (
    probe_id smallint PRIMARY KEY,
    probe json,
    probe_description varchar(1000)
);

-- Create the Experiment table
CREATE TABLE Experiment (
    experimenter varchar(40) REFERENCES Experimenter(experimenter),
    experiment_id smallint PRIMARY KEY,
    experiment_description varchar(1000),
    equip_type enum('axona','openephys')
);

-- Create the SortingParams table
CREATE TABLE SortingParams (
    experiment_id smallint REFERENCES Experiment(experiment_id),
    params_id smallint PRIMARY KEY,
    sortingparams_description varchar(1000),
    params json
);

-- Create the Animal table
CREATE TABLE Animal (
    experiment_id smallint REFERENCES Experiment(experiment_id),
    animal_id varchar(15) PRIMARY KEY,
    animal_description varchar(1000),
    probe_id smallint REFERENCES Probes(probe_id)
);

-- Create the Trial table
CREATE TABLE Trial (
    animal_id varchar(15) REFERENCES Animal(animal_id),
    trial_id int PRIMARY KEY,
    trial_description varchar(1000),
    raw blob -- You should specify the proper data type for raw data
);

-- Create the SpikeSorting table
CREATE TABLE SpikeSorting (
    trial_id int REFERENCES Trial(trial_id),
    PRIMARY KEY (trial_id)
);

-- Create the ManualCuration table
CREATE TABLE ManualCuration (
    trial_id int REFERENCES Trial(trial_id),
    results_id int REFERENCES SpikeSorting(trial_id),
    manual_curation json,
    PRIMARY KEY (trial_id, results_id)
);

-- Create the Ephys table
CREATE TABLE Ephys (
    trial_id int REFERENCES Trial(trial_id),
    PRIMARY KEY (trial_id)
);

-- Create the Ephys Probe table
CREATE TABLE Ephys_Probe (
    trial_id int REFERENCES Trial(trial_id),
    probe_id int,
    PRIMARY KEY (trial_id, probe_id)
);

-- Create the Ephys Channel table
CREATE TABLE Ephys_Channel (
    trial_id int,
    probe_id int,
    channel_id int,
    coordinates tinyblob,
    PRIMARY KEY (trial_id, probe_id, channel_id)
);

-- Create the Ephys LFP table
CREATE TABLE Ephys_LFP (
    trial_id int,
    probe_id int,
    channel_id int,
    waveform blob,
    sample_rate int,
    PRIMARY KEY (trial_id, probe_id, channel_id)
);

-- Create the Ephys Unit table
CREATE TABLE Ephys_Unit (
    trial_id int,
    probe_id int,
    unit int,
    PRIMARY KEY (trial_id, probe_id, unit)
);

-- Create the Ephys Spike table
CREATE TABLE Ephys_Spike (
    trial_id int,
    probe_id int,
    unit int,
    spike_nb int,
    timestamp float,
    PRIMARY KEY (trial_id, probe_id, unit, spike_nb)
);

-- Create the Ephys Waveform table
CREATE TABLE Ephys_Waveform (
    trial_id int,
    probe_id int,
    unit int,
    channel_id int,
    waveform blob,
    PRIMARY KEY (trial_id, probe_id, unit, channel_id)
);
