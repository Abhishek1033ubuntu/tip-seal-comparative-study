# Copyright (c) 2026 Abhishek Singh
# ORCID: https://orcid.org/0009-0004-6913-096X
# GitHub: https://github.com/Abhishek1033ubuntu
# AI Computational & Multi-Physics Support: Team Gemini (Google DeepMind)

import numpy as np
import matplotlib.pyplot as plt

T_IN_K = 800.0
TARGET_PR = 2.0
TARGET_M_CORE_KG_S = 25.0
K_MIX_TRACK_B = 1.65

GAMMA = 1.35
R_GAS = 287.05

LEAK_TRACK_A_BASE = 6.008e-3
LEAK_TRACK_A_DEG = 24.12e-3
LEAK_TRACK_B_36BL = 799.071e-3

def isentropic_dh(pr, t_in, gamma=GAMMA, r_gas=R_GAS):
    cp = gamma * r_gas / (gamma - 1.0)
    return cp * t_in * (1.0 - (1.0 / pr) ** ((gamma - 1.0) / gamma))

dh_target = isentropic_dh(TARGET_PR, T_IN_K)
pr_scale = (TARGET_PR / 2.0) ** 0.5

cases = {
    "Track A (Baseline)": (LEAK_TRACK_A_BASE * pr_scale, 1.0),
    "Track A (Degraded)": (LEAK_TRACK_A_DEG * pr_scale, 1.0),
    "Track B (Bypass Only, k=1.0)": (LEAK_TRACK_B_36BL * pr_scale, 1.0),
    f"Track B (w/ Mixing, k={K_MIX_TRACK_B:.2f})": (LEAK_TRACK_B_36BL * pr_scale, K_MIX_TRACK_B),
}

print(f"Operating Point: PR = {TARGET_PR:.2f}, T_in = {T_IN_K:.1f} K, Core Flow = {TARGET_M_CORE_KG_S:.1f} kg/s")
print(f"Isentropic Enthalpy Drop (dh_s): {dh_target/1000.0:.2f} kJ/kg\n")

for name, (m_leak, k_mult) in cases.items():
    w_loss_kw = (m_leak * dh_target * k_mult) / 1000.0
    eff_pen_pct = (m_leak / (TARGET_M_CORE_KG_S + m_leak)) * 100.0 * k_mult
    print(f"  - {name:32s} | Leak: {m_leak*1000:7.2f} g/s | Power Loss: {w_loss_kw:6.2f} kW | Eff. Penalty: {eff_pen_pct:5.2f}%")

m_core_sweep = np.linspace(10.0, 60.0, 200)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.2), dpi=150)

pr_sweep = np.linspace(1.2, 3.0, 60)
for name, (m_leak_ref, k_mult) in cases.items():
    scale_curve = (pr_sweep / 2.0) ** 0.5
    dh_curve = np.array([isentropic_dh(p, T_IN_K) for p in pr_sweep])
    w_curve_kw = (m_leak_ref * scale_curve) * dh_curve * k_mult / 1000.0
    ax1.plot(pr_sweep, w_curve_kw, linewidth=2.0, label=name)

ax1.axvline(TARGET_PR, color="gray", linestyle=":", linewidth=1.2, label=f"Target PR = {TARGET_PR:.1f}")
ax1.set_title(f"Stage Power Loss vs. Pressure Ratio ({T_IN_K:.0f} K)", fontsize=11, fontweight="bold")
ax1.set_xlabel("Pressure Ratio (P_in / P_out)")
ax1.set_ylabel("Lost Stage Power [kW]")
ax1.grid(True, linestyle="--", alpha=0.5)
ax1.legend(fontsize=8)

for name, (m_leak_ref, k_mult) in cases.items():
    m_leak_pt = m_leak_ref * ((TARGET_PR / 2.0) ** 0.5)
    pen_curve = (m_leak_pt / (m_core_sweep + m_leak_pt)) * 100.0 * k_mult
    ax2.plot(m_core_sweep, pen_curve, linewidth=2.0, label=name)

ax2.axvline(TARGET_M_CORE_KG_S, color="gray", linestyle=":", linewidth=1.2, label=f"Core = {TARGET_M_CORE_KG_S:.0f} kg/s")
ax2.set_title(f"Efficiency Penalty vs. Core Flow (PR = {TARGET_PR:.1f})", fontsize=11, fontweight="bold")
ax2.set_xlabel("Core Mass Flow Rate [kg/s]")
ax2.set_ylabel("Stage Efficiency Penalty [%]")
ax2.grid(True, linestyle="--", alpha=0.5)
ax2.legend(fontsize=8)

plt.tight_layout()
plt.savefig("figures/stage_leakage_power_loss_refined.png", dpi=200)
