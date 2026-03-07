# What counts as the WUI boundary

Before perimeter is measured, the boundary object must be defined. In this project, that object-definition choice is denoted by \(d\).

## Object-definition sensitivity (choice of \(d\))

Different delineation rules can all be scientifically defensible, but they do not produce the same boundary geometry. Examples include differences in:

- settlement representation (points, polygons, gridded proxies),
- vegetation thresholds,
- neighborhood radius or connectivity assumptions,
- adjacency rules used to identify interface zones.

Changing these assumptions changes the boundary object itself.

## Distinguishing two sources of variation

The full perimeter quantity is
\[
L_d(\varepsilon).
\]

- Holding \(d\) fixed and varying \(\varepsilon\) reveals **measurement-scale sensitivity**.
- Holding \(\varepsilon\) fixed and varying \(d\) reveals **object-definition sensitivity**.

Both are scientifically important and should be reported separately whenever possible.

## Why this separation is essential

Without distinguishing object-definition and measurement-scale effects, disagreements in reported perimeter can be mistaken for ecological differences when they may instead be methodological.

[Next: Interactive experiments](interactive-experiments.md){ .md-button .md-button--primary }
