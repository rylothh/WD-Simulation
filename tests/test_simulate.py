import unittest

from wd1145_sim.simulate import run_simulation


class SimulateTests(unittest.TestCase):
    def _config(self):
        return {
            "constants": {
                "G": 6.67430e-11,
                "M_sun_kg": 1.98847e30,
                "M_earth_kg": 5.9722e24,
                "day_s": 86400,
                "au_m": 1.495978707e11,
            },
            "system": {
                "wd_mass_msun": 0.6,
                "period_days": 124.0,
                "eccentricity": 0.975,
                "interloper_mass_mearth": 0.00016,
                "interloper_radius_km": 470.0,
            },
            "disk": {
                "wd_radius_km": 8750.0,
                "r_in_wd_radii": 97.0,
                "r_out_wd_radii": 101.0,
                "initial_fragment_count": 100000,
                "psd_slope_q0": 3.0,
            },
            "collision": {"impulse_efficiency": 0.05},
            "activity": {
                "local_rate_boost_initial": 4.0,
                "decay_tau_years": 2.0,
                "psd_stochastic_sigma": 0.25,
            },
            "sublimation": {
                "da_dt_scale_au_per_yr": -1e-6,
                "de_dt_scale_per_yr": -2e-6,
            },
            "integration": {"duration_years": 2.0, "random_seed": 7},
        }

    def test_run_simulation_lengths_match(self):
        result = run_simulation(self._config())
        n = len(result.collision_counts)
        self.assertEqual(len(result.lambda_history), n)
        self.assertEqual(len(result.relative_speed_km_s), n)
        self.assertEqual(len(result.dip_depth_index), n)
        self.assertEqual(len(result.a_history_m), n + 1)
        self.assertEqual(len(result.e_history), n + 1)


if __name__ == "__main__":
    unittest.main()
