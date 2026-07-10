import unittest
import numpy as np
from firmware.aethel_3d_torus_engine import Aethel3DTorusEngine

class TestAethel3DTorusEngine(unittest.TestCase):
    def setUp(self):
        """Initialize a fresh testing instance before each validation check."""
        self.engine = Aethel3DTorusEngine(grid_size=8)

    def test_torus_coordinate_wrapping(self):
        """Verifies that floating-point numbers correctly map and wrap onto the torus grid boundaries."""
        # A position of 1.2 should wrap to index mapping matching 0.2 via modulo
        idx_x1, idx_y1, idx_z1 = self.engine.map_coordinates_to_3d_torus(1.2, 0.4, -0.1)
        idx_x2, idx_y2, idx_z2 = self.engine.map_coordinates_to_3d_torus(0.2, 0.4, 0.9)
        
        self.assertEqual(idx_x1, idx_x2)
        self.assertEqual(idx_y1, idx_y2)
        self.assertEqual(idx_z1, idx_z2)

    def test_einstein_fresnel_lens_generation(self):
        """Ensures the optical lensing calculation yields bounded phase dimensions between 0 and 2*pi."""
        self.engine.process_3d_ternary_topography(0.5, 0.5, 0.5, raw_signal=2.5)
        lens_matrix = self.engine.compute_einstein_fresnel_lens(0.5, 0.5, 0.5)
        
        self.assertEqual(lens_matrix.shape, (8, 8, 8))
        self.assertTrue(np.all(lens_matrix >= 0.0))
        self.assertTrue(np.all(lens_matrix <= 2.0 * np.pi))

    def test_tensored_trinity_resolution(self):
        """Validates that the multi-dimensional tensor contraction returns valid trajectories and profiles."""
        self.engine.process_3d_ternary_topography(0.3, 0.6, 0.2, raw_signal=-2.0)
        self.engine.relax_3d_field_potentials(iterations=1)
        
        v_x, v_y, v_z, anomaly = self.engine.calculate_tensored_ramanujan_godel_lagrangian(0.3, 0.6, 0.2)
        
        # Verify numeric outputs are active floating-point metrics
        self.assertIsInstance(v_x, (float, np.float64))
        self.assertIsInstance(anomaly, bool)

if __name__ == "__main__":
    unittest.main()
