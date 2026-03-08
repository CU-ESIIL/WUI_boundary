# Scaling results

Once the boundary object has been defined and measurement scale has been made explicit, the next step is to examine how the reported perimeter changes across a range of scales. The figure on this page summarizes that relationship for the current demonstration analysis.

Each point represents a measurement of the same boundary traced with a different effective ruler length. Coarser rulers smooth over many small irregularities, producing shorter perimeter estimates. Finer rulers follow these irregularities more closely and therefore accumulate additional length. The figure should therefore be read not as a search for a single correct perimeter, but as a compact representation of how measured length changes across observational scales.

The present demonstration remains synthetic and conceptual. Its purpose is not to estimate a definitive empirical scaling law for the Wildland–Urban Interface, but to show how perimeter behaves when scale is treated as an explicit variable. In that sense the figure is less an answer than a statement of method: boundary length is meaningful only in relation to how the boundary was defined and how finely it was measured.

The slope and form of the relationship matter because they summarize scale sensitivity. A steeper decline toward coarser ruler lengths indicates that the measured perimeter is strongly dependent on the observational scale used to trace it. A flatter relationship would suggest weaker sensitivity over the same range. In either case, the central scientific point remains the same: perimeter is not independent of scale.

Read alongside the remote-sensing discussion, this result becomes more than a geometric curiosity. It implies that satellite products of different spatial resolution may return systematically different interface lengths even when they are nominally describing the same landscape. The current figure is synthetic, but the interpretive logic it illustrates is directly relevant to empirical WUI mapping.

<img src="/WUI_boundary/assets/figures/boundary_scaling_plot.svg" alt="Synthetic WUI boundary scaling relationship with labeled axes and annotation" loading="lazy" class="scaling-results-plot" />

*Figure 1. Measurements of a single delineated boundary across progressively coarser effective ruler lengths. The downward trend shows that measured perimeter shortens as scale becomes coarser, and the fitted relationship summarizes the strength of this scale sensitivity over the tested range.*

The current synthetic summary data are available at [`docs/assets/data/boundary_scaling_summary.csv`](/WUI_boundary/assets/data/boundary_scaling_summary.csv).

| Delineation scenario | Boundary object ID | Measurement scale, \(\varepsilon\) | Measured boundary length | Fit status | Fitted slope (log-log) |
| --- | --- | ---: | ---: | --- | ---: |
| parcel_v0.35_r120_touches | synthetic_wui_boundary_001 | 1.0 | 738.9227 | ok_fitted | -0.003054 |
| parcel_v0.35_r120_touches | synthetic_wui_boundary_001 | 13.4286 | 737.1697 | ok_fitted | -0.003054 |
| parcel_v0.35_r120_touches | synthetic_wui_boundary_001 | 30.0 | 730.3127 | ok_fitted | -0.003054 |

To refresh this figure and table from the current pipeline, run the reproducibility workflow documented on the methods page, including `scripts/pre_pr_site_review.sh` for website-facing validation.

[Next: Fire science implications](fire-science-implications.md){ .md-button .md-button--primary }
