"""Collision-rate and impulse approximations for the interloper model."""

from __future__ import annotations

import math
import random


def expected_collisions(
    fragment_surface_density_m2: float,
    crossing_length_m: float,
    interloper_radius_m: float,
    activity_multiplier: float,
) -> float:
    """Compute expected number of collisions as an optical-depth proxy."""

    swept_area = 2.0 * interloper_radius_m * crossing_length_m
    return fragment_surface_density_m2 * swept_area * max(1.0, activity_multiplier)


def sample_poisson(lam: float, rng: random.Random) -> int:
    """Sample Poisson variates with stable behavior for large lambda.

    - For lambda < 30: exact Knuth algorithm.
    - For lambda >= 30: Gaussian approximation N(lambda, sqrt(lambda)), clipped >= 0.
    """

    if lam <= 0.0:
        return 0

    if lam < 30.0:
        limit = math.exp(-lam)
        k = 0
        p = 1.0
        while p > limit:
            k += 1
            p *= rng.random()
        return k - 1

    val = int(round(rng.gauss(lam, math.sqrt(lam))))
    return max(0, val)


def impulsive_orbit_kick(
    collisions: int,
    impulse_efficiency: float,
    a_m: float,
    e: float,
    relative_speed_m_s: float,
) -> tuple[float, float]:
    """Return simplified orbital element kick from cumulative collisions.

    Kick magnitude increases with collision count and relative speed scale.
    """

    speed_scale = max(relative_speed_m_s / 1.0e5, 1e-6)
    scale = collisions * impulse_efficiency * speed_scale
    delta_a = -scale * 1.0e-6 * a_m
    delta_e = -scale * 1.0e-6 * max(0.0, e)
    return delta_a, delta_e
