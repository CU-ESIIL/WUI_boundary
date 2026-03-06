"""Reporting helpers for manuscript/site outputs."""


def assemble_summary_row(
    delineation_id: str,
    study_area: str,
    fit_status: str,
    slope: float | None,
) -> dict:
    """Create one minimal row for summary exports."""
    if not delineation_id:
        raise ValueError("delineation_id is required")
    if not study_area:
        raise ValueError("study_area is required")

    return {
        "delineation_id": delineation_id,
        "study_area": study_area,
        "fit_status": fit_status,
        "slope": slope,
    }
