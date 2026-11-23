# Copyright (c) 2026 Abhishek Singh
# ORCID: https://orcid.org/0009-0004-6913-096X
# GitHub: https://github.com/Abhishek1033ubuntu
# AI Computational & Multi-Physics Support: Team Gemini (Google DeepMind)

import numpy as np
import matplotlib.pyplot as plt

T_in = 800.0          # Inlet total temperature [K]
P_out = 101325.0      # Downstream static pressure [Pa]
gamma = 1.35          # Specific heat ratio for hot gas
R_gas = 287.05        # Specific gas constant [J/(kg*K)]

PR_sweep = np.linspace(1.05, 3.0, 50)
P_in_sweep = PR_sweep * P_out

def compressible_mass_flux(P0, P_back, T0, Cd):
    """Computes compressible mass flow per unit area [kg/(s*m^2)] with choking check."""
    PR_crit = ((gamma + 1.0) / 2.0) ** (gamma / (gamma - 1.0))
    PR = P0 / P_back
    if PR >= PR_crit:
        factor = np.sqrt(gamma / (R_gas * T0)) * ((2.0 / (gamma + 1.0)) ** ((gamma + 1.0) / (2.0 * (gamma - 1.0))))
        return Cd * P0 * factor
    term1 = (2.0 * gamma) / (R_gas * T0 * (gamma - 1.0))
    term2 = (P_back / P0) ** (2.0 / gamma) - (P_back / P0) ** ((gamma + 1.0) / gamma)
    return Cd * P0 * np.sqrt(term1 * np.maximum(term2, 0.0))

# Track A Geometry Parameters
R_casing = 204.85e-3
R_ring_out_hot = 204.701e-3
gap_end_hot = 1.845e-3
N_teeth = 6
pitch_teeth = 3.2e-3
clearance_lab = 0.35e-3

A_end_gap = gap_end_hot * (R_casing - R_ring_out_hot)
A_ring_film = 2.0 * np.pi * R_ring_out_hot * 0.02e-3
A_track_a_eff = A_end_gap + A_ring_film

alpha_carry = 1.0 / np.sqrt(1.0 - (1.0 / (1.0 + (clearance_lab / pitch_teeth))))
Cd_track_a = (0.62 / np.sqrt(N_teeth)) * alpha_carry

# Track B Geometry Parameters
chord_len = 140.0e-3
tip_clearance_b = 0.50e-3
N_holes = 22
d_hole = 2.20e-3
N_blades_equiv = int(np.round((2.0 * np.pi * 200.0e-3) / 35.0e-3))

A_over_tip_single = chord_len * tip_clearance_b
A_bleed_holes_single = N_holes * (np.pi * (d_hole / 2.0) ** 2)
A_track_b_annulus = N_blades_equiv * (A_over_tip_single + 0.35 * A_bleed_holes_single)
Cd_track_b = 0.78

mdot_A = np.array([compressible_mass_flux(P_in, P_out, T_in, Cd_track_a) * A_track_a_eff for P_in in P_in_sweep])
mdot_B = np.array([compressible_mass_flux(P_in, P_out, T_in, Cd_track_b) * A_track_b_annulus for P_in in P_in_sweep])
leakage_reduction_pct = (1.0 - (mdot_A / np.maximum(mdot_B, 1e-12))) * 100.0

idx_2 = np.argmin(np.abs(PR_sweep - 2.0))
print(f"Track A (PR=2.0): {mdot_A[idx_2]*1000:.3f} g/s")
print(f"Track B (PR=2.0, {N_blades_equiv}-blade annulus): {mdot_B[idx_2]*1000:.3f} g/s")
print(f"Leakage Reduction: {leakage_reduction_pct[idx_2]:.2f}%")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.2), dpi=150)
ax1.plot(PR_sweep, mdot_B * 1000.0, color="#2ca02c", linewidth=2.2, label="Track B: Open-Tip + 22 Holes (Annulus Eq.)")
ax1.plot(PR_sweep, mdot_A * 1000.0, color="#d62728", linewidth=2.2, label="Track A: Zero-Hole Shroud + Carbide Ring")
ax1.set_title("Tip-Leakage Mass Flow vs. Stage Pressure Ratio", fontsize=11, fontweight="bold")
ax1.set_xlabel("Pressure Ratio (P_in / P_out)")
ax1.set_ylabel("Leakage Mass Flow Rate [g/s]")
ax1.grid(True, linestyle="--", alpha=0.5)
ax1.legend(fontsize=9)

ax2.plot(PR_sweep, leakage_reduction_pct, color="#1f77b4", linewidth=2.2)
ax2.set_title("Leakage Suppression Advantage (Track A vs. Track B)", fontsize=11, fontweight="bold")
ax2.set_xlabel("Pressure Ratio (P_in / P_out)")
ax2.set_ylabel("Leakage Reduction [%]")
ax2.set_ylim(0, 100)
ax2.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("figures/tip_leakage_comparison.png", dpi=200)
