import math
import unittest

from wd1145_sim.orbit import (
    OrbitState,
    estimate_crossing_length,
    estimate_relative_speed_at_annulus,
    periastron_distance,
    semimajor_axis_from_period,
)


class OrbitTests(unittest.TestCase):
    def test_semimajor_axis_from_period_reasonable(self):
        g = 6.67430e-11
        m_sun = 1.98847e30
        mu = g * 0.6 * m_sun
        p = 124 * 86400
        a = semimajor_axis_from_period(p, mu)
        # ~0.41 AU from prior estimate
        self.assertTrue(0.35 < a / 1.495978707e11 < 0.5)

    def test_crossing_length_positive_when_annulus_contains_periastron(self):
        orbit = OrbitState(a_m=1.0e9, e=0.5)
        rp = periastron_distance(orbit.a_m, orbit.e)
        length = estimate_crossing_length(orbit, rp * 0.95, rp * 1.05)
        self.assertGreater(length, 0.0)

    def test_relative_speed_non_negative(self):
        g = 6.67430e-11
        m_sun = 1.98847e30
        mu = g * 0.6 * m_sun
        orbit = OrbitState(a_m=2.0e9, e=0.3)
        v_rel = estimate_relative_speed_at_annulus(orbit, 1.0e9, 1.2e9, mu)
        self.assertGreaterEqual(v_rel, 0.0)


if __name__ == "__main__":
    unittest.main()
