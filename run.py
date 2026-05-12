"""CLI entry point for WD1145 simulation."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from wd1145_sim import run_simulation


if __name__ == "__main__":
    config_path = Path("config.yaml")
    config = yaml.safe_load(config_path.read_text())
    result = run_simulation(config)

    first_impact_orbit = next(
        (idx for idx, n in enumerate(result.collision_counts, start=1) if n > 0),
        None,
    )

    out = {
        "num_orbits": len(result.collision_counts),
        "total_collisions": int(sum(result.collision_counts)),
        "mean_collisions_per_orbit": (
            sum(result.collision_counts) / max(1, len(result.collision_counts))
        ),
        "first_impact_orbit": first_impact_orbit,
        "mean_lambda": sum(result.lambda_history) / max(1, len(result.lambda_history)),
        "mean_relative_speed_km_s": sum(result.relative_speed_km_s)
        / max(1, len(result.relative_speed_km_s)),
        "mean_dip_index": sum(result.dip_depth_index) / max(1, len(result.dip_depth_index)),
        "final_a_m": result.a_history_m[-1],
        "final_e": result.e_history[-1],
    }
    print(json.dumps(out, indent=2))
