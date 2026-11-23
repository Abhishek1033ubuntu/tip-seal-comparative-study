# Tip-Seal & Blade-Tip Architecture Study: Zero-Hole Labyrinth Shroud + Carbide Ring (Track A) vs. Open-Tip 22-Port Bleed Array (Track B)

[![Lead Author](https://img.shields.io/badge/Lead%20Author-Abhishek%20Singh-0f172a.svg)](https://orcid.org/0009-0004-6913-096X)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0004--6913--096X-a6ce39.svg)](https://orcid.org/0009-0004-6913-096X)
[![AI Collaborator](https://img.shields.io/badge/AI%20Collaborator-Google%20Gemini-4285F4.svg)](https://deepmind.google/technologies/gemini/)
[![AI Computational Support](https://img.shields.io/badge/AI%20Computational%20%26%20Multi--Physics%20Support-Team%20Gemini%20(Google%20DeepMind)-1a73e8.svg)](https://deepmind.google/technologies/gemini/)
[![License](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

---

## 1. Original Engineering Case Study & Industrial Context

Parasitic over-tip gas leakage is one of the largest single sources of aerodynamic loss, stage work degradation, and thermal distress in high-pressure rotating turbomachinery. Across unshrouded or perforated-tip turbine and compressor stages, the static pressure differential between the pressure side and suction side—combined with the axial stage pressure ratio—drives high-momentum fluid across the radial tip gap and through tip-cooling/bleed perforations. This leakage jet bypasses useful rotor work extraction and rolls up into a tip-leakage vortex that disrupts main-passage boundary layers.

### Applicable Equipment Envelope

The two architectures modeled, verified, and benchmarked in this repository are directly applicable to high-temperature, elevated-pressure-ratio rotating equipment:

 * **Axial & Radial Gas Turbine Stages:** High-pressure (HP) and intermediate-pressure (IP) rotor rows operating at elevated gas temperatures (T<sub>in</sub> ≈ 800 K and above) where radial tip-clearance growth during thermal transients drives severe specific fuel consumption (SFC) penalties.
 * **High-Pressure Industrial Centrifugal & Axial Compressors:** Multi-stage compression trains where inter-stage recirculation across rotor tips reduces surge margin and polytropic efficiency.
 * **Supercritical CO<sub>2</sub> (sCO<sub>2</sub>) & High-Pressure Steam Expanders:** Compact power-generation expanders where high fluid density and steep pressure ratios (Π = P<sub>in</sub> / P<sub>out</sub> from 1.2 to 3.0) amplify leakage mass flux through even sub-millimeter clearances.
 * **Shrouded Turbomachinery Retrofits:** Rotor tip-shroud assemblies requiring zero-perforation containment and low-CTE (coefficient of thermal expansion) sealing rings to prevent radial binding across wide thermal soak cycles (ΔT = +500 K).

### Comparative Architectural Scope

 * **Track A — Zero-Hole Labyrinth Shroud + Split Carbide Piston Ring:** A continuous, non-perforated annular shroud (R<sub>in</sub> = 200.00 mm, R<sub>out</sub> = 204.20 mm cold, axial height 25.00 mm) incorporating a central rectangular ring groove (R = 202.00 mm, axial width 2.60 mm) flanked by six tapered labyrinth sealing teeth (R<sub>root</sub> = 198.40 mm). A pressure-energized tungsten-carbide (WC-Co) split piston ring (R<sub>in</sub> = 202.12 mm, R<sub>out</sub> = 204.17 mm, axial height 2.48 mm, circumferential thermal end-gap ≈ 2.84 mm cold) seats inside the groove and expands radially against the stationary outer casing under internal gas pressure.
 * **Track B — Open-Tip Blade Profile + 22-Hole Bleed Array:** A lofted B-spline airfoil tip section (chordwise span X ≈ -103.87 mm to +70.00 mm at Z = 0, tip rim at Z ≈ 66.00 mm with an internal cavity step at Z = 60.00 mm) operating unshrouded with a baseline radial running tip clearance of 0.50 mm (Z<sub>casing</sub> = 66.50 mm) and twenty-two Ø 2.20 mm through-holes arranged at 5.00 mm pitch along Z = 54.72 mm.

---

## 2. Quantitative Benchmark & Thermal Stack-Up Results

### A. Differential Thermal Stack-Up Verification (Track A, ΔT = +500 K: 20 °C → 520 °C)

Using α<sub>WC-Co</sub> = 5.2 × 10<sup>-6</sup> K<sup>-1</sup> for the carbide ring and α<sub>shroud</sub> = 13.0 × 10<sup>-6</sup> K<sup>-1</sup> for the metallic shroud:

| Interface / Clearance Metric | Cold State (20 °C) | Hot State (520 °C) | Engineering Verdict |
| :--- | :--- | :--- | :--- |
| **Radial Back-Clearance** (R<sub>ring,in</sub> − R<sub>groove</sub>) | +0.120 mm | +0.908 mm | Shroud groove grows outward faster; zero root pinching |
| **Shroud OD vs. Ring OD Offset** (R<sub>shroud,out</sub> − R<sub>ring,out</sub>) | +0.030 mm | +0.826 mm | Ring OD reaches 204.701 mm; size cold casing bore ≥ 204.85 mm |
| **Axial Groove Side-Play** (W<sub>groove</sub> − h<sub>ring</sub>) | +0.120 mm | +0.130 mm | Prevents axial binding while maintaining downstream face seal |
| **Ring End-Gap** (Worst-case +150 K ring thermal lag) | 2.840 mm | 1.845 mm | Positive circumferential clearance retained; zero butt-joint buckling |

### B. Compressible Tip-Leakage & Stage Power Loss (PR = 2.0, T<sub>in</sub> = 800 K, γ = 1.35, Core Flow = 25.0 kg/s)

At Π = 2.0 and T<sub>in</sub> = 800 K, the isentropic specific enthalpy drop across the stage is Δh<sub>s</sub> = 145.69 kJ/kg:

| Configuration | Effective Annulus Leakage | Leakage Reduction vs. Track B | Bypass Power Loss (k = 1.0) | Mixing-Adjusted Power Loss (k<sub>mix</sub> = 1.65) | Stage Efficiency Penalty (@ 25 kg/s Core) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Track A (Baseline Seal)** | **6.01 g/s** | **99.25%** | **0.88 kW** | — | **0.02%** |
| **Track A (Degraded / Lift-Off)** | **24.12 g/s** | **96.98%** | **3.51 kW** | — | **0.10%** |
| **Track B (36-Blade, 0.25 mm Gap)** | ~510.0 g/s | — | ~74.30 kW | ~122.60 kW | ~2.00% (bypass) |
| **Track B (36-Blade, 0.50 mm Gap)** | **799
