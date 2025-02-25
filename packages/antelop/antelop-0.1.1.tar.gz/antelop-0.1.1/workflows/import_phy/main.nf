#!/usr/bin/env nextflow
nextflow.enable.dsl = 2

params.key
params.phyDir

process DownloadData {

	input:
		val key

	output:
		tuple val(key), path('hashkey.txt'), path('recording'), path('equip.txt'), path('probe.json'), path('params.json')

	script:
	if (key != null)
		"""
		python '${workflow.projectDir}'/bin/download_data.py --key '$key'
		unzip -d recording recording/*.zip
		rm recording/*.zip
		"""

	else
		"""
		echo "No parameter specified"
		"""
}

process ConvertRec {

	input:
		tuple val(key), val(hash), path('recording'), path('equip.txt'), path('probe.json'), path('params.json')

	output:
		tuple val(key), val(hash), path('params.json'), path('split_recordings/*')

	script:
	"""
	python '${workflow.projectDir}'/bin/convert_rec.py
	"""

}

process PreProcess {

	input:
		tuple val(key), val(hash), path('params.json'), path('probe'), val(probenum)

	output:
		tuple val(key), val(hash), path('params.json'), val(probenum), path('preprocessed_*')

	script:
	"""
	export MPLCONFIGDIR='matplotlib_cache'
	python '${workflow.projectDir}'/bin/preprocess.py --probe '$probenum' --key '$key'
	"""

}

process ImportPhy {

	input:
		tuple val(key), val(hash), path(params), val(probenum), path(preprocessed)
		val(phyDir)

	output:
		tuple val(key), path(params), val(probenum), path(preprocessed), path('agreement_*')

	script:
	"""
	export MPLCONFIGDIR='matplotlib_cache'
	python '${workflow.projectDir}'/bin/import_phy.py --probe '$probenum' --phy '${phyDir}/${hash}'
	"""

}

process ExtractWaveforms {

	input:
		tuple val(key), val(probe_id), path(agreement), path(preprocessed), path(params)

	output:
		tuple val(key), val(probe_id), path('data_*')

	script:
	"""
	export NUMBA_CACHE_DIR='numba_cache'
	export MPLCONFIGDIR='matplotlib_cache'
	export FC_CACHE_DIR='fontconfig_cache'
	python '${workflow.projectDir}'/bin/extract_waveforms.py --sortkey '$key' --probeid '$probe_id'
	"""

}

process UploadData {

	input:
		tuple val(key), val(probe_ids), path(data)

	output:

	script:
	"""
	export MPLCONFIGDIR='matplotlib_cache'
	python '${workflow.projectDir}'/bin/send_db.py --sortkey '$key' --probe_ids '$probe_ids'
	"""

}

workflow {

	DownloadData(params.key)

	// read key
	ConvertRecChannel = DownloadData.out.map { tuple ->
		def key = tuple[0]
		def hash = tuple[1].getText()
		def recording = tuple[2]
		def equip = tuple[3]
		def probe = tuple[4]
		def params = tuple[5]

		[ key, hash, recording, equip, probe, params ]
	}

	ConvertRec(ConvertRecChannel)

	// split channel by probe
	SplitProbe = ConvertRec.out.flatMap { key, hash, params, recording ->
		recording.collect { probe ->
			probenum = probe.getName()
			tuple(key, hash, params, probe, probenum)
		}
	}

	PreProcess(SplitProbe)

	// rejoin probes
	ImportPhyChannel = PreProcess.out.groupTuple(by: 0).map { tuple ->
		def key = tuple[0]
		def hash = tuple[1][0]
		def params = tuple[2][0]
		def probes = tuple[3]
		def preprocessed = tuple[4]

		[ key, hash, params, probes, preprocessed]
	}

	ImportPhy(ImportPhyChannel, params.phyDir)

	ExtractChannel = ImportPhy.out.flatMap { key, params, probes, preprocessed, agreement ->
		probes.collect { probe ->
			tuple(key, probe, agreement, preprocessed, params)
		}
	}

	ExtractWaveforms(ExtractChannel)

	UploadChannel = ExtractWaveforms.out.groupTuple()

	UploadData(UploadChannel)

}
