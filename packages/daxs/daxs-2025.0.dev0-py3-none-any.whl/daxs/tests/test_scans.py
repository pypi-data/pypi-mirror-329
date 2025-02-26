from __future__ import annotations

import copy
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pytest

from daxs.measurements import Measurement
from daxs.scans import Scan
from daxs.sources import Hdf5Source
from daxs.utils import resources


@pytest.fixture
def scan():
    x = np.array([3, 1, 2, 0, 4], dtype=float)
    signal = np.array([[2, 9, 0, 4, 1], [9, 1, 3, 4, 3]], dtype=float)
    data = {
        "monitor": np.array([1, 1, 2, 4, 2], dtype=float),
        "detection_time": [0.2, 0.2, 0.2, 0.2, 0.2],
        "filename": "No file name",
        "index": 1,
    }
    scan = Scan(x, signal, data=data)
    scan.reindex()
    return scan


def test_scan_init():
    rng = np.random.default_rng()
    x = rng.random(10)
    signal = "not an array"

    with pytest.raises(AssertionError):
        Scan(x, signal)  # type: ignore


def test_scan_reset(scan: Scan):
    scan.x = np.array([1, 1, 1, 1, 1])
    scan.reset()
    assert scan.x == pytest.approx([0, 1, 2, 3, 4])


def test_scan_properties(scan: Scan):
    assert scan.x == pytest.approx([0, 1, 2, 3, 4])
    assert scan.signal == pytest.approx([4.0, 5.0, 1.5, 5.5, 2.0])
    assert scan.monitor == pytest.approx([4, 1, 2, 1, 2])

    scan.x = np.array([3, 1, 2, 0, 4])
    assert scan.x == pytest.approx([0, 1, 2, 3, 4])
    assert scan.signal == pytest.approx([4.0, 5.0, 1.5, 5.5, 2.0])

    scan.reset()
    scan.x = np.array([5, 6, 7, 9, 11])
    assert scan.x == pytest.approx([5, 6, 7, 9, 11])
    assert scan.signal == pytest.approx([4.0, 5.0, 1.5, 5.5, 2.0])

    scan.reset()
    with pytest.raises(ValueError):
        scan.x = np.array([5, 6, 7, 9, 11, 12])

    scan.reset()
    scan.x = np.array([0, 1, 2, 3, 5, 10])
    assert scan.x == pytest.approx([0, 1, 2, 3, 5, 10])
    assert scan.signal == pytest.approx(
        [4.0, 5.0, 1.5, 5.5, np.nan, np.nan], nan_ok=True
    )


def test_scan_interpolate(scan: Scan):
    scan._signal = np.ndarray([])  # type: ignore
    with pytest.raises(ValueError):
        rng = np.random.default_rng()
        scan.interpolate(a=rng.random(10))


def test_scan_outliers_removal(scan: Scan):
    scan.remove_outliers(method="hampel")
    assert scan.signal == pytest.approx([4.0, 5.0, 1.5, 2.5, 2.0])


def test_scan_dead_time_correction(scan: Scan):
    with pytest.raises(TypeError):
        scan.dead_time_correction()  # type: ignore

    tau = np.array([1.0, 1.0, 1.0], dtype=np.float64) * 1e-3
    with pytest.raises(ValueError):
        scan.dead_time_correction(tau=tau)

    scan.reset()
    tau = np.array([1.0, 1.0]) * 1e-3
    scan.dead_time_correction(tau)
    assert scan.signal == pytest.approx(
        np.array([4.08163265, 5.21455445, 1.52284264, 5.72214289, 2.0253552])
    )

    scan.reset()
    scan.data.pop("detection_time", None)
    with pytest.raises(ValueError):
        scan.dead_time_correction(tau)

    with pytest.raises(ValueError):
        scan.dead_time_correction(tau=tau, detection_time=0.0)

    with pytest.raises(ValueError):
        scan.dead_time_correction(tau=[1.0, 1.0], detection_time=2)


def test_scan_plot(scan: Scan):
    _, ax = plt.subplots()
    scan.remove_outliers(method="hampel")
    scan.plot(ax)


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
def test_scan_divide_by_scan(scan: Scan):
    scan1 = copy.deepcopy(scan)
    scan2 = copy.deepcopy(scan)

    scan2.divide_by_scan(scan1)
    scan2._signal = scan2._signal / 2.0  # type: ignore
    assert scan2.signal[0:2] == pytest.approx([0.5, 0.5])


def test_str(scan: Scan):
    assert str(scan) == "None/None"


@pytest.fixture()
def hdf5_filename():
    return resources.getfile("Pd_foil_La_XANES.h5")


@pytest.fixture()
def data_mappings():
    return {
        "x": ".1/measurement/hdh_angle",
        "signal": [".1/measurement/g09", ".1/measurement/g14"],
    }


def test_scans_get_common_axis(hdf5_filename: str, data_mappings: dict[str, Any]):
    source = Hdf5Source(hdf5_filename, [3], data_mappings=data_mappings)
    measurement = Measurement(source)
    values = measurement.scans.get_common_axis("x")
    assert np.all(values == getattr(measurement.scans[0], "x"))

    source = Hdf5Source(hdf5_filename, [3, 4, 7, 8, 9], data_mappings=data_mappings)
    measurement = Measurement(source)

    values = measurement.scans.get_common_axis("x")
    assert values[-1] == pytest.approx(38.72936736)

    values = measurement.scans.get_common_axis("x", mode="union")
    assert values[-1] == pytest.approx(38.72939236)
