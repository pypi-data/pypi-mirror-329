"""utility functions for taurex-cupy"""

import cupy as cp
import numpy as np
import numpy.typing as npt
from taurex.cia import CIA
from taurex.util import create_grid_res, find_closest_pair
from taurex.util.math import interp_lin_only


def cuda_find_closest_pair(arr: cp.ndarray, values: cp.ndarray) -> cp.ndarray:
    """
    Find the closest pair of values in an array

    Parameters
    ----------
    arr : cp.ndarray
        The array to search
    values : cp.ndarray
        The values to search for

    Returns
    -------
    cp.ndarray
        The indices of the closest pair
    """
    right = arr.searchsorted(values, side="right")
    right = cp.clip(right, 0, arr.shape[0] - 1)
    left = right - 1
    left = cp.clip(left, 0, arr.shape[0] - 1)

    return left, right


def determine_grid_slice(dest_wngrid: npt.NDArray[np.float64], src_wngrid: npt.NDArray[np.float64]) -> slice:
    """Determine the grid length of the destination grid.

    Args:
        dest_wngrid: The destination wavenumber grid.
        src_wngrid: The source wavenumber grid.

    Returns:
        slice: The slice of the destination grid.

    """
    min_grid_idx = 0
    max_grid_idx = None
    min_wn = dest_wngrid.min()
    max_wn = dest_wngrid.max()
    src_min = src_wngrid.min()
    src_max = src_wngrid.max()
    if min_wn > src_min:
        min_grid_idx = max(np.argmax(min_wn < src_wngrid) - 1, 0)
    if max_wn < src_max:
        max_grid_idx = np.argmax(src_wngrid >= max_wn) + 1

    return slice(min_grid_idx, max_grid_idx)


class FakeCIA(CIA):
    """Fake opacity for testing purposes."""

    def __init__(
        self,
        molecule_pair: tuple[str, str],
        num_t: int = 27,
        wn_res: int = 15000,
        wn_size: tuple[float, float] = (300, 30000),
    ) -> None:
        """Create the fake opacity.

        Args:
            molecule_pair: The pair of molecules.
            num_t: The number of temperature points.
            wn_res: The resolution of the wavenumber grid.
            wn_size: The size of the wavenumber grid.



        """
        super().__init__("FAKE", "-".join(molecule_pair))
        self.pair = molecule_pair
        self._wavenumber_grid = create_grid_res(wn_res, *wn_size)[:, 0]
        self._temperature_grid = np.linspace(100, 10000, num_t)
        self._xsec_grid = np.random.rand(self._temperature_grid.size, self._wavenumber_grid.size)

    def find_closest_temperature_index(self, temperature: float) -> tuple[int, int]:
        """Finds the nearest indices for a particular temperature

        Args:
            temperature: The temperature to search for.

        Returns:
            tuple[int, int]: The indices of the closest temperatures.

        """

        t_min, t_max = find_closest_pair(self.temperatureGrid, temperature)
        return t_min, t_max

    def interp_linear_grid(self, temperature: float, t_idx_min: int, t_idx_max: int) -> npt.NDArray[np.float64]:
        """Linear interpolate the CIA opacity.

        Args:
            temperature: The temperature to interpolate.
            t_idx_min: The minimum temperature index.
            t_idx_max: The maximum temperature index.

        Returns:
            The interpolated opacity.


        """

        if temperature > self._temperature_grid.max():
            return self._xsec_grid[-1]
        elif temperature < self._temperature_grid.min():
            return self._xsec_grid[0]

        temp_max = self._temperature_grid[t_idx_max]
        temp_min = self._temperature_grid[t_idx_min]
        fx0 = self._xsec_grid[t_idx_min]
        fx1 = self._xsec_grid[t_idx_max]

        return interp_lin_only(fx0, fx1, temperature, temp_min, temp_max)

    def compute_cia(self, temperature: float) -> npt.NDArray[np.float64]:
        """Computes the collisionally induced absorption cross-section.

        Args:
            temperature: The temperature to compute the opacity at.

        Returns:
            npt.NDArray[np.float64]: The opacity.

        """
        indicies = self.find_closest_temperature_index(temperature)
        return self.interp_linear_grid(temperature, *indicies)

    @property
    def moleculeName(self) -> str:
        """Name of molecule."""
        return self._molecule_name

    @property
    def xsecGrid(self) -> npt.NDArray[np.float64]:
        """Opacity grid."""
        return self._xsec_grid

    @property
    def wavenumberGrid(self) -> npt.NDArray[np.float64]:
        """Wavenumber grid."""
        return self._wavenumber_grid

    @property
    def temperatureGrid(self) -> npt.NDArray[np.float64]:
        """Temperature grid."""
        return self._temperature_grid
