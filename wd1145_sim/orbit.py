"""Orbit utilities for the WD1145 interloper model."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class OrbitState:
    """Keplerian state in scalar element form for coplanar dynamics."""

    a_m: float
    e: float
    omega_rad: float = 0.0


def semimajor_axis_from_period(period_s: float, mu_m3_s2: float) -> float:
    """Return semimajor axis from orbital period and gravitational parameter."""

    return (mu_m3_s2 * period_s**2 / (4.0 * math.pi**2)) ** (1.0 / 3.0)


def periastron_distance(a_m: float, e: float) -> float:
    """Return periastron radius."""

    return a_m * (1.0 - e)


def vis_viva_speed(r_m: float, a_m: float, mu_m3_s2: float) -> float:
    """Return orbital speed via vis-viva equation."""

    return math.sqrt(mu_m3_s2 * (2.0 / r_m - 1.0 / a_m))


def radius_at_true_anomaly(a_m: float, e: float, f_rad: float) -> float:
    """Return radius at true anomaly for an ellipse."""

    p = a_m * (1.0 - e * e)
    return p / (1.0 + e * math.cos(f_rad))


def estimate_crossing_length(
    orbit: OrbitState,
    r_in_m: float,
    r_out_m: float,
    n_samples: int = 4096,
) -> float:
    """Estimate physical path length inside annulus via sampled true anomaly.

    The path is integrated from piecewise-linear segments in polar coordinates.
    """

    if n_samples < 8:
        n_samples = 8

    f_start = -math.pi
    f_end = math.pi
    total = 0.0
    prev_f = f_start
    prev_r = radius_at_true_anomaly(orbit.a_m, orbit.e, prev_f)
    prev_in = r_in_m <= prev_r <= r_out_m

    step = (f_end - f_start) / n_samples
    for i in range(1, n_samples + 1):
        f = f_start + i * step
        r = radius_at_true_anomaly(orbit.a_m, orbit.e, f)
        curr_in = r_in_m <= r <= r_out_m

        if prev_in or curr_in:
            x0, y0 = prev_r * math.cos(prev_f), prev_r * math.sin(prev_f)
            x1, y1 = r * math.cos(f), r * math.sin(f)
            seg = math.hypot(x1 - x0, y1 - y0)
            total += seg

        prev_f, prev_r, prev_in = f, r, curr_in

    return total


def estimate_relative_speed_at_annulus(
    orbit: OrbitState,
    r_in_m: float,
    r_out_m: float,
    mu_m3_s2: float,
) -> float:
    """Estimate relative speed between interloper and circularized fragment flow.

    Uses midpoint radius of the annulus as the comparison location.
    """

    r_mid = 0.5 * (r_in_m + r_out_m)
    v_interloper = vis_viva_speed(r_mid, orbit.a_m, mu_m3_s2)
    v_circular = math.sqrt(mu_m3_s2 / r_mid)
    return abs(v_interloper - v_circular)
