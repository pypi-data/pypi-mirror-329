# pylint: disable=redefined-outer-name

import os
from typing import Iterator

import h5py
import numpy as np
import pytest
from pytest import TempPathFactory


@pytest.fixture(scope="session")
def hdf5_mock_path(tmp_path_factory: TempPathFactory) -> Iterator[str]:
    """Mock HDF5 file."""
    path = os.path.join(tmp_path_factory.mktemp("files"), "test.h5")
    rng = np.random.default_rng()
    with h5py.File(path, driver="core", mode="w") as h5:
        for scan_id in range(1, 6):
            h5.create_dataset(f"{scan_id}.1/title", data=b"fscan")
            h5.create_dataset(f"{scan_id}.1/instrument/name", data="detector")
            for counter in ["x", "signal", "monitor"]:
                if scan_id not in (1, 2):
                    h5.create_dataset(
                        f"{scan_id}.1/measurement/{counter}", data=rng.random(10)
                    )
        h5.create_dataset("2.1/measurement/x", data=rng.random(15))
        h5.create_dataset("2.1/measurement/signal", data=rng.random(15))
        h5.create_dataset("5.1/measurement/sec", data=rng.random(10))
        h5.create_dataset("5.1/measurement/counter1", data=rng.random(10))
        h5.create_dataset("5.1/measurement/counter2", data=rng.random(10))
    yield path
    os.remove(path)
