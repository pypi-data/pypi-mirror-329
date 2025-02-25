__all__ = ["convolve"]

from typing import Literal

import numpy as np
from numpy.typing import NDArray

from rlic._core import convolve_f32, convolve_f64
from rlic._typing import ConvolveClosure, FloatT, f32, f64

_KNOWN_UV_MODES = ["velocity", "polarization"]
_SUPPORTED_DTYPES = [np.dtype("float32"), np.dtype("float64")]


class _ConvolveF32:
    @staticmethod
    def closure(
        image: NDArray[f32],
        u: NDArray[f32],
        v: NDArray[f32],
        kernel: NDArray[f32],
        iterations: int = 1,
        uv_mode: Literal["velocity", "polarization"] = "velocity",
    ) -> NDArray[f32]:
        return convolve_f32(image, u, v, kernel, iterations, uv_mode)


class _ConvolveF64:
    @staticmethod
    def closure(
        image: NDArray[f64],
        u: NDArray[f64],
        v: NDArray[f64],
        kernel: NDArray[f64],
        iterations: int = 1,
        uv_mode: Literal["velocity", "polarization"] = "velocity",
    ) -> NDArray[f64]:
        return convolve_f64(image, u, v, kernel, iterations, uv_mode)


def convolve(
    image: NDArray[FloatT],
    u: NDArray[FloatT],
    v: NDArray[FloatT],
    *,
    kernel: NDArray[FloatT],
    iterations: int = 1,
    uv_mode: Literal["velocity", "polarization"] = "velocity",
):
    if iterations < 0:
        raise ValueError(
            f"Invalid number of iterations: {iterations}\n"
            "Expected a strictly positive integer."
        )
    if iterations == 0:
        return image.copy()

    if uv_mode not in _KNOWN_UV_MODES:
        raise ValueError(
            f"Invalid uv_mode {uv_mode!r}. Expected one of {_KNOWN_UV_MODES}"
        )

    dtype_error_expectations = (
        f"Expected image, u, v and kernel with identical dtype, from {_SUPPORTED_DTYPES}. "
        f"Got {image.dtype=}, {u.dtype=}, {v.dtype=}, {kernel.dtype=}"
    )

    input_dtypes = {arr.dtype for arr in (image, u, v, kernel)}
    if unsupported_dtypes := input_dtypes.difference(_SUPPORTED_DTYPES):
        raise TypeError(
            f"Found unsupported data type(s): {list(unsupported_dtypes)}. "
            f"{dtype_error_expectations}"
        )

    if len(input_dtypes) != 1:
        raise TypeError(f"Data types mismatch. {dtype_error_expectations}")

    if image.ndim != 2:
        raise ValueError(
            f"Expected an image with exactly two dimensions. Got {image.ndim=}"
        )
    if np.any(image < 0):
        raise ValueError(
            "Found invalid image element(s). Expected only positive values."
        )
    if u.shape != image.shape or v.shape != image.shape:
        raise ValueError(
            "Shape mismatch: expected image, u and v with identical shapes. "
            f"Got {image.shape=}, {u.shape=}, {v.shape=}"
        )

    if kernel.ndim != 1:
        raise ValueError(
            f"Expected a kernel with exactly one dimension. Got {kernel.ndim=}"
        )
    if kernel.size < 3:
        raise ValueError(f"Expected a kernel with size 3 or more. Got {kernel.size=}")
    if kernel.size > (max_size := min(image.shape)):
        raise ValueError(
            f"{kernel.size=} exceeds the smallest dim of the image ({max_size})"
        )
    if np.any(kernel < 0):
        raise ValueError(
            "Found invalid kernel element(s). Expected only positive values."
        )

    input_dtype = image.dtype
    cc: ConvolveClosure[FloatT]
    if input_dtype == np.dtype("float32"):
        cc = _ConvolveF32  # type: ignore[assignment] # pyright: ignore reportAssignmentType
    elif input_dtype == np.dtype("float64"):
        cc = _ConvolveF64  # type: ignore[assignment] # pyright: ignore reportAssignmentType
    else:
        raise RuntimeError  # pragma: no cover
    return cc.closure(image, u, v, kernel, iterations, uv_mode)
