"""Plot yearly overhead fragment-scatter proxy for a 5-year run."""

from __future__ import annotations

import copy
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml

from wd1145_sim import run_simulation


def main() -> None:
    cfg = yaml.safe_load(Path("config.yaml").read_text())
    cfg["integration"]["duration_years"] = 5.0

    res = run_simulation(copy.deepcopy(cfg))
    impacts = np.array(res.collision_counts, dtype=float)
    period_days = np.array(res.period_history_days, dtype=float)

    # Build cumulative time axis with period decay.
    t_days = np.cumsum(period_days)
    t_years = t_days / 365.25

    years = [1, 2, 3, 4, 5]
    fig, axes = plt.subplots(1, 5, figsize=(18, 4), dpi=160, sharex=True, sharey=True)

    rng = np.random.default_rng(42)
    n_points = 4000

    for i, year in enumerate(years):
        ax = axes[i]
        mask = t_years <= year
        cum_impacts = impacts[mask].sum() if mask.any() else 0.0

        # Proxy: larger cumulative impacts -> larger angular/radial spread.
        spread = min(0.35, 0.02 + cum_impacts / 300000.0)
        base_r = 1.0
        theta = rng.uniform(0, 2 * np.pi, size=n_points)
        r = base_r + rng.normal(0.0, spread, size=n_points)
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        ax.scatter(x, y, s=1, alpha=0.25, color="#f4c542")
        ax.scatter([0], [0], s=20, color="#9ed0ff")
        ax.set_title(f"Year {year}\nCum impacts={int(cum_impacts)}", fontsize=9)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(alpha=0.2)

    fig.suptitle("WD1145 5-year Fragment Scatter Proxy (Overhead)")
    plt.tight_layout()

    out = Path("visuals/wd1145_5y_fragment_scatter_proxy.svg")
    fig.savefig(out)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
