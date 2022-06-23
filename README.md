# eiger-tools
Eiger related tooling - summing images etc. (public script repo)

## HDF5 Summing

Code to simulate the effect of collecting e.g. multi-lattice / wide bandwidth data by simply pixel-wise summing of data sets. Script is `hdf5sum.py` - run as

```
python hdf5sum.py out.h5 in1.h5 in2.h5
```

N.B. this _only_ sums the `data` dataset and uses / assumes `bslz4 compression`.