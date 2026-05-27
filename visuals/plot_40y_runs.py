"""Run 3 simulations over 40 years and plot impacts per orbit and cumulative impacts."""

from __future__ import annotations

import copy
from pathlib import Path

import matplotlib.pyplot as plt
import yaml

from wd1145_sim import run_simulation


def main() -> None:
    cfg = yaml.safe_load(Path("config.yaml").read_text())
    cfg["integration"]["duration_years"] = 40.0

    seeds = [12001, 12002, 12003]
    fig1, ax1 = plt.subplots(figsize=(10, 5), dpi=150)
    fig2, ax2 = plt.subplots(figsize=(10, 5), dpi=150)

    summary_lines = []

    for seed in seeds:
        c = copy.deepcopy(cfg)
        c["integration"]["random_seed"] = seed
        res = run_simulation(c)

        impacts = res.collision_counts
        cum = []
        s = 0
        for v in impacts:
            s += v
            cum.append(s)

        orbits = list(range(1, len(impacts) + 1))
        ax1.plot(orbits, impacts, label=f"seed {seed}")
        ax2.plot(orbits, cum, label=f"seed {seed}")

        summary_lines.append(
            f"seed={seed}, orbits={len(impacts)}, total_impacts={sum(impacts)}, mean_per_orbit={sum(impacts)/len(impacts):.3f}"
        )

    ax1.set_title("WD1145 40-year runs: impacts per orbit")
    ax1.set_xlabel("Orbit index")
    ax1.set_ylabel("Impacts")
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    ax2.set_title("WD1145 40-year runs: cumulative impacts")
    ax2.set_xlabel("Orbit index")
    ax2.set_ylabel("Cumulative impacts")
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    out_dir = Path("visuals")
    out_dir.mkdir(parents=True, exist_ok=True)
    fig1.tight_layout()
    fig2.tight_layout()
    p1 = out_dir / "wd1145_40y_impacts_per_orbit.svg"
    p2 = out_dir / "wd1145_40y_cumulative_impacts.svg"
    fig1.savefig(p1)
    fig2.savefig(p2)

    txt = out_dir / "wd1145_40y_run_summary.txt"
    txt.write_text("\n".join(summary_lines) + "\n")

    print(f"saved {p1}")
    print(f"saved {p2}")
    print(f"saved {txt}")
    for line in summary_lines:
        print(line)


if __name__ == "__main__":
    main()
