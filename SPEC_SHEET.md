# WD1145 Simulation Spec Sheet (v2)

## Purpose
Build a Monte Carlo simulation of a high-eccentricity interloper crossing a flat,
coplanar Roche debris annulus around WD1145, estimating:

1. impact frequency per interloper orbit,
2. orbits-to-first-impact,
3. multi-year post-collision activity windows,
4. orbital element drift from collisions + sublimation,
5. dip-like observable proxies.

## Baseline assumptions
- WD mass: 0.6 solar masses.
- Interloper period: 124 days.
- Interloper eccentricity: 0.975.
- Interloper mass: 0.00016 Earth masses (Ceres-scale proxy).
- Disk geometry: flat, coplanar, no thickness profile.
- Initial debris can be specified either as a single count or as size bins.
- Default bins: 5 million at 1 km diameter, 10 million at 500 m diameter,
  and 20 million at 50 m diameter.
- Initial debris: 15,000,000 fragments.
- Fragment diameter range: 2 to 12 meters.
- Collision cross-section: geometric.
- Post-impact activity scatter window: ~4.5 years.
- Extra non-gravitational term: effective sublimation drift.

## Core model blocks
- `orbit.py`: Kepler helpers, sampled true-anomaly annulus crossing length,
  and annulus relative-speed estimator.
- `disk_state.py`: statistical fragment population and activity decay.
- `collisions.py`: expected collisions, robust Poisson sampler, impulsive orbital kick.
- `sublimation.py`: smooth orbital drift term.
- `observables.py`: optical depth and dip depth index proxies.
- `simulate.py`: orbit-by-orbit Monte Carlo driver with lambda and velocity histories,
  including mixed-size fragment-bin handling with cross-section weighting.
- `simulate.py`: orbit-by-orbit Monte Carlo driver with lambda and velocity histories.

## Primary outputs
- Collision count per orbit.
- Time-to-first-impact distribution across Monte Carlo runs.
- Semi-major axis and eccentricity history.
- Expected-collision (`lambda`) history.
- Relative-speed history at annulus crossings.
- Dip depth activity index time series.

## Validation and testing
- Unit tests validate:
  - semimajor-axis scale from period,
  - positive crossing length when annulus brackets periastron,
  - non-negative relative speed,
  - output-series length consistency from `run_simulation`.

## Known v2 simplifications
- 2D annulus treatment with no explicit vertical structure.
- Crossing length computed by dense sampling, not analytic root solving.
- Statistical PSD evolution instead of explicit collisional cascade tree.
- Dip outputs are proxies, not radiative-transfer light curves.

## Near-term upgrade path
1. Analytic annulus boundary crossing in true anomaly (replace sampled geometry).
2. Spatially resolved azimuthal density map and disk gaps.
3. Explicit cascade branching and debris size-bin transfer matrix.
4. Observer-frame light-curve synthesis (cadence + noise model).

## Sweep utility
- `sweep.py` runs multi-seed parameter sweeps over `initial_fragment_count` and writes
  `sweep_results.csv` with:
  - hit fraction (runs with >=1 impact),
  - median total collisions,
  - median first-impact orbit.

