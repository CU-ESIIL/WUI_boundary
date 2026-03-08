# Reproducible prompts

This project was developed through an iterative conversation between scientific reasoning, code generation, interface design, and analytical refinement. The purpose of this page is to make that workflow more reproducible. What follows is not a single master prompt, but a set of reusable prompt blocks that correspond to different stages of the project. Together they show how a reader might reconstruct the same line of work: from the initial scientific question, to the analytical scaffold, to the narrative website that presents the results.

These prompts are not intended to imply that the project emerged automatically from prompting alone. They should instead be understood as research instruments. Like scripts, notebooks, or figure-generating pipelines, they make parts of the workflow more explicit, more portable, and easier to repeat.

## Prompting the scientific question

```text
I want to study how the measured length of the Wildland–Urban Interface depends on both how the boundary is defined and the scale at which it is measured. Help me formalize this as a scientific question, identify the key variables, and connect it to ideas like the coastline paradox, fractal geometry, and remote sensing resolution.
```

## Prompting the analytical scaffold

```text
Create a lightweight Python analysis scaffold that treats measured WUI boundary length as L_d(epsilon), where d is the delineation choice and epsilon is the measurement scale. Start with synthetic boundary geometry, measure perimeter across a grid of scales, and generate publication-style plots and summary tables.
```

## Prompting the website structure

```text
Redesign this MkDocs site so it reads like a manuscript rather than a documentation portal. The public site should tell a scientific story in this order: the question, why length depends on scale, what counts as the WUI boundary, interactive experiments, scaling results, implications for remote sensing, and implications for wildfire science.
```

## Prompting the interactive experiments

```text
Create a self-contained HTML experiment that helps readers understand how a boundary changes when its delineation rules and measurement scale change. The app should behave like an interactive scientific figure, not like a generic dashboard. Controls and map outputs should remain visually linked in both full-page and iframe contexts.
```

## Prompting the scaling interpretation

```text
Write a scholarly explanation of how to interpret a scaling plot where measured boundary length changes across ruler lengths or pixel sizes. Explain what the slope means, why the relationship matters, and how it connects to synthetic demonstrations versus empirical remote-sensing analysis.
```

## Prompting the remote-sensing implications

```text
Explain why satellite data do not simply observe the WUI boundary but help determine the scale at which it becomes visible and measurable. Connect pixel size to effective ruler length and discuss why WUI perimeter estimates may not be directly comparable across sensors, regions, or time.
```

## Prompting the real-data transition

```text
Help me move from a synthetic WUI boundary scaling demo to a small real-data experiment. Propose a minimal reproducible pipeline that downloads a sample settlement dataset and a sample vegetation dataset for one test region, constructs a WUI-like boundary object, and measures its perimeter across multiple scales.
```

## Prompting site cleanup and scholarly prose

```text
Rewrite this website so it reads like a short scholarly monograph with interactive figures. Use paragraph-based prose, preserve L_d(epsilon), reduce outline-style language, keep the manuscript-like navigation, and maintain scientific honesty about what is synthetic versus empirical.
```

The prompts on this page are intended as reusable building blocks. They can be adapted, recombined, or extended depending on whether the user is trying to reproduce the current synthetic demonstration, improve the website, or move the analysis toward empirical WUI data.
