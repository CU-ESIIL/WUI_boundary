"""Scaling model helpers and diagnostics."""

from dataclasses import dataclass
from math import isfinite, log


@dataclass(frozen=True)
class ScalingFitResult:
    """Structured return object for log-log model fitting."""

    model_name: str
    n_observations: int
    slope: float | None
    intercept: float | None
    diagnostics: dict
    status: str


def fit_loglog_scaling(
    epsilon_values: list[float],
    perimeter_values: list[float],
    min_points: int = 3,
) -> ScalingFitResult:
    """Fit log(L_d(epsilon)) ~ a + b * log(epsilon) if enough points exist."""
    if len(epsilon_values) != len(perimeter_values):
        raise ValueError("epsilon_values and perimeter_values must have equal length")
    if len(epsilon_values) < 2:
        raise ValueError("at least two observations are required")

    valid_pairs = [
        (e, p)
        for e, p in zip(epsilon_values, perimeter_values, strict=False)
        if e > 0 and p > 0 and isfinite(e) and isfinite(p)
    ]

    if len(valid_pairs) < min_points:
        return ScalingFitResult(
            model_name="loglog_power_law",
            n_observations=len(valid_pairs),
            slope=None,
            intercept=None,
            diagnostics={"reason": "too_few_points", "min_points": min_points},
            status="insufficient_points",
        )

    xs = [log(e) for e, _ in valid_pairs]
    ys = [log(p) for _, p in valid_pairs]
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    sxx = sum((x - x_mean) ** 2 for x in xs)

    if sxx == 0:
        return ScalingFitResult(
            model_name="loglog_power_law",
            n_observations=len(valid_pairs),
            slope=None,
            intercept=None,
            diagnostics={"reason": "zero_variance_log_epsilon"},
            status="ill_conditioned",
        )

    sxy = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys, strict=False))
    slope = sxy / sxx
    intercept = y_mean - slope * x_mean

    residuals = [y - (intercept + slope * x) for x, y in zip(xs, ys, strict=False)]
    sse = sum(r**2 for r in residuals)

    return ScalingFitResult(
        model_name="loglog_power_law",
        n_observations=len(valid_pairs),
        slope=slope,
        intercept=intercept,
        diagnostics={"sse": sse},
        status="ok_fitted",
    )
