"""Generate top-down WD1145 overview from config using perigee debris ring."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import yaml
from matplotlib.patches import Circle, Ellipse


def main() -> None:
    cfg = yaml.safe_load(Path("config.yaml").read_text())

    e = float(cfg["system"]["eccentricity"])
    inc = float(cfg["system"].get("inclination_deg", 0.0))
    period_days = float(cfg["system"]["period_days"])

    G = float(cfg["constants"]["G"])
    M_sun = float(cfg["constants"]["M_sun_kg"])
    day_s = float(cfg["constants"]["day_s"])
    mu = G * float(cfg["system"]["wd_mass_msun"]) * M_sun
    P = period_days * day_s
    a_m = (mu * P * P / (4 * math.pi**2)) ** (1 / 3)

    earth_diam_km = float(cfg["constants"].get("earth_diameter_km", 12742.0))
    wd_radius_km = 0.5 * earth_diam_km * float(cfg["system"].get("wd_diameter_earth", 1.0))

    a = a_m / (wd_radius_km * 1e3)
    rp = a * (1 - e)

    r_in = float(cfg["disk"]["r_in_wd_radii"])
    r_out = float(cfg["disk"]["r_out_wd_radii"])

    fig, ax = plt.subplots(figsize=(10, 10), dpi=180)
    ax.set_facecolor("#0b1020")
    fig.patch.set_facecolor("#0b1020")

    outer = Circle((0, 0), r_out, facecolor="#f4c542", alpha=0.2, edgecolor="#f4c542", lw=2)
    inner = Circle((0, 0), r_in, facecolor="#0b1020", edgecolor="#f4c542", lw=1.5)
    ax.add_patch(outer)
    ax.add_patch(inner)

    wd = Circle((0, 0), 1.0, facecolor="#9ed0ff", edgecolor="#d9eeff", lw=1.5)
    ax.add_patch(wd)

    center_x = -a * e
    orbit = Ellipse(
        (center_x, 0),
        width=2 * a,
        height=2 * a * math.sqrt(1 - e * e),
        edgecolor="#7aa6ff",
        facecolor="none",
        lw=2.0,
    )
    ax.add_patch(orbit)

    ax.annotate(
        "",
        xy=(rp + 20, 10),
        xytext=(rp - 40, 30),
        arrowprops={"arrowstyle": "->", "color": "#ff7f7f", "lw": 2},
    )

    ax.text(5, 8, "WD1145", color="white", fontsize=11)
    ax.text(r_out + 4, 8, "Perigee debris ring", color="#f4c542", fontsize=11)
    ax.text(center_x + a * 0.25, a * math.sqrt(1 - e * e) * 0.8, "Interloper orbit", color="#7aa6ff", fontsize=11)
    ax.text(
        0.02,
        0.98,
        f"P={period_days} d, i={inc:.1f}°, v_perigee={cfg['system']['perigee_speed_km_s']} km/s\n"
        f"Ring diameter=20 km, thickness=5 km",
        transform=ax.transAxes,
        va="top",
        color="white",
        fontsize=10,
    )

    lim = max(r_out * 1.25, 1200)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("WD1145 Top-Down Geometry (Perigee Ring)", color="white", pad=16)
    ax.set_xlabel("x [WD radii]", color="white")
    ax.set_ylabel("y [WD radii]", color="white")
    ax.tick_params(colors="#c9d1ff")
    for spine in ax.spines.values():
        spine.set_color("#6b7399")
    ax.grid(color="#2a335a", alpha=0.45, linestyle="--", linewidth=0.8)

    out = Path("visuals/wd1145_topdown_overview.svg")
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out, facecolor=fig.get_facecolor())
    print(f"saved {out}")


if __name__ == "__main__":
    main()
