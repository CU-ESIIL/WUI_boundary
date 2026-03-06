"""Definitions for WUI delineation bundles.

These structures describe *how* a WUI boundary object is constructed (index d).
Real delineation logic is intentionally lightweight until real datasets are integrated.
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

    def short_id(self) -> str:
        """Return a filesystem-safe short identifier for delineation index d."""
        settlement = self.settlement_representation.replace(" ", "_")
        adjacency = self.adjacency_rule.replace(" ", "_")
        return f"{settlement}_v{self.vegetation_threshold:.2f}_r{int(self.neighborhood_radius_m)}_{adjacency}"
