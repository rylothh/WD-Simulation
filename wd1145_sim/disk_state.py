"""Disk population and activity-state helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DiskState:
    """Statistical disk state for Monte Carlo simulation."""

    fragment_count: int
    psd_slope_q: float
    activity_level: float = 0.0


def decay_activity(activity_level: float, dt_years: float, tau_years: float) -> float:
    """Exponential decay of post-collision activity."""

    if tau_years <= 0:
        return 0.0
    return activity_level * (2.718281828459045 ** (-dt_years / tau_years))


def update_psd_slope(base_q: float, activity_level: float, stochastic_term: float) -> float:
    """Return PSD slope under active-scatter conditions."""

    return base_q + activity_level * stochastic_term
