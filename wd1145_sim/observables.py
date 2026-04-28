"""Synthetic dip-activity observables derived from collision activity."""

from __future__ import annotations

import math


def optical_depth_proxy(activity_level: float, collision_count: int) -> float:
    """Toy optical-depth proxy from activity and collision multiplicity."""

    return max(0.0, 0.01 * collision_count * (1.0 + activity_level))


def dip_depth_index(tau: float) -> float:
    """Map optical depth proxy to dip depth index D=1-exp(-tau)."""

    return 1.0 - math.exp(-tau)
