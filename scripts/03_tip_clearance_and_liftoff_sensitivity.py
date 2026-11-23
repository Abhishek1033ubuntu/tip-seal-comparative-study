# Copyright (c) 2026 Abhishek Singh
# ORCID: https://orcid.org/0009-0004-6913-096X
# GitHub: https://github.com/Abhishek1033ubuntu
# AI Computational & Multi-Physics Support: Team Gemini (Google DeepMind)

import numpy as np
import matplotlib.pyplot as plt

T_in = 800.0
P_out = 101325.0
gamma = 1.35
R_gas = 287.05
PR_sweep = np.linspace(1.05, 3.0, 50)
P_in_sweep = PR_sweep * P_out

def compressible_mass_flux(P0, P_back, T0, Cd):
    PR_crit = ((gamma + 1.0) / 2.0) ** (gamma / (gamma - 1.0))
    PR = P0 / P_back
    if PR >= PR_crit:
        factor = np.sqrt(gamma / (R_gas * T0)) * ((2.0 / (gamma + 1.0)) ** ((gamma + 1.0) / (2.0 * (gamma - 1.0))))
        return Cd * P0 * factor
    term1 = (2.0 * gamma) / (R_gas * T0 * (gamma - 1.0))
    term2 = (P_back / P0) ** (2.0 / gamma) - (P_back / P0) ** ((gamma + 1.0) / gamma)
    return Cd * P0 * np.sqrt(term1 * np.maximum(term2, 0.0))

chord_len = 140.0e-3
N_holes = 22
d_hole = 2.20e-3
N_blades_equiv = int(np.round((2.0 * np.pi * 200.0e-3) / 35.0e-3))
Cd_track_b = 0.78

R_casing = 204.85e-3
R_ring_out_hot = 204.701e-3
N_teeth = 6
pitch_teeth = 3.2e-3
clearance_lab = 0.35e-3
alpha_carry = 1.0 / np.sqrt(1.0 - (1.0 / (1.0 + (clearance_lab / pitch_teeth))))
Cd_track_a = (0.62 / np.sqrt(N_teeth)) * alpha_carry

A_track_a_base = (1.845e-3 * (R_casing - R_ring_out_hot)) + (2.0 * np.pi * R_ring_out_hot * 0.02e-3)
A_track_a_degraded = (3.00e-3 * 0.50e-3) + (2.0 * np.pi * R_ring_out_hot * 0.08e-3)

mdot_A_base = np.array([compressible_mass_flux(p, P_out, T_in, Cd_track_a) * A_track_a_base for p in P_in_sweep])
mdot_A_deg = np.array([compressible_mass_flux(p, P_out, T_in, Cd_track_a) * A_track_a_degraded for p in P_in_sweep])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.2), dpi=150)

for gap_mm in [0.25, 0.50, 1.00]:
    A_b = N_blades_equiv * (chord_len * (gap_mm * 1e-3) + 0.35 * N_holes * (np.pi * (d_hole / 2.0) ** 2))
    mdot_b_var = np.array([compressible_mass_flux(p, P_out, T_in, Cd_track_b) * A_b for p in P_in_sweep])
    ax1.plot(PR_sweep, mdot_b_var * 1000.0, linewidth=2.0, label=f"Track B (Tip Gap = {gap_mm:.2f} mm)")

ax1.plot(PR_sweep, mdot_A_base * 1000.0, color="black", linestyle="--", linewidth=2.0, label="Track A (Baseline Seal)")
ax1.set_title("Track B Tip-Clearance Sensitivity (800 K)", fontsize=11, fontweight="bold")
ax1.set_xlabel("Pressure Ratio (P_in / P_out)")
ax1.set_ylabel("Leakage Mass Flow Rate [g/s]")
ax1.grid(True, linestyle="--", alpha=0.5)
ax1.legend(fontsize=8.5)

mdot_B_ref = np.array([
    compressible_mass_flux(p, P_out, T_in, Cd_track_b) *
    (N_blades_equiv * (chord_len * 0.50e-3 + 0.35 * N_holes * (np.pi * (d_hole / 2.0) ** 2)))
    for p in P_in_sweep
])

red_base = (1.0 - mdot_A_base / np.maximum(mdot_B_ref, 1e-12)) * 100.0
red_deg = (1.0 - mdot_A_deg / np.maximum(mdot_B_ref, 1e-12)) * 100.0

ax2.plot(PR_sweep, red_base, color="#1f77b4", linewidth=2.2, label="Track A Baseline vs. Track B (0.50 mm)")
ax2.plot(PR_sweep, red_deg, color="#d62728", linewidth=2.2, label="Track A Degraded/Lift-Off vs. Track B (0.50 mm)")
ax2.set_title("Leakage Reduction Sensitivity to Ring Lift-Off", fontsize=11, fontweight="bold")
ax2.set_xlabel("Pressure Ratio (P_in / P_out)")
ax2.set_ylabel("Leakage Reduction [%]")
ax2.set_ylim(85, 100.5)
ax2.grid(True, linestyle="--", alpha=0.5)
ax2.legend(fontsize=8.5)

plt.tight_layout()
plt.savefig("figures/tip_leakage_sensitivity.png", dpi=200)
