# Draft 1 — WUI Boundary Story Lab

This Draft 1 interface is a presentation-ready **story lab** for the manuscript's central claim: WUI boundary length is not a fixed scalar, but a scale-conditioned estimand.

<div class="oasis-embed">
  <iframe
    title="WUI Boundary Story Lab Draft 1"
    src="draft-1/story-lab.html"
    loading="lazy"
    allowfullscreen>
  </iframe>
</div>

[Open the Story Lab in a full page](draft-1/story-lab.html){ .md-button .oasis-hover-button }

## What this draft demonstrates

- **Definition scale sensitivity:** changing delineation choices changes the mapped boundary object itself.
- **Measurement scale sensitivity:** changing measurement scale changes the measured perimeter of that object.
- The object-level and measurement-level sensitivities are related but distinct, so the perimeter should be treated as \(L_d(\varepsilon)\), not a single number.

## What is still synthetic

- Geometry, perimeter values, and scaling behavior in this interface are synthetic.
- Controls and outputs are designed for clear conceptual communication in talks and manuscript walkthroughs.
- This draft is **not** the real analytics engine and does not ingest external geospatial datasets.

## What comes next

- The future analytics module will define defensible delineation bundles \(d\).
- It will measure perimeter across an explicit scale grid \(\varepsilon\).
- It will fit and diagnose scaling relationships in reproducible workflows and export manuscript-ready outputs.

For planned implementation details, see [Roadmap to Real Data](roadmap-to-real-data.md) and [Boundary Analytics Scaffold](../analytics/scaffold.md).
