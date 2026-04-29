"""Generate a top-down WD1145 overview image."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse


def main() -> None:
    # Scaled units in WD radii for visual clarity.
    wd_r = 1.0
    r_in = 175.30
    r_out = 175.80

    # Orbit chosen so rp=a(1-e) ~ 175.5 WD radii.
    a = 7020.0
    e = 0.975
    rp = a * (1 - e)

    fig, ax = plt.subplots(figsize=(10, 10), dpi=180)
    ax.set_facecolor("#0b1020")
    fig.patch.set_facecolor("#0b1020")

    outer = Circle((0, 0), r_out, facecolor="#f4c542", alpha=0.25, edgecolor="#f4c542", lw=2)
    inner = Circle((0, 0), r_in, facecolor="#0b1020", edgecolor="#f4c542", lw=1.5)
    ax.add_patch(outer)
    ax.add_patch(inner)

    wd = Circle((0, 0), wd_r, facecolor="#9ed0ff", edgecolor="#d9eeff", lw=1.5)
    ax.add_patch(wd)

    center_x = -a * e
    orbit = Ellipse(
        (center_x, 0),
        width=2 * a,
        height=2 * a * math.sqrt(1 - e * e),
        edgecolor="#7aa6ff",
        facecolor="none",
        lw=2.2,
    )
    ax.add_patch(orbit)

    ax.annotate(
        "",
        xy=(rp + 20, 15),
        xytext=(rp - 40, 30),
        arrowprops={"arrowstyle": "->", "color": "#ff7f7f", "lw": 2},
    )

    ax.text(4, 6, "WD1145", color="white", fontsize=11)
    ax.text(r_out + 8, 10, "Roche debris annulus", color="#f4c542", fontsize=11)
    ax.text(center_x + a * 0.2, a * math.sqrt(1 - e * e) * 0.9, "Interloper orbit", color="#7aa6ff", fontsize=11)
    ax.text(rp + 10, -22, f"Periastron ≈ {rp:.1f} WD radii", color="#ffb3b3", fontsize=10)

    lim = 260
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("WD1145 Top-Down Geometry: White Dwarf, Debris Disk, and Interloper Path", color="white", pad=16)
    ax.set_xlabel("x [WD radii]", color="white")
    ax.set_ylabel("y [WD radii]", color="white")
    ax.tick_params(colors="#c9d1ff")
    for spine in ax.spines.values():
        spine.set_color("#6b7399")
    ax.grid(color="#2a335a", alpha=0.45, linestyle="--", linewidth=0.8)

    out_dir = Path("visuals")
    out_dir.mkdir(parents=True, exist_ok=True)
    png_out = out_dir / "wd1145_topdown_overview.png"
    svg_out = out_dir / "wd1145_topdown_overview.svg"

    plt.tight_layout()
    plt.savefig(png_out, facecolor=fig.get_facecolor())
    plt.savefig(svg_out, facecolor=fig.get_facecolor())
    print(f"saved {png_out}")
    print(f"saved {svg_out}")


if __name__ == "__main__":
    main()
