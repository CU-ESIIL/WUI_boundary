"""Boundary analytics scaffold for scale-conditioned WUI perimeter workflows."""

from .definitions import DelineationBundle
from .measurement import ScaleGrid, validate_scale_grid
from .scaling import ScalingFitResult, fit_loglog_scaling_placeholder

__all__ = [
    "DelineationBundle",
    "ScaleGrid",
    "ScalingFitResult",
    "fit_loglog_scaling_placeholder",
    "validate_scale_grid",
]
