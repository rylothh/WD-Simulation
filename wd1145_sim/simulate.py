"""Simulation driver for WD1145 interloper/debris interactions."""

from __future__ import annotations

import random
from dataclasses import dataclass

from .collisions import expected_collisions, impulsive_orbit_kick, sample_poisson
from .disk_state import DiskState, decay_activity, update_psd_slope
from .observables import dip_depth_index, optical_depth_proxy
from .orbit import (
    OrbitState,
    estimate_crossing_length,
    estimate_relative_speed_at_annulus,
    semimajor_axis_from_period,
)
from .sublimation import sublimation_drift


@dataclass
class SimulationResult:
    """Container for simulation outputs."""

    collision_counts: list[int]
    dip_depth_index: list[float]
    a_history_m: list[float]
    e_history: list[float]
    lambda_history: list[float]
    relative_speed_km_s: list[float]



def run_simulation(config: dict) -> SimulationResult:
    """Run one Monte Carlo realization aligned to `config.yaml`."""

    rng = random.Random(config["integration"]["random_seed"])

    G = float(config["constants"]["G"])
    M_sun = float(config["constants"]["M_sun_kg"])
    au_m = float(config["constants"]["au_m"])
    period_days = float(config["system"]["period_days"])
    period_s = period_days * float(config["constants"]["day_s"])
    duration_years = config["integration"]["duration_years"]

    n_orbits = max(1, int(duration_years * 365.25 / period_days))
    dt_years = period_days / 365.25

    wd_radius_km = config["disk"]["wd_radius_km"]
    r_in_m = config["disk"]["r_in_wd_radii"] * wd_radius_km * 1e3
    r_out_m = config["disk"]["r_out_wd_radii"] * wd_radius_km * 1e3

    mu = G * float(config["system"]["wd_mass_msun"]) * M_sun
    a0 = semimajor_axis_from_period(period_s, mu)
    orbit = OrbitState(a_m=a0, e=float(config["system"]["eccentricity"]))

    disk = DiskState(
        fragment_count=config["disk"]["initial_fragment_count"],
        psd_slope_q=config["disk"]["psd_slope_q0"],
    )

    interloper_radius_m = config["system"]["interloper_radius_km"] * 1e3
    annulus_area_m2 = 3.141592653589793 * (r_out_m**2 - r_in_m**2)
    frag_surface_density = disk.fragment_count / max(annulus_area_m2, 1.0)

    collision_counts: list[int] = []
    dip_index: list[float] = []
    a_hist: list[float] = [orbit.a_m]
    e_hist: list[float] = [orbit.e]
    lambda_hist: list[float] = []
    rel_speeds: list[float] = []

    for _ in range(n_orbits):
        crossing_length_m = estimate_crossing_length(orbit, r_in_m, r_out_m)
        v_rel_m_s = estimate_relative_speed_at_annulus(orbit, r_in_m, r_out_m, mu)
        rel_speeds.append(v_rel_m_s / 1e3)

        lam = expected_collisions(
            fragment_surface_density_m2=frag_surface_density,
            crossing_length_m=crossing_length_m,
            interloper_radius_m=interloper_radius_m,
            activity_multiplier=1.0 + disk.activity_level,
        )
        lambda_hist.append(lam)
        n_coll = sample_poisson(lam, rng)
        collision_counts.append(n_coll)

        da_imp, de_imp = impulsive_orbit_kick(
            collisions=n_coll,
            impulse_efficiency=config["collision"]["impulse_efficiency"],
            a_m=orbit.a_m,
            e=orbit.e,
            relative_speed_m_s=v_rel_m_s,
        )

        da_sub, de_sub = sublimation_drift(
            dt_years=dt_years,
            da_dt_au_per_yr=float(config["sublimation"]["da_dt_scale_au_per_yr"]),
            de_dt_per_yr=float(config["sublimation"]["de_dt_scale_per_yr"]),
            au_m=au_m,
        )

        orbit.a_m = max(1e6, orbit.a_m + da_imp + da_sub)
        orbit.e = min(0.9999, max(0.0, orbit.e + de_imp + de_sub))

        if n_coll > 0:
            disk.activity_level = min(
                config["activity"]["local_rate_boost_initial"],
                disk.activity_level + 0.5,
            )
        disk.activity_level = decay_activity(
            disk.activity_level,
            dt_years,
            config["activity"]["decay_tau_years"],
        )
        stochastic = rng.gauss(0.0, config["activity"]["psd_stochastic_sigma"])
        disk.psd_slope_q = update_psd_slope(
            config["disk"]["psd_slope_q0"],
            disk.activity_level,
            stochastic,
        )

        tau = optical_depth_proxy(disk.activity_level, n_coll)
        dip_index.append(dip_depth_index(tau))

        a_hist.append(orbit.a_m)
        e_hist.append(orbit.e)

    return SimulationResult(
        collision_counts=collision_counts,
        dip_depth_index=dip_index,
        a_history_m=a_hist,
        e_history=e_hist,
        lambda_history=lambda_hist,
        relative_speed_km_s=rel_speeds,
    )
