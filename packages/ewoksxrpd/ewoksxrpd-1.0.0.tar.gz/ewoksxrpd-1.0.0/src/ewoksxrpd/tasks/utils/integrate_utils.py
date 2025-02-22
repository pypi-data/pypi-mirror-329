from contextlib import ExitStack
from typing import Optional, Tuple, Union
import numpy
from pyFAI.containers import Integrate1dResult, Integrate2dResult
from ewoksdata.data.hdf5.dataset_writer import DatasetWriter
from . import pyfai_utils
import h5py


def get_intensity_error(
    result: Union[Integrate1dResult, Integrate2dResult],
) -> numpy.ndarray:
    if result.sigma is None:
        return numpy.full_like(result.intensity, numpy.nan)

    sigma = result.sigma
    sigma[result.intensity <= 0] = numpy.nan

    return numpy.abs(sigma)


def save_result(
    result: Union[Integrate1dResult, Integrate2dResult],
    intensity_writer: Optional[DatasetWriter],
    error_writer: Optional[DatasetWriter],
    nxprocess: h5py.Group,
    stack: ExitStack,
    flush_period: Optional[float] = None,
) -> Tuple[Optional[DatasetWriter], Optional[DatasetWriter], bool]:
    if intensity_writer is None:
        radial_axis, azimuthal_axis = pyfai_utils.parse_pyfai_units(result.unit)
        nxdata = pyfai_utils.create_integration_results_nxdata(
            nxprocess,
            result.intensity.ndim + 1,  # +1 for the scan dimension
            result.radial,
            radial_axis.to_str(),
            result.azimuthal if isinstance(result, Integrate2dResult) else None,
            azimuthal_axis.to_str() if isinstance(result, Integrate2dResult) else None,
        )
        nxdata.attrs["signal"] = "intensity"
        intensity_writer = stack.enter_context(
            DatasetWriter(nxdata, "intensity", flush_period=flush_period)
        )
        if result.sigma is not None:
            error_writer = stack.enter_context(
                DatasetWriter(nxdata, "intensity_errors", flush_period=flush_period)
            )

    flush = intensity_writer.add_point(result.intensity)
    if result.sigma is not None:
        flush |= error_writer.add_point(result.sigma)

    return intensity_writer, error_writer, flush
