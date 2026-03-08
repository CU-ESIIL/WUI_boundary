# How long is the Wildland–Urban Interface boundary?

The Wildland–Urban Interface is one of the most consequential boundaries in wildfire science. It marks the places where settlement meets flammable landscape, where houses and infrastructure become entangled with vegetation capable of carrying fire, and where ecological process and human vulnerability are forced into direct contact. Maps of this interface now shape how exposure is estimated, how mitigation is prioritized, and how the geography of wildfire risk is described at regional and national scales.

Yet beneath these applications lies a deceptively simple question. How long is the Wildland–Urban Interface?

At first glance the problem appears straightforward. One might imagine drawing a line wherever development meets vegetation and then measuring the length of that line. But the apparent simplicity dissolves as soon as one asks what exactly is being measured. The WUI boundary is not a naturally given curve waiting quietly in the landscape to be recovered by a sufficiently careful algorithm. It is a spatial object that emerges from choices about how settlement is represented, how vegetation is classified, and how proximity between the two is interpreted.

Even once the boundary has been defined, its measured length remains unstable. Irregular boundaries behave differently at different scales of observation. A coarse ruler smooths over small bends and irregularities, while a finer ruler begins to follow them. This is the logic behind the coastline paradox described by Mandelbrot: the more carefully certain kinds of boundaries are traced, the longer they appear to become. The Wildland–Urban Interface shares many of these geometric properties.

For this reason the quantity examined throughout this site is written as \(L_d(\varepsilon)\), where \(d\) represents the delineation of the boundary and \(\varepsilon\) represents the scale at which that boundary is measured. The purpose of this manuscript-style site is not simply to report a perimeter value. It is to explore how the reported length of the WUI emerges from the interaction between landscape geometry, methodological choice, and measurement scale.

The pages that follow move from first principles to implication. They begin by asking why complex boundaries resist simple measurement, then turn to the question of what counts as the boundary in the first place, then to interactive experiments and scaling results, and finally to the consequences for remote sensing and wildfire science. The argument is simple, but its implications are not: there is no single WUI boundary length independent of delineation and scale.

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
