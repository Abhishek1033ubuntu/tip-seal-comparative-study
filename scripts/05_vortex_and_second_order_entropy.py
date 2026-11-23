# Copyright (c) 2026 Abhishek Singh
# ORCID: https://orcid.org/0009-0004-6913-096X
# GitHub: https://github.com/Abhishek1033ubuntu
# AI Computational & Multi-Physics Support: Team Gemini (Google DeepMind)

import os
import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# THERMODYNAMIC & STAGE OPERATING CONSTANTS
# ==============================================================================
T_IN_K = 800.0          # Inlet total temperature [K]
P_OUT_PA = 101325.0     # Downstream static pressure [Pa]
GAMMA = 1.35            # Specific heat ratio
R_GAS = 287.05          # Specific gas constant [J/(kg*K)]
CP = GAMMA * R_GAS / (GAMMA - 1.0)
K_MIX_TRACK_B = 1.65    # Tip-vortex + bleed-jet mixing multiplier on Track B

PR_SWEEP = np.linspace(1.05, 3.0, 60)
P_IN_SWEEP = PR_SWEEP * P_OUT_PA

def compressible_mass_flux(P0, P_back, T0, Cd):
    """Compressible orifice/clearance mass flux [kg/(s*m^2)] with choking check."""
    PR_crit = ((GAMMA + 1.0) / 2.0) ** (GAMMA / (GAMMA - 1.0))
    PR = P0 / P_back
    if PR >= PR_crit:
        factor = np.sqrt(GAMMA / (R_GAS * T0)) * ((2.0 / (GAMMA + 1.0)) ** ((GAMMA + 1.0) / (2.0 * (GAMMA - 1.0))))
        return Cd * P0 * factor
    term1 = (2.0 * GAMMA) / (R_GAS * T0 * (GAMMA - 1.0))
    term2 = (P_back / P0) ** (2.0 / GAMMA) - (P_back / P0) ** ((GAMMA + 1.0) / GAMMA)
    return Cd * P0 * np.sqrt(term1 * np.maximum(term2, 0.0))

def second_order_entropy_rate(mdot_leak, pr, t_in, k_vortex_mix=1.0):
    """
    Computes irreversible entropy generation rate [W/K] from:
      1. Irreversible throttling across the tip/seal pressure ratio:
         s_gen,throttle = mdot_leak * R * ln(PR)
      2. Second-order tip-vortex shear & bleed-jet mixing dissipation:
         T_exit * s_gen,II = (k_vortex_mix - 1.0) * mdot_leak * dh_s
    Returns (S_gen_total [W/K], S_gen_II_vortex [W/K]).
    """
    T_exit_s = t_in * (1.0 / pr) ** ((GAMMA - 1.0) / GAMMA)
    dh_s = CP * (t_in - T_exit_s)

    # First-order throttling entropy generation [W/K]
    s_gen_throttle = mdot_leak * R_GAS * np.log(pr)

    # Second-order aerodynamic vortex & shear mixing entropy generation [W/K]
    w_dissipated_ii = max(k_vortex_mix - 1.0, 0.0) * mdot_leak * dh_s
    s_gen_ii = w_dissipated_ii / max(T_exit_s, 1.0)

    return s_gen_throttle + s_gen_ii, s_gen_ii

# ==============================================================================
# TRACK A VS. TRACK B EFFECTIVE FLOW AREAS & DISCHARGE COEFFICIENTS
# ==============================================================================
R_casing = 204.85e-3
R_ring_out_hot = 204.701e-3
N_teeth = 6
pitch_teeth = 3.2e-3
clearance_lab = 0.35e-3
alpha_carry = 1.0 / np.sqrt(1.0 - (1.0 / (1.0 + (clearance_lab / pitch_teeth))))
Cd_track_a = (0.62 / np.sqrt(N_teeth)) * alpha_carry

A_track_a_base = (1.845e-3 * (R_casing - R_ring_out_hot)) + (2.0 * np.pi * R_ring_out_hot * 0.02e-3)
A_track_a_deg = (3.00e-3 * 0.50e-3) + (2.0 * np.pi * R_ring_out_hot * 0.08e-3)

chord_len = 140.0e-3
N_holes = 22
d_hole = 2.20e-3
N_blades_equiv = int(np.round((2.0 * np.pi * 200.0e-3) / 35.0e-3))
Cd_track_b = 0.78
A_track_b_ref = N_blades_equiv * (chord_len * 0.50e-3 + 0.35 * N_holes * (np.pi * (d_hole / 2.0) ** 2))

mdot_A_base = np.array([compressible_mass_flux(p, P_OUT_PA, T_IN_K, Cd_track_a) * A_track_a_base for p in P_IN_SWEEP])
mdot_A_deg = np.array([compressible_mass_flux(p, P_OUT_PA, T_IN_K, Cd_track_a) * A_track_a_deg for p in P_IN_SWEEP])
mdot_B_ref = np.array([compressible_mass_flux(p, P_OUT_PA, T_IN_K, Cd_track_b) * A_track_b_ref for p in P_IN_SWEEP])

# Compute total & second-order vortex/mixing entropy generation across PR sweep
S_tot_A_base, S_II_A_base = zip(*[second_order_entropy_rate(m, pr, T_IN_K, k_vortex_mix=1.02) for m, pr in zip(mdot_A_base, PR_SWEEP)])
S_tot_A_deg, S_II_A_deg = zip(*[second_order_entropy_rate(m, pr, T_IN_K, k_vortex_mix=1.08) for m, pr in zip(mdot_A_deg, PR_SWEEP)])
S_tot_B, S_II_B = zip(*[second_order_entropy_rate(m, pr, T_IN_K, k_vortex_mix=K_MIX_TRACK_B) for m, pr in zip(mdot_B_ref, PR_SWEEP)])

S_tot_A_base = np.array(S_tot_A_base)
S_tot_A_deg = np.array(S_tot_A_deg)
S_tot_B = np.array(S_tot_B)
S_II_B = np.array(S_II_B)

idx_2 = np.argmin(np.abs(PR_SWEEP - 2.0))
entropy_red_pct = (1.0 - S_tot_A_base[idx_2] / S_tot_B[idx_2]) * 100.0

print(f"=== Second-Order Entropy & Vortex Dissipation Benchmark (PR = 2.0, T_in = {T_IN_K:.0f} K) ===")
print(f"Track A (Baseline) Total S_gen   : {S_tot_A_base[idx_2]:.2f} W/K (Second-Order S_gen,II: {S_II_A_base[idx_2]:.2f} W/K)")
print(f"Track A (Degraded) Total S_gen   : {S_tot_A_deg[idx_2]:.2f} W/K (Second-Order S_gen,II: {S_II_A_deg[idx_2]:.2f} W/K)")
print(f"Track B (36-Blade) Total S_gen   : {S_tot_B[idx_2]:.2f} W/K (Second-Order Vortex/Jet S_gen,II: {S_II_B[idx_2]:.2f} W/K)")
print(f"Total Entropy Generation Reduction (Track A Baseline vs. Track B): {entropy_red_pct:.2f}%")

# ==============================================================================
# PLOT: TOTAL & SECOND-ORDER ENTROPY GENERATION VS. PRESSURE RATIO
# ==============================================================================
os.makedirs("figures", exist_ok=True)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.2), dpi=150)

ax1.plot(PR_SWEEP, S_tot_B, color="#2ca02c", linewidth=2.2, label="Track B: Total S_gen (Throttling + Vortex/Jet Mixing)")
ax1.plot(PR_SWEEP, S_II_B, color="#ff7f0e", linestyle="--", linewidth=2.0, label="Track B: Second-Order Vortex/Bleed S_gen,II")
ax1.plot(PR_SWEEP, S_tot_A_base, color="#d62728", linewidth=2.2, label="Track A: Baseline Labyrinth + Carbide Ring")
ax1.set_title("Irreversible Entropy Generation Rate vs. Pressure Ratio", fontsize=11, fontweight="bold")
ax1.set_xlabel("Pressure Ratio (P_in / P_out)")
ax1.set_ylabel("Entropy Generation Rate S_gen [W/K]")
ax1.grid(True, linestyle="--", alpha=0.5)
ax1.legend(fontsize=8.5)

# Right panel: Sensitivity of Track B Second-Order Vortex Entropy to Tip Clearance
for gap_mm in [0.25, 0.50, 1.00]:
    A_b_var = N_blades_equiv * (chord_len * (gap_mm * 1e-3) + 0.35 * N_holes * (np.pi * (d_hole / 2.0) ** 2))
    mdot_b_var = np.array([compressible_mass_flux(p, P_OUT_PA, T_IN_K, Cd_track_b) * A_b_var for p in P_IN_SWEEP])
    _, s_ii_var = zip(*[second_order_entropy_rate(m, pr, T_IN_K, k_vortex_mix=K_MIX_TRACK_B) for m, pr in zip(mdot_b_var, PR_SWEEP)])
    ax2.plot(PR_SWEEP, s_ii_var, linewidth=2.0, label=f"Track B Vortex S_gen,II (Gap = {gap_mm:.2f} mm)")

ax2.plot(PR_SWEEP, S_II_A_base, color="black", linestyle="--", linewidth=2.0, label="Track A Baseline S_gen,II (Suppressed)")
ax2.set_title("Second-Order Vortex & Bleed-Jet Entropy vs. Tip Gap", fontsize=11, fontweight="bold")
ax2.set_xlabel("Pressure Ratio (P_in / P_out)")
ax2.set_ylabel("Second-Order Entropy S_gen,II [W/K]")
ax2.grid(True, linestyle="--", alpha=0.5)
ax2.legend(fontsize=8.5)

plt.tight_layout()
plt.savefig("figures/vortex_second_order_entropy.png", dpi=200)
plt.show()
