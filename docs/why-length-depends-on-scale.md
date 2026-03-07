# Why length depends on scale

Boundary length depends on how closely we trace irregular structure. A coarse ruler skips fine bends; a fine ruler follows them. As ruler length shrinks, measured perimeter typically grows.

In this project, ruler length is represented as measurement scale \(\varepsilon\), and measured WUI perimeter is represented as \(L_d(\varepsilon)\).

## A coastline-style intuition for WUI boundaries

WUI boundaries are not smooth circles. They are spatial mosaics formed where settlement and wildland patterns interlock. Their edges include pockets, fingers, and disconnected fragments. Because of this complexity, perimeter is scale-conditioned rather than absolute.

## What changes when \(\varepsilon\) changes

For a fixed delineation \(d\):

- large \(\varepsilon\) smooths local detail and tends to produce shorter perimeter estimates;
- small \(\varepsilon\) resolves more structure and tends to produce longer estimates.

This is **measurement-scale sensitivity**. It reflects how we measure an object, not necessarily a change in the object itself.

## Why this matters before any WUI-specific model

If two studies use different effective resolutions, their perimeter estimates are not directly comparable, even when they describe the same mapped boundary object. Scale must therefore be reported as part of the result.

## Transition to WUI delineation choices

Measurement-scale sensitivity explains variation within a fixed object. The next step is object-definition sensitivity: different delineation choices \(d\) can produce different boundary objects before measurement begins.

[Next: What counts as the WUI boundary?](what-counts-as-wui-boundary.md){ .md-button .md-button--primary }
