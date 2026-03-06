"""Reporting helpers for manuscript/site outputs."""

from pathlib import Path


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


def write_markdown_summary(output_path: Path, lines: list[str]) -> None:
    """Write a small markdown summary file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
