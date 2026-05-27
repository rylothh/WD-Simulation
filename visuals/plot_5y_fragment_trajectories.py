"""Plot representative fragment orbit trajectories after impact kicks over 5 years.

This uses a proxy mapping from orbit-by-orbit impact counts to eccentricity kicks,
so we can visualize likely post-impact fragment orbit families.
"""

from __future__ import annotations

import copy
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml

from wd1145_sim import run_simulation


def ellipse_points(a: float, e: float, n: int = 720) -> tuple[np.ndarray, np.ndarray]:
    f = np.linspace(0, 2 * np.pi, n)
    r = a * (1 - e * e) / (1 + e * np.cos(f))
    return r * np.cos(f), r * np.sin(f)


def main() -> None:
    cfg = yaml.safe_load(Path("config.yaml").read_text())
    cfg = copy.deepcopy(cfg)
    cfg["integration"]["duration_years"] = 5.0

    res = run_simulation(cfg)

    earth_diam_km = float(cfg["constants"].get("earth_diameter_km", 12742.0))
    wd_radius_km = 0.5 * earth_diam_km * float(cfg["system"].get("wd_diameter_earth", 1.0))

    # Base ring radius (midpoint of debris annulus) used for fragment initial circular orbits.
    r_ring_wd = 0.5 * (float(cfg["disk"]["r_in_wd_radii"]) + float(cfg["disk"]["r_out_wd_radii"]))

    # Select most active orbits as impact-trigger anchors.
    impacts = np.array(res.collision_counts)
    if impacts.sum() <= 0:
        top_idx = np.array([0, 1, 2])
    else:
        top_idx = np.argsort(impacts)[-12:]

    fig, ax = plt.subplots(figsize=(8, 8), dpi=180)
    ax.set_facecolor("#0b1020")
    fig.patch.set_facecolor("#0b1020")

    # Draw WD and ring guide.
    th = np.linspace(0, 2 * np.pi, 600)
    ax.plot(r_ring_wd * np.cos(th), r_ring_wd * np.sin(th), color="#f4c542", lw=1.2, alpha=0.9, label="Debris ring")
    ax.scatter([0], [0], s=28, color="#9ed0ff", label="WD1145")

    # Plot representative post-impact fragment orbits as lines.
    # Proxy rule: more impacts -> larger eccentricity spread.
    cmap = plt.get_cmap("plasma")
    max_imp = max(float(impacts.max()), 1.0)

    for rank, idx in enumerate(top_idx):
        imp = float(impacts[idx])
        # Map impacts to eccentricity in [0.02, 0.92].
        e = min(0.92, 0.02 + 0.90 * (imp / max_imp) ** 0.75)
        # Keep pericenter near ring while stretching apocenter outward.
        rp = r_ring_wd * (1.0 - 0.02 * (rank / max(1, len(top_idx) - 1)))
        a = rp / (1.0 - e)
        x, y = ellipse_points(a, e)

        color = cmap(rank / max(1, len(top_idx) - 1))
        ax.plot(x, y, color=color, lw=1.0, alpha=0.85)

    ax.set_title("5-year post-impact fragment trajectory proxy", color="white")
    ax.set_xlabel("x [WD radii]", color="white")
    ax.set_ylabel("y [WD radii]", color="white")
    ax.tick_params(colors="#c9d1ff")
    for spine in ax.spines.values():
        spine.set_color("#6b7399")
    ax.grid(color="#2a335a", alpha=0.35, linestyle="--", linewidth=0.7)
    ax.set_aspect("equal", adjustable="box")

    lim = r_ring_wd * 3.0
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)

    text = (
        f"Representative trajectories from top-{len(top_idx)} impact orbits\n"
        f"Total impacts in 5y: {int(impacts.sum())}; first-impact orbit: "
        f"{next((i+1 for i,v in enumerate(impacts) if v>0), None)}"
    )
    ax.text(0.02, 0.98, text, transform=ax.transAxes, va="top", color="white", fontsize=8)

    out = Path("visuals/wd1145_5y_fragment_trajectories.svg")
    fig.tight_layout()
    fig.savefig(out, facecolor=fig.get_facecolor())
    print(f"saved {out}")


if __name__ == "__main__":
    main()
