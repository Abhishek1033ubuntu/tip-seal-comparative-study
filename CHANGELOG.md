# Changelog

All notable updates to the **Tip-Seal & Blade-Tip Architecture Study** repository are documented in this file.

## [1.0.0] - 2026-11-23

### Added
 * **CAD Solids (`cad/`):** Added watertight ISO 10303-21 STEP files `track_a_carbide_piston_ring.step`, `track_a_zero_hole_shroud.step`, and `track_b_open_tip_22holes.step`.
 * **Surface Meshes (`meshes/`):** Added triangulated STL meshes generated at 0.02 mm chordal tolerance and 0.1 rad angular tolerance.
 * **Simulation Scripts (`scripts/`):**
   * `01_cad_verify_and_stl_export.py` — Native OpenCASCADE B-Rep radial slicing and multi-panel orthographic verification.
   * `02_compressible_leakage_comparison.py` — Isentropic/choked compressible mass-flux sweep (Π = 1.05 to 3.00) with Vermes labyrinth carry-over modeling.
   * `03_tip_clearance_and_liftoff_sensitivity.py` — Parametric sensitivity across Track B tip clearances (0.25 mm, 0.50 mm, 1.00 mm) and Track A degraded ring lift-off states.
   * `04_stage_power_loss_and_pdf_report.py` — Stage bypass power loss (kW) and efficiency penalty (%) evaluation across 10–60 kg/s core flows with secondary mixing factor k<sub>mix</sub> = 1.65.
 * **Figures & Report (`figures/`, `reports/`):** Added four verification plots and the comparative technical assessment PDF report.
 * **Citation & Metadata (`CITATION.cff`, `References.md`, `RELEASE_NOTES.md`, `requirements.txt`, `.gitignore`):** Added complete release, licensing, and academic citation files attributed to Abhishek Singh.
