"""The module provides classes to deal with different types of data sources."""

from __future__ import annotations

import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Iterator

import numpy as np
import numpy.typing as npt

from daxs.scans import Scan, Scans

logger = logging.getLogger(__name__)


class BlissPath:
    def __init__(  # noqa
        self,
        root: str,
        proposal: str,
        beamline: str,
        session: str,
        sample: str,
        dataset: str,
        data_type: str = "RAW_DATA",
    ) -> None:
        self.root = root
        self.proposal = proposal
        self.beamline = beamline
        self.session = session
        self.sample = sample
        self.dataset = dataset
        self.data_type = data_type

    @property
    def collection(self) -> str:
        return f"{self.sample}_{self.dataset}"

    @property
    def filename(self) -> str:
        return f"{self.collection}.h5"

    @property
    def path(self) -> str:
        return os.path.join(
            self.root,
            self.proposal,
            self.beamline,
            self.session,
            self.data_type,
            self.sample,
            self.collection,
            self.filename,
        )

    @classmethod
    def from_path(cls, path: str) -> BlissPath:
        """Create a BlissPath object from a path."""
        tokens: list[str] = os.path.normpath(path).split(os.sep)
        if not tokens:
            raise ValueError("Invalid path.")
        tokens = tokens[::-1]
        _, collection, sample, data_type, session, beamline, proposal, *root = tokens
        # Determine the dataset name.
        dataset = collection.split(sample)[1][1:]
        # Create the root.
        root = os.path.join(os.sep, *root[::-1])
        return cls(root, proposal, beamline, session, sample, dataset, data_type)


class Selection:
    def __init__(
        self,
        items: int | str | list[int] | npt.NDArray[np.int64 | np.float64],
    ) -> None:
        """
        Class to handle selections of items.

        Parameters
        ----------
        items :
            The items to select.

        """
        if not isinstance(items, (int, str, list, np.ndarray)):  # type: ignore
            raise ValueError(
                "The items must be an integer, a string, a list of integers, or a "
                "Numpy array. \n"
                "For example: 1, [1, 2, 3], np.array([1, 2, 3]), "
                "or the output of certain functions like np.arange(1, 10, 2). \n"
                f"Provided items: {items}"
            )
        self._items = items

    @property
    def items(self):
        if isinstance(self._items, int):
            return [self._items]
        elif isinstance(self._items, str):
            raise ValueError(
                (
                    "Selecting scans using strings is not supported anymore. ",
                    "Please use a list of integers or a Numpy array",
                )
            )
        elif isinstance(self._items, list):
            for item in self._items:
                if not isinstance(item, int):  # type: ignore
                    raise ValueError("The items must be integers.")
            return self._items
        elif isinstance(self._items, np.ndarray):  # type: ignore
            return self._items.astype(np.int64).tolist()
        else:
            raise ValueError(
                "The items must be an integer, list of integers, or Numpy array."
            )

    def __iter__(self) -> Iterator[int]:
        return iter(self.items)


class Source(ABC):
    """Base class for sources of scans."""

    @property
    @abstractmethod
    def filename(self) -> str | None:
        """The filename of the source."""

    @property
    @abstractmethod
    def data_mappings(self) -> dict[str, Any]:
        """The mappings between scan attributes and paths in the source."""

    @data_mappings.setter
    def data_mappings(self, data_mappings: dict[str, Any]) -> None:
        """Set the mappings between scan attributes and paths in the source."""

    @abstractmethod
    def read_scans(
        self, indices: list[int] | npt.NDArray[np.int64] | None = None
    ) -> Scans:
        """Return all source scans."""


class Hdf5Source(Source):
    def __init__(
        self,
        filename: str,
        included_scan_ids: Any = None,
        excluded_scan_ids: Any = None,
        data_mappings: dict[str, Any] | None = None,
    ) -> None:
        """
        Class for a HDF5 source of scans

        Parameters
        ----------
        filename :
            Name of the HDF5 file.
        included_scans_ids :
            Selection of included scans.
        excluded_scans_ids :
            Selection of excluded scans.
        data_mappings :
            Mappings between scan attributes (x, signal, monitor, etc.) and paths in
            the HDF5 file.

        """
        included_scan_ids = [] if included_scan_ids is None else included_scan_ids
        excluded_scan_ids = [] if excluded_scan_ids is None else excluded_scan_ids

        self._filename = filename
        self.included_scan_ids = Selection(included_scan_ids)
        self.excluded_scan_ids = Selection(excluded_scan_ids)

        if not isinstance(data_mappings, dict):
            raise ValueError("The data_mappings must be a dict.")
        self._data_mappings = data_mappings

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def data_mappings(self) -> dict[str, Any]:
        return self._data_mappings

    @data_mappings.setter
    def data_mappings(self, data_mappings: dict[str, Any]) -> None:
        self._data_mappings = data_mappings

    @property
    def selected_scan_ids(self) -> list[int]:
        """Get the selected scans considering the included and excluded scan ids."""
        selected_scan_ids = []

        for index in sorted(self.included_scan_ids):
            if index not in self.excluded_scan_ids:
                selected_scan_ids.append(index)
            else:
                logger.info("Scan %s/%d was excluded.", self.filename, index)

        logger.debug(
            "The scans %s have been selected from %s.", selected_scan_ids, self.filename
        )
        return selected_scan_ids

    def read_scans(
        self, indices: list[int] | npt.NDArray[np.int64] | None = None
    ) -> Scans:
        """Read the scans from the source."""
        if indices is None:
            indices = self.selected_scan_ids
        return Scans([self.read_scan(index) for index in indices])

    def read_scan(self, index: int) -> Scan:
        """Return a scan object at the index."""
        if "x" not in self.data_mappings:
            raise ValueError("The data_mappings attribute must contain an entry for x.")
        if "signal" not in self.data_mappings:
            raise ValueError(
                "The data_mappings attribute must contain an entry for signal."
            )
        scan = Scan()
        scan.filename = self.filename
        scan.index = index

        # Read additional data paths.
        for key, data_paths in self.data_mappings.items():
            scan.data[key] = scan.read_data_at_path(data_paths)

        # Reindex the scan which includes sorting the data.
        scan.reindex()

        return scan
