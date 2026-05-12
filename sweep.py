"""Parameter sweep utility for WD1145 Monte Carlo simulation."""

from __future__ import annotations

import argparse
import copy
import csv
import statistics
from pathlib import Path

import yaml

from wd1145_sim import run_simulation


def first_impact_orbit(collision_counts: list[int]) -> int | None:
    """Return 1-indexed first orbit with >=1 collision, otherwise None."""

    for idx, count in enumerate(collision_counts, start=1):
        if count > 0:
            return idx
    return None


def run_grid(
    base_config: dict,
    fragment_counts: list[int],
    seeds: list[int],
) -> list[dict]:
    """Run realizations for each fragment-count value and summarize outcomes."""

    rows: list[dict] = []

    for n_frag in fragment_counts:
        total_collisions: list[int] = []
        first_impacts: list[int] = []
        hit_runs = 0

        for seed in seeds:
            cfg = copy.deepcopy(base_config)
            cfg["disk"]["initial_fragment_count"] = int(n_frag)
            cfg["integration"]["random_seed"] = int(seed)

            result = run_simulation(cfg)
            total = int(sum(result.collision_counts))
            first = first_impact_orbit(result.collision_counts)

            total_collisions.append(total)
            if first is not None:
                first_impacts.append(first)
                hit_runs += 1

        hit_fraction = hit_runs / max(1, len(seeds))
        median_total = statistics.median(total_collisions) if total_collisions else 0.0
        median_first = statistics.median(first_impacts) if first_impacts else None

        rows.append(
            {
                "initial_fragment_count": n_frag,
                "runs": len(seeds),
                "hit_fraction": hit_fraction,
                "median_total_collisions": median_total,
                "median_first_impact_orbit": median_first,
            }
        )

    return rows


def parse_int_list(value: str) -> list[int]:
    """Parse comma-separated integers."""

    return [int(v.strip()) for v in value.split(",") if v.strip()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WD1145 parameter sweep runner")
    parser.add_argument("--config", default="config.yaml", help="Path to config YAML")
    parser.add_argument(
        "--fragment-counts",
        default="15000000,30000000,60000000,120000000",
        help="Comma-separated initial fragment counts",
    )
    parser.add_argument(
        "--seeds",
        default="1145,1146,1147,1148,1149,1150,1151,1152,1153,1154",
        help="Comma-separated random seeds",
    )
    parser.add_argument(
        "--output",
        default="sweep_results.csv",
        help="Output CSV path",
    )

    args = parser.parse_args()

    config = yaml.safe_load(Path(args.config).read_text())
    fragment_counts = parse_int_list(args.fragment_counts)
    seeds = parse_int_list(args.seeds)

    rows = run_grid(config, fragment_counts, seeds)

    out_path = Path(args.output)
    with out_path.open("w", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "initial_fragment_count",
                "runs",
                "hit_fraction",
                "median_total_collisions",
                "median_first_impact_orbit",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {out_path}")
    for row in rows:
        print(row)
