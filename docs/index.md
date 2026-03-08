# How long is the Wildland–Urban Interface boundary?

<div class="esiil-hero" markdown>

The Wildland–Urban Interface (WUI) is one of the most consequential boundaries in wildfire science. Yet a simple question has no single answer: **how long is the WUI boundary?**

Our central claim is that boundary length is not a fixed scalar. It is a scale-conditioned quantity,
\[
L_d(\varepsilon),
\]
where **\(d\)** is the delineation choice (what counts as the boundary) and **\(\varepsilon\)** is the measurement scale (the effective ruler length or resolution).

<div class="oasis-embed" markdown>
  <iframe
    title="Interactive Figure — Measuring the WUI boundary"
    src="ui-drafts/draft-1/story-lab.html"
    loading="lazy"
    allowfullscreen>
  </iframe>
</div>

[Enter the interactive experiments](interactive-experiments.md){ .md-button .md-button--primary }
[Read the scaling intuition](why-length-depends-on-scale.md){ .md-button }

</div>


!!! tip "Current synthetic output"
    See the latest published figure and CSV on [Scaling Results](scaling-results.md).  
    If those look stale, the workflow likely ran on a PR (artifact only) rather than a manual dispatch (commits docs assets).

Satellite-like measurement scale is now treated explicitly as part of interpretation; see [Implications for remote sensing](implications-for-remote-sensing.md) for a manuscript-style discussion and synthetic scale demonstration.

## The question

When WUI boundaries are used for exposure, risk, and planning decisions, perimeter length is often treated as if it were a stable property of the landscape. This site treats that assumption as a testable scientific hypothesis.

## Why this is difficult

Two distinct mechanisms change measured length:

1. **Object-definition sensitivity:** changing delineation assumptions changes the boundary object itself.
2. **Measurement-scale sensitivity:** changing resolution changes the measured length of a fixed boundary object.

Because both mechanisms operate together, the reported length depends on both \(d\) and \(\varepsilon\).

## What this site lets you test

This manuscript-style site combines intuition, definitions, interactive figures, and reproducible synthetic outputs so you can inspect how \(L_d(\varepsilon)\) behaves under different assumptions.

## Main takeaway

There is no single WUI boundary length independent of delineation and measurement scale. Comparisons are only meaningful when \(d\) and \(\varepsilon\) are explicit.

## Where to go next

<div class="grid cards" markdown>

- **Why Length Depends on Scale**  
  Build intuition for why complex boundaries produce different lengths at different ruler sizes.  
  [Read the explainer](why-length-depends-on-scale.md)

- **What Counts as the WUI Boundary**  
  See how delineation assumptions define different boundary objects before measurement starts.  
  [Define \(d\)](what-counts-as-wui-boundary.md)

- **Interactive Experiments**  
  Explore figure-driven experiments comparing definition and measurement sensitivity.  
  [Open the lab](interactive-experiments.md)

- **Scaling Results**  
  Review synthetic demo outputs and the log-log scaling framework used to summarize \(L_d(\varepsilon)\).  
  [View results](scaling-results.md)

- **Fire Science Implications**  
  Connect geometric sensitivity to interpretation, comparability, and applied wildfire science.  
  [Interpret implications](fire-science-implications.md)

- **Methods & Reproducibility**  
  Inspect the current analysis scaffold, status, and reproducible execution workflow.  
  [Review methods](methods-reproducibility.md)

</div>
