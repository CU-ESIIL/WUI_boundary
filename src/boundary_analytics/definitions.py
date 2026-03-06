"""Definitions for WUI delineation bundles.

These structures describe *how* a WUI boundary object is constructed (index d).
Real delineation logic is intentionally deferred until real datasets are integrated.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DelineationBundle:
    """Configuration for a defensible WUI definition bundle.

    Attributes:
        settlement_representation: e.g., point, parcel, rasterized footprint.
        vegetation_threshold: threshold used to classify nearby wildland vegetation.
        neighborhood_radius_m: neighborhood radius in meters.
        adjacency_rule: textual rule for deciding WUI adjacency.
    """

    settlement_representation: str
    vegetation_threshold: float
    neighborhood_radius_m: float
    adjacency_rule: str

    def label(self) -> str:
        """Return a concise label for documentation and reports."""
        return (
            f"settlement={self.settlement_representation}; "
            f"veg_thr={self.vegetation_threshold}; "
            f"radius_m={self.neighborhood_radius_m}; "
            f"adj={self.adjacency_rule}"
        )
