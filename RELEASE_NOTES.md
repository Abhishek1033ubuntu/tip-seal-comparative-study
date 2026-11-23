# Release v1.0.0 — Tip-Seal & Blade-Tip Architecture Comparative Study

**Release Tag:** `v1.0.0`  
**Release Date:** November 23, 2026  
**Lead Author / Principal Investigator:** Abhishek Singh ([ORCID: 0009-0004-6913-096X](https://orcid.org/0009-0004-6913-096X))  
**Repository:** [Abhishek1033ubuntu/tip-seal-comparative-study](https://github.com/Abhishek1033ubuntu/tip-seal-comparative-study)  
**License:** Apache-2.0  

---

## Release Highlights

This initial public release (`v1.0.0`) delivers a complete, reproducible CAD, thermal stack-up, compressible leakage, and stage power-loss comparison between two rotating turbomachinery tip-sealing architectures:

 * **Track A (Zero-Hole Labyrinth Shroud + Split Carbide Piston Ring):** Watertight STEP and STL models of an annular zero-perforation shroud (R<sub>in</sub> = 200.00 mm, R<sub>out</sub> = 204.20 mm cold, six tapered labyrinth teeth) paired with a pressure-energized split tungsten-carbide (WC-Co) piston ring (R<sub>in</sub> = 202.12 mm, R<sub>out</sub> = 204.17 mm cold, axial height 2.48 mm).
 * **Track B (Open-Tip Blade Profile + 22-Port Cross-Bleed Array):** Watertight STEP and STL models of a lofted B-spline blade tip (tip rim at Z ≈ 66.00 mm, internal step at Z = 60.00 mm) incorporating twenty-two Ø 2.20 mm through-holes spaced at 5.00 mm pitch along Z = 54.72 mm.
 * **Differential Thermal Stack-Up (+500 K Soak):** Analytical verification from 20 °C to 520 °C confirming zero root pinching (+0.908 mm radial back-clearance), positive axial side-play (+0.130 mm), and safe end-gap retention (+1.845 mm under a +150 K ring thermal lag) when paired with a cold stationary casing bore radius ≥ 204.85 mm.
 * **Compressible Leakage & Power-Loss Benchmark:** At stage pressure ratio Π = 2.00, T<sub>in</sub> = 800 K, γ = 1.35, and 25.0 kg/s core flow (Δh<sub>s</sub> = 145.69 kJ/kg):
   * **Track A (Baseline):** **6.01 g/s** leakage | **0.88 kW** bypass power loss | **0.02%** stage efficiency penalty (**99.25%** leakage reduction vs. Track B).
   * **Track A (Degraded / Lift-Off):** **24.12 g/s** leakage | **3.51 kW** bypass power loss | **0.10%** stage efficiency penalty (**96.98%** leakage reduction vs. Track B).
   * **Track B (36-Blade Annulus, 0.50 mm Tip Gap):** **799.07 g/s** leakage | **116.42 kW** pure bypass loss (**3.10%** penalty) | **192.09 kW** mixing-adjusted loss (**5.11%** penalty at k<sub>mix</sub> = 1.65).
   * * **Vortex Suppression & Second-Order Entropy Reduction:** Explicitly documents suppression of tip-leakage and cross-bleed jet vortices alongside reduction of second-order aerodynamic and mixing entropy generation (Ṡ<sub>gen,II</sub>) achieved by Track A relative to Track B.

---

## Release Assets Checklist

 * `cad/` — ISO 10303-21 (`STEP AP214`) watertight B-Rep solids for Track A and Track B.
 * `meshes/` — High-resolution triangulated `.stl` surface meshes (0.02 mm chordal tolerance).
 * `scripts/` — Self-contained Python scripts for B-Rep sectioning, compressible flow sweeps, clearance/lift-off sensitivity, and stage power-loss modeling.
 * `figures/` — High-resolution verification sheets and parametric performance plots (`.png`).
 * `reports/` — Comparative technical assessment report (`Tip_Seal_Comparative_Assessment_Report.pdf`).
 * `CITATION.cff` & `References.md` — Machine-readable citation metadata and public engineering standards links.

---

## Attribution & AI Collaboration Notice

 * **Lead Author / Sole Inventor:** Abhishek Singh (`Copyright (c) 2026 Abhishek Singh`)
 * **AI Computational & Multi-Physics Support:** Google Gemini (Team Gemini, Google DeepMind) — assisted with numerical verification scripts, B-Rep cross-section plotting, and release documentation formatting under the direction of Abhishek Singh.
