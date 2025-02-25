import probeinterface as pi
from probeinterface import ProbeGroup
from collections import namedtuple

# neuropixels 1.0
specs = namedtuple("specs", ["num_contacts", "xpitch", "ypitch"])
np1 = {
    "short": specs(960, 32, 20),
    "medium": specs(2496, 103, 20),
    "long": specs(4416, 103, 20),
}
for k, v in np1.items():
    probegroup = ProbeGroup()
    probe = pi.generate_multi_columns_probe(
        num_columns=2,
        num_contact_per_column=v.num_contacts // 2,
        xpitch=v.xpitch,
        ypitch=v.ypitch,
        contact_shapes="square",
        contact_shape_params={"width": 12},
    )
    device_channel_indices = list(range(v.num_contacts))
    probe.set_device_channel_indices(device_channel_indices)
    probegroup.add_probe(probe.to_3d(axes="xz"))
    pi.io.write_probeinterface(
        f"../resources/probes/neuropixels1.0_{k}.json", probegroup
    )

# tetrodes
n_tetrodes = [1, 2, 4, 8, 16]
for n in n_tetrodes:
    probegroup = ProbeGroup()
    for i in range(n):
        probe = pi.generate_tetrode()
        probe.move([i * 50, 0])
        device_channel_indices = list(range(i * 4, i * 4 + 4))
        probe.set_device_channel_indices(device_channel_indices)
        probegroup.add_probe(probe.to_3d(axes="xz"))
    pi.io.write_probeinterface(f"../resources/probes/tetrode_{n}.json", probegroup)
