import os
import shutil
import sys

import numpy as np
import h5py
import hdf5plugin


def h5sum(output_h5, input_h5s):

    shuffle = hdf5plugin.Bitshuffle

    inputs = [h5py.File(f, "r") for f in input_h5s]

    shapes = list(set(i["data"].shape for i in inputs))

    assert len(shapes) == 1

    nn = len(inputs)

    print(f"Merging {nn} sets of shape {shapes[0]}")

    with h5py.File(output_h5, "x") as fout:
        frames, slow, fast = shapes[0]

        dset = fout.create_dataset(
            "data",
            (frames, slow, fast),
            chunks=(1, slow, fast),
            dtype=np.int32,
            **shuffle(nelems=0, lz4=True),
        )

        for j in range(frames):
            image = inputs[0]["data"][j, :, :].astype(np.int32)
            for k in range(1, nn):
                image += inputs[k]["data"][j, :, :].astype(np.int32)
            dset[j, :, :] = image

        for k in "image_nr_low", "image_nr_high":
            dset.attrs.create(k, inputs[0]["data"].attrs.get(k), dtype="i4")


if __name__ == "__main__":
    assert not os.path.exists(sys.argv[1])
    for arg in sys.argv[2:]:
        assert os.path.exists(arg)
    h5sum(sys.argv[1], sys.argv[2:])
