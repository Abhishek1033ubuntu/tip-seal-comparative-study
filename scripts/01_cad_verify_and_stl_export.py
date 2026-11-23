# Copyright (c) 2026 Abhishek Singh
# ORCID: https://orcid.org/0009-0004-6913-096X
# GitHub: https://github.com/Abhishek1033ubuntu
# AI Computational & Multi-Physics Support: Team Gemini (Google DeepMind)

import cadquery as cq
import numpy as np
import matplotlib.pyplot as plt

# 1. Load verified watertight STEP files from cad/
ring_shape = cq.importers.importStep("cad/track_a_carbide_piston_ring.step")
shroud_shape = cq.importers.importStep("cad/track_a_zero_hole_shroud.step")
tip_shape = cq.importers.importStep("cad/track_b_open_tip_22holes.step")

# 2. Export High-Resolution Watertight Surface Meshes (.stl)
models = [
    ("meshes/track_a_carbide_piston_ring.stl", ring_shape),
    ("meshes/track_a_zero_hole_shroud.stl", shroud_shape),
    ("meshes/track_b_open_tip_22holes.stl", tip_shape),
]

for fname, shape in models:
    cq.exporters.export(shape, fname, exportType="STL", tolerance=0.02, angularTolerance=0.1)
    solid = shape.val()
    verts, tris = solid.tessellate(0.02)
    print(f"Exported {fname}: {len(tris)} triangles | Watertight: {solid.isValid()} | Volume: {solid.Volume():.2f} mm^3")

# 3. Generate Native B-Rep Cross-Section & Orthographic Verification Sheet
fig = plt.figure(figsize=(16, 10), dpi=150)

# Panel 1: Track A Exact Radial Cross-Section (Y = 0 plane, X > 0)
ax1 = fig.add_subplot(2, 2, 1)
cut_plane = cq.Workplane("XZ").center(202.5, 13.0).rect(15.0, 30.0)
shroud_sec = shroud_shape.intersect(cut_plane)
ring_sec = ring_shape.intersect(cut_plane)

for edge in shroud_sec.edges().vals():
    pts = np.array([[p.x, p.z] for p in edge.sample(40)[0]])
    ax1.plot(pts[:, 0], pts[:, 1], color="#1f77b4", linewidth=1.8, label="Zero-Hole Shroud")

for edge in ring_sec.edges().vals():
    pts = np.array([[p.x, p.z] for p in edge.sample(40)[0]])
    ax1.plot(pts[:, 0], pts[:, 1], color="#d62728", linewidth=2.0, label="Carbide Piston Ring")

ax1.set_title("Track A: Exact Radial Cross-Section (Labyrinth & Ring Groove)", fontsize=11, fontweight="bold")
ax1.set_xlabel("Radial Coordinate R [mm]")
ax1.set_ylabel("Axial Coordinate Z [mm]")
ax1.set_xlim(197.5, 205.0)
ax1.set_ylim(-0.5, 25.5)
ax1.grid(True, linestyle="--", alpha=0.5)
handles, labels = ax1.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax1.legend(by_label.values(), by_label.keys(), loc="upper left", fontsize=9)

# Panel 2: Track A Ring End-Gap Detail (XY Plane)
ax2 = fig.add_subplot(2, 2, 2)
for edge in ring_shape.edges().vals():
    pts = np.array([[p.x, p.y] for p in edge.sample(120)[0]])
    mask = (pts[:, 0] > 201.5) & (np.abs(pts[:, 1]) < 6.0)
    if np.any(mask):
        ax2.plot(pts[mask, 0], pts[mask, 1], color="#d62728", linewidth=1.6)

ax2.set_title("Track A: Carbide Ring Thermal End-Gap Detail (XY Plane)", fontsize=11, fontweight="bold")
ax2.set_xlabel("X [mm]")
ax2.set_ylabel("Y [mm]")
ax2.set_aspect("equal")
ax2.grid(True, linestyle="--", alpha=0.5)

# Panel 3: Track B Top-Down View (22 Through-Holes Alignment)
ax3 = fig.add_subplot(2, 2, 3)
for edge in tip_shape.edges().vals():
    pts = np.array([[p.x, p.y] for p in edge.sample(50)[0]])
    ax3.plot(pts[:, 0], pts[:, 1], color="#2ca02c", linewidth=0.8, alpha=0.85)

ax3.set_title("Track B: Open-Tip Blade Profile & 22-Hole Array (XY Planform)", fontsize=11, fontweight="bold")
ax3.set_xlabel("Chordwise X [mm]")
ax3.set_ylabel("Pitchwise Y [mm]")
ax3.set_aspect("equal")
ax3.grid(True, linestyle="--", alpha=0.5)

# Panel 4: Track B Spanwise Elevation & Port Line (XZ Plane)
ax4 = fig.add_subplot(2, 2, 4)
for edge in tip_shape.edges().vals():
    pts = np.array([[p.x, p.z] for p in edge.sample(50)[0]])
    ax4.plot(pts[:, 0], pts[:, 1], color="#2ca02c", linewidth=0.8, alpha=0.85)

ax4.axhline(54.72, color="#ff7f0e", linestyle="--", linewidth=1.4, label="22-Port Axis (Z = 54.72 mm)")
ax4.set_title("Track B: Spanwise Elevation & Port Line (XZ Plane)", fontsize=11, fontweight="bold")
ax4.set_xlabel("Chordwise X [mm]")
ax4.set_ylabel("Spanwise Z [mm]")
ax4.legend(loc="lower right", fontsize=9)
ax4.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("figures/cad_verification_sheet.png", dpi=200)
