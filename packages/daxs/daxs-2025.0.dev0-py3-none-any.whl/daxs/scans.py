"""The module provides classes for the representation of scans in measurements."""

from __future__ import annotations

import copy
import logging
from typing import TYPE_CHECKING, Any, Iterable

if TYPE_CHECKING:
    import matplotlib.axes
import numpy as np
import numpy.typing as npt

from daxs.config import Config
from daxs.filters import hampel
from daxs.utils import arrays

logger = logging.getLogger(__name__)

use_dynamic_hdf5 = Config().get("use_dynamic_hdf5", False)
if use_dynamic_hdf5:
    from blissdata.h5api.dynamic_hdf5 import File
else:
    from silx.io.h5py_utils import File


class Scan:
    def __init__(
        self,
        x: npt.NDArray[np.float64] | None = None,
        signal: npt.NDArray[np.float64] | None = None,
        *,
        data: dict[Any, Any] | None = None,
    ) -> None:
        """
        Define the base representation of scans in measurements.

        Parameters
        ----------
        x :
            X-axis values (1D array).
        signal :
            Signal values (1D or 2D array). For a 2D array, the components must be
            stored as rows. A 1D array will be converted to a 2D array.
        data :
            Storage for the raw scan data and metadata.

        """
        self.data = {} if data is None else data

        # Initialize the x, y, signal, and monitor values.
        if x is not None:
            assert isinstance(x, np.ndarray), "The X-axis must be a Numpy array."
            x = np.asarray(x)
            self._x = x
            self.data["x"] = copy.deepcopy(x)
        else:
            self._x = np.array([])
        self._y = np.array([])
        if signal is not None:
            assert isinstance(signal, np.ndarray), "The signal must be a Numpy array."
            signal = np.asarray(signal)
            self._signal = signal
            self.data["signal"] = copy.deepcopy(signal)
        else:
            self._signal = np.array([])
        self._monitor = np.array([])

        # Array of indices used to reindex the data.
        self._indices: npt.NDArray[np.int32] = np.array([])

        # Initialize the outliers and medians arrays.
        self.outliers: npt.NDArray[np.bool_] = np.array([])
        self.medians: npt.NDArray[np.float64] = np.array([])

        self.filename: str | None = None
        self.index: int | None = None

        self.aggregation: str = "mean"

    @property
    def x(self):
        if self._x.size == 0:
            try:
                self._x = copy.deepcopy(self.data["x"])
            except KeyError as e:
                raise KeyError(
                    "The data dictionary does not contain X-axis values."
                ) from e
            if self._x.size == 0:
                raise ValueError("The X-axis values are empty.")
        return self._x

    @x.setter
    def x(self, a: npt.NDArray[np.float64]) -> None:
        """Set the X-axis values.

        Several cases are considered:

        1. The new values are the same as the current ones. In this case, nothing has
           to be done.
        2. The limits of the new values are within the current values. In this case, the
           signal and monitor data are interpolated to the new X-axis values.
        3. The new values are outside the current values, but the two arrays have the
           same shape. In this case, the new values are assigned to the X-axis. It
           is useful when the X-axis changes to different units, e.g., angle to energy.
        4. The new values are outside the current values and of different shapes. In
           this case, an error is raised.
        """
        a = np.sort(a, kind="stable")

        if np.array_equal(self._x, a):
            logger.debug("The new X-axis values are the same as the current ones.")
            return
        elif arrays.intersect(a, self._x).size > 0:
            self.interpolate(a)
            return
        elif self._x.size == a.size:
            logger.debug("Assigning the new X-axis values.")
            self._x = np.copy(a)
            self._indices = np.array([])
            return
        else:
            raise ValueError("The new X-axis values are outside the current ones.")

    @property
    def y(self):
        if self._y.size == 0:
            try:
                self._y = copy.deepcopy(self.data["y"])
            except KeyError as e:
                raise KeyError(
                    "The data dictionary does not contain Y-axis values."
                ) from e
        return self._y

    @property
    def signal(self):
        if self._signal.size == 0:
            try:
                self._signal = copy.deepcopy(self.data["signal"])
            except KeyError as e:
                raise KeyError(
                    "The data dictionary does not contain signal values."
                ) from e
        if self._signal.size == 0:
            raise ValueError("The signal values are empty.")
        if self._signal.ndim not in (1, 2):
            raise ValueError("The signal must be a 1D or a 2D array.")
        if self._signal.ndim == 1:
            self._signal = self._signal[np.newaxis, :]
        if self.aggregation == "mean":
            return self._signal.mean(axis=0)
        else:
            raise ValueError(f"Unknown aggregation method: {self.aggregation}.")

    @property
    def monitor(self):
        if self._monitor.size == 0:
            try:
                self._monitor = copy.deepcopy(self.data["monitor"])
            except KeyError:
                logger.debug("The data dictionary does not contain monitor values.")
            if self._monitor.size == 0:
                logger.debug("The monitor values are empty.")
        return self._monitor

    @property
    def indices(self):
        return self._indices

    @indices.setter
    def indices(self, a: npt.NDArray[np.int32]) -> None:
        if a.shape != self._x.shape:
            raise ValueError("The indices and X-axis arrays must have the same shape.")
        self._indices = a
        self.reset()

    @property
    def label(self) -> str:
        return f"{self.filename}/{self.index}"

    def read_data_at_path(self, data_paths: str | list[str]) -> npt.NDArray[np.float64]:
        """Read and store the data from the file."""
        if self.filename is None:
            raise ValueError("The filename from where to read the data must be set.")
        if self.index is None:
            raise ValueError("The scan index from where to read the data must be set.")

        data_paths = [data_paths] if isinstance(data_paths, str) else data_paths

        # Set the retry timeout for dynamic HDF5 if enabled.
        kwargs = {}
        if use_dynamic_hdf5:
            kwargs["retry_timeout"] = Config().get("dynamic_hdf5_retry_timeout")

        data: list[Any] = []
        with File(self.filename, **kwargs) as fh:
            for data_path in data_paths:
                full_data_path = f"{self.index}{data_path}"

                try:
                    data_at_path = fh[full_data_path][()]  # type: ignore
                except KeyError as e:
                    raise KeyError(f"Unable to access {full_data_path}.") from e
                except TypeError as e:
                    raise TypeError(
                        f"Unable to read data from {full_data_path}."
                    ) from e

                try:
                    data_at_path = np.asarray(data_at_path)
                except ValueError as e:
                    raise ValueError(
                        f"Unable to convert data from {full_data_path} "
                        "to a Numpy array."
                    ) from e
                if data_at_path.size == 0:
                    raise ValueError(f"Data from {full_data_path} is empty.")

                data.append(data_at_path)

        # Return the element of the array if it has only one element.
        if len(data) == 1:
            [data] = data

        return np.array(data)

    def reset(self) -> None:
        """Reset the scan data to the values read from file."""
        self._x = np.array([])
        self._signal = np.array([])

        self._y = np.array([])
        self._monitor = np.array([])
        self._indices = np.array([])
        self.outliers, self.medians = np.array([]), np.array([])
        self.reindex()

    def reindex(self):
        """Reindex the scan data."""
        if self.x.size == 0 or self.signal.size == 0:
            raise ValueError("The X-axis and signal values must be set.")
        if self._indices.size == 0:
            self._indices = np.argsort(self._x, kind="stable")
        self._x = self._x[self._indices]
        self._signal = self._signal[:, self._indices]
        if self.monitor.size != 0:
            self._monitor = self._monitor[self._indices]

    def find_outliers(self, method: str = "hampel", **kwargs: Any):
        """
        Find outliers in the signal.

        See the docstring in the :mod:`daxs.filters`.
        """
        if method == "hampel":
            self.outliers, self.medians = hampel(self._signal, axis=1, **kwargs)
        else:
            raise ValueError(f"Unknown method: {method}.")

    def remove_outliers(self, method: str = "hampel", **kwargs: Any):
        """
        Remove outliers from the signal.

        See the docstring of :meth:`daxs.scans.Scan.find_outliers`.
        """
        if self.outliers.size == 0 or self.medians.size == 0:
            self.find_outliers(method=method, **kwargs)

        if self.outliers.size > 0 and self.medians.size > 0:
            self._signal = np.where(self.outliers, self.medians, self._signal)
        else:
            logger.info("No outliers found for scan %s.", self.label)

    def plot(self, ax: matplotlib.axes.Axes, shift: float = 0.0):
        """
        Plot the scan data and outliers if available.

        Parameters
        ----------
        ax :
            The axes to plot the scan data on.
        shift :
            Shift the signal by the given value.

        """
        shift = float(np.mean(self._signal))
        for i, _ in enumerate(self._signal):
            ax.plot(self.x, self._signal[i, :] + i * shift, label=f"{i}")
            if self.outliers.size > 0:
                indices = self.outliers[i, :]
                ax.plot(self.x[indices], self._signal[i, :][indices] + i * shift, "k.")
            ax.legend()

    def dead_time_correction(
        self,
        tau: Iterable[float],
        detection_time: float | npt.NDArray[np.float64] | None = None,
    ):
        """
        Perform a dead time correction using a non-paralyzable model.

        Parameters
        ----------
        tau :
            The detector dead time in seconds.
        detection_time :
            The time spent on a point of the scan in seconds.

        """
        if detection_time is None:
            try:
                detection_time = copy.deepcopy(self.data["detection_time"])
            except KeyError:
                raise ValueError(
                    "Either the detection time parameter or `detection_time`"
                    " data path must be set."
                )
        else:
            detection_time = np.ones_like(self.signal) * detection_time

        detection_time = np.asarray(detection_time)

        if np.any(detection_time == 0):
            raise ValueError("The detection time has zero values.")

        tau = np.array(tau)
        if self._signal.shape[0] != tau.shape[0]:
            raise ValueError(
                "Each signal data path must have a detector dead time (tau) value."
            )

        norm = 1 - ((self._signal / detection_time).T * tau).T
        if np.any(norm == 0):
            raise ValueError("The normalization has zero values.")

        self._signal = self._signal / norm

    # TODO: Extract the interpolation logic to a separate class.
    def interpolate(self, a: npt.NDArray[np.float64]):
        """
        Interpolate the signal and possibly the monitor data to the new X-axis values.

        Parameters
        ----------
        a :
            Array used to interpolate the signal and monitor.

        """
        if a.size == 0:
            raise ValueError("The new X-axis values must not be empty.")
        if self.signal.size == 0:
            raise ValueError("The signal values must not be empty.")

        logger.debug(
            "Interpolating the signal and monitor data for scan %s.", self.label
        )

        # The interpolated signal is probably going to have a different size,
        # so we can't change the values in-place, and a new array needs to be
        # initialized.
        signal = np.zeros((self._signal.shape[0], a.size))

        # Interpolate the signal from each counter individually.
        for i, _ in enumerate(self._signal):
            signal[i, :] = np.interp(
                a, self._x, self._signal[i, :], left=np.nan, right=np.nan
            )

        # Interpolate the monitor if present.
        if self._monitor.size > 0:
            self._monitor = np.interp(
                a, self._x, self._monitor, left=np.nan, right=np.nan
            )

        self._x = a
        self._signal = signal
        self._indices = np.array([])

    def divide_by_scalars(self, signal: float, monitor: float | None = None) -> Scan:
        """Divide the scan by scalar values."""
        self._signal /= signal
        if monitor is not None:
            self._monitor /= monitor
        return self

    def divide_by_scan(self, other: Scan | None) -> Scan:
        return self.__truediv__(other)

    def __truediv__(self, other: Scan | None) -> Scan:
        """Divide the scan by another scan."""
        if not isinstance(other, Scan):
            raise TypeError("The divisor must be a scan.")
        try:
            self._signal /= np.nan_to_num(other._signal, nan=1)
        except ValueError as e:
            raise ValueError(
                "The signal arrays of the two scans must have the same shape."
            ) from e
        if self._monitor.size > 0 and other._monitor.size > 0:
            try:
                self._monitor /= np.nan_to_num(other._monitor, nan=1)
            except ValueError as e:
                raise ValueError(
                    "The monitor arrays of the two scans must have the same shape."
                ) from e
        return self

    def __str__(self):
        return self.label


class Scans:
    """A collection of scans."""

    def __init__(self, scans: Scan | list[Scan] | None = None) -> None:
        """Initialize the collection of scans."""
        if scans is None:
            self.scans = []
        elif isinstance(scans, list):
            self.scans = scans
        else:
            self.scans = [scans]

    def check_sizes(self) -> None:
        """Sanity check for the number of points in the scans."""
        sizes = [scan.x.size for scan in self.scans]
        mean = np.mean(sizes)
        std = np.std(sizes)

        if any(abs(size - mean) > std for size in sizes):
            logger.warning(
                "The number of points in the selected scans have a "
                "large spread (mean = %.2f, standard deviation: %.2f).",
                mean,
                std,
            )

    def get_common_axis(
        self, label: str = "x", mode: str = "intersection"
    ) -> npt.NDArray[np.float64]:
        """Return the common axis for the scans."""
        if not self.scans:
            raise ValueError("There are no scans available.")

        def step(axis: npt.NDArray[np.float64]) -> float:
            return np.abs((axis[0] - axis[-1]) / (axis.size - 1))

        # If there is a single scan, use its axis as the common axis.
        if len(self.scans) == 1:
            [axis] = self.scans
            return getattr(axis, label)

        axes = sorted([getattr(scan, label) for scan in self.scans], key=np.min)

        # Initialize the common axis as the first axis.
        common_axis = axes[0]
        for i, axis in enumerate(axes):
            message = (
                f"{label.upper()}-axis parameters for scan {self.scans[i].label}: "
                f"start = {axis[0]:.8f}, stop = {axis[-1]:.8f}, "
                f"size = {axis.size:d}, step = {step(axis):.8f}."
            )
            logger.debug(message)

            if np.array_equal(common_axis, axis):
                continue

            common_axis = arrays.merge(common_axis, axis, mode=mode)

            if common_axis.size == 0 and mode == "intersection":
                message = (
                    f"The common {label.upper()}-axis is empty after merging scan "
                    f"{self.scans[i].label}. "
                    "Switching to union mode for the common axis search."
                )
                logger.warning(message)
                return self.get_common_axis(label, mode="union")

        message = (
            f"Common {label.upper()}-axis parameters using {mode} mode: "
            f"start = {common_axis[0]:.8f}, stop = {common_axis[-1]:.8f}, "
            f"size = {common_axis.size:d}, step = {step(common_axis):.8f}"
        )
        logger.info(message)

        return common_axis

    def reset(self) -> None:
        """Reset the scans to their original values."""
        for scan in self.scans:
            scan.reset()

    def extend(self, scans: Scans) -> None:
        """Extend the collection of scans."""
        self.scans.extend(scans)

    def __len__(self) -> int:
        """Return the number of scans in the collection."""
        return len(self.scans)

    def __iter__(self):
        """Iterate over the scans."""
        return iter(self.scans)

    def __getitem__(self, index: int) -> Scan:
        """Return the scan at the given index."""
        return self.scans[index]

    def remove(self, item: Scan) -> None:
        """Remove the scan at the given index."""
        self.scans.remove(item)

    def append(self, item: Scan) -> None:
        """Append a scan to the collection."""
        self.scans.append(item)
