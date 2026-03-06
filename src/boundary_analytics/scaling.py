"""Scaling model interfaces and placeholder diagnostics."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ScalingFitResult:
    """Structured return object for future log-log model fitting."""

    model_name: str
    n_observations: int
    slope: float | None
    intercept: float | None
    diagnostics: dict
    status: str


def fit_loglog_scaling_placeholder(
    epsilon_values: list[float],
    perimeter_values: list[float],
) -> ScalingFitResult:
    """Placeholder log-log fit interface.

    TODO: replace with a real implementation once observed perimeter data are
    available for each delineation bundle and study area.
    """
    if len(epsilon_values) != len(perimeter_values):
        raise ValueError("epsilon_values and perimeter_values must have equal length")
    if len(epsilon_values) < 2:
        raise ValueError("at least two observations are required")

    return ScalingFitResult(
        model_name="loglog_power_law",
        n_observations=len(epsilon_values),
        slope=None,
        intercept=None,
        diagnostics={"note": "placeholder_result"},
        status="placeholder_not_fitted",
    )
