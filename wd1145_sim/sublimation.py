"""Effective sublimation terms for orbit drift in the WD1145 model."""

from __future__ import annotations


def sublimation_drift(
    dt_years: float,
    da_dt_au_per_yr: float,
    de_dt_per_yr: float,
    au_m: float,
) -> tuple[float, float]:
    """Return (delta_a_m, delta_e) from effective sublimation drift rates."""

    return da_dt_au_per_yr * au_m * dt_years, de_dt_per_yr * dt_years
