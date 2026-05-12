"""Generate non-binary/vector and PNG views of inclined interloper orbit vs debris ring."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml


def main() -> None:
    cfg = yaml.safe_load(Path("config.yaml").read_text())

    e = float(cfg["system"]["eccentricity"])
    inc = math.radians(float(cfg["system"].get("inclination_deg", 0.0)))

    G = float(cfg["constants"]["G"])
    M_sun = float(cfg["constants"]["M_sun_kg"])
    day_s = float(cfg["constants"]["day_s"])
    mu = G * float(cfg["system"]["wd_mass_msun"]) * M_sun
    P = float(cfg["system"]["period_days"]) * day_s
    a = (mu * P * P / (4 * math.pi**2)) ** (1 / 3)

    earth_diam_km = float(cfg["constants"].get("earth_diameter_km", 12742.0))
    wd_radius_km = 0.5 * earth_diam_km * float(cfg["system"].get("wd_diameter_earth", 1.0))

    rin = float(cfg["disk"]["r_in_wd_radii"])
    rout = float(cfg["disk"]["r_out_wd_radii"])

    # Parametric interloper orbit with WD at focus, projected to sky plane.
    f = np.linspace(0, 2 * np.pi, 3000)
    r = a * (1 - e * e) / (1 + e * np.cos(f))
    x = r * np.cos(f)
    y = r * np.sin(f) * np.cos(inc)

    # Convert to WD-radii units for display.
    x_wd = x / (wd_radius_km * 1e3)
    y_wd = y / (wd_radius_km * 1e3)

    th = np.linspace(0, 2 * np.pi, 1000)
    ring_in_x = rin * np.cos(th)
    ring_in_y = rin * np.sin(th)
    ring_out_x = rout * np.cos(th)
    ring_out_y = rout * np.sin(th)

    fig, ax = plt.subplots(figsize=(10, 10), dpi=180)
    ax.set_facecolor("#0b1020")
    fig.patch.set_facecolor("#0b1020")

    ax.fill_between(ring_out_x, ring_out_y, -ring_out_y, color="#f4c542", alpha=0.15)
    ax.plot(ring_in_x, ring_in_y, color="#f4c542", lw=1.6, label="Debris ring inner/outer")
    ax.plot(ring_out_x, ring_out_y, color="#f4c542", lw=1.6)
    ax.plot(x_wd, y_wd, color="#7aa6ff", lw=2.2, label="Interloper orbit (inclined projection)")

    ax.scatter([0], [0], color="#9ed0ff", s=40, label="WD1145")

    rp = a * (1 - e) / (wd_radius_km * 1e3)
    ra = a * (1 + e) / (wd_radius_km * 1e3)
    ax.text(0.02, 0.98,
            f"P={cfg['system']['period_days']} d, e={e:.4f}, i={math.degrees(inc):.1f}°\n"
            f"Perigee speed target={cfg['system']['perigee_speed_km_s']} km/s\n"
            f"rp≈{rp:.1f} WD radii, ra≈{ra:.1f} WD radii",
            transform=ax.transAxes, va="top", color="white", fontsize=10)

    lim = max(rout * 1.1, np.nanmax(np.abs(x_wd)) * 0.12)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(color="#2a335a", alpha=0.4, linestyle="--", linewidth=0.8)
    ax.tick_params(colors="#c9d1ff")
    for sp in ax.spines.values():
        sp.set_color("#6b7399")
    ax.set_title("WD1145 Interloper Orbit vs Debris Ring (PNG)", color="white")
    ax.set_xlabel("x [WD radii]", color="white")
    ax.set_ylabel("y [WD radii]", color="white")
    ax.legend(facecolor="#1a2242", edgecolor="#6b7399", labelcolor="white")

    out_dir = Path("visuals")
    out_dir.mkdir(parents=True, exist_ok=True)
    png_out = out_dir / "wd1145_inclined_orbit_ring.png"
    svg_out = out_dir / "wd1145_inclined_orbit_ring.svg"
    plt.tight_layout()
    plt.savefig(png_out, facecolor=fig.get_facecolor())
    plt.savefig(svg_out, facecolor=fig.get_facecolor())
    print(f"saved {png_out}")
    print(f"saved {svg_out}")


if __name__ == "__main__":
    main()
