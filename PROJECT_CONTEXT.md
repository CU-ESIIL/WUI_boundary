# PROJECT_CONTEXT

## Project Overview

This repository explores the hypothesis that **wildland–urban interface (WUI) boundaries may exhibit coastline-like fractal scaling**, analogous to the phenomenon described by Benoit Mandelbrot in the *coastline paradox*. In Mandelbrot’s formulation, the measured length of a coastline depends on the scale of measurement: the smaller the ruler, the longer the measured boundary becomes. This project investigates whether a similar **scale-dependent geometry** exists at the interface between human settlements and vegetated landscapes.

The goal is to determine whether WUI boundaries behave like **fractal perimeters**, where boundary length increases systematically as measurement resolution increases. If this relationship holds, it may reveal fundamental properties of how built environments interlace with vegetation and could influence wildfire modeling, landscape analysis, and hazard assessment.

---

## Conceptual Motivation

The idea for this project emerged from considering the geometry of WUI boundaries through the lens of fractal geometry. Urban development and natural vegetation often interlace in complex patterns. When mapped at different spatial resolutions, the boundary between buildings and vegetation may appear smooth at coarse resolution but increasingly complex at finer scales.

This raises a question similar to Mandelbrot’s coastline paradox:

> Does the measured length of the WUI boundary increase as measurement scale becomes finer?

If so, WUI boundaries may exhibit **fractal scaling behavior**, suggesting that the interface between built structures and vegetation forms a scale-dependent geometric structure.

Understanding this geometry could improve how wildfire risk models represent the **contact surface between fuels and human infrastructure**, which is a critical factor in fire spread and exposure.

---

## Hypothesis Development

During the exploratory phase of the project, several possible explanations for apparent fractal scaling in WUI boundaries were considered:

### Candidate Explanations Explored

1. **Measurement artifacts**
   - Satellite resolution effects
   - Raster resampling and classification boundaries
   - Map generalization effects

2. **Landscape ecology mechanisms**
   - Vegetation patch fragmentation
   - Percolation-like spatial structures
   - Heterogeneous ecological mosaics

3. **Urban development processes**
   - Road network expansion
   - Clustered settlement growth
   - Zoning and parcelization

4. **Fire and disturbance feedbacks**
   - Repeated disturbance shaping landscape boundaries
   - Suppression and management infrastructure

After exploring these possibilities, the project narrowed to a **working hypothesis** that can be tested directly with available geospatial data.

---

## Working Hypothesis

**Wildland–urban interface boundaries exhibit scale-dependent (fractal-like) geometry because the spatial interaction between discrete built structures and heterogeneous vegetation creates an interlaced boundary whose measured length depends on observation scale.**

In other words:

- Buildings form **discrete spatial objects**.
- Vegetation forms **heterogeneous spatial fields**.
- Their intersection generates **complex boundary geometry**.

When measured with progressively smaller rulers (or finer raster resolution), the boundary length may increase following a **power-law relationship**.

---

## Core Datasets

The analysis relies on two globally available geospatial datasets that can be combined to identify the building–vegetation interface.

### 1. OpenStreetMap (OSM) Building Footprints

Source:  
https://www.openstreetmap.org

Access method:

- Queried dynamically using **OSMnx**
- Extracted using the `building=True` tag

Purpose:

- Represent the spatial distribution of built structures
- Define the **urban component** of the WUI boundary

---

### 2. ESA WorldCover Land Cover Dataset

Source:  
https://esa-worldcover.org/

Resolution:

- 10-meter global land cover classification

Relevant vegetation classes include:

- Tree cover
- Shrubland
- Grassland
- Cropland
- Moss/lichen

Purpose:

- Identify **vegetated land cover**
- Provide the **wildland component** of the WUI boundary

---

## Prototype Workflow

The prototype workflow combines these datasets to measure WUI boundary scaling.

### Step 1 — Load Satellite Land Cover Raster

Load the ESA WorldCover raster tile and extract vegetation classes to create a **binary vegetation mask**.

```python
veg_mask = np.isin(data, veg_classes)
```
