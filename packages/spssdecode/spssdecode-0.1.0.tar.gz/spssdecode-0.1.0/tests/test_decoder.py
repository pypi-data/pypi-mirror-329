import unittest
import numpy as np
from spssdecode.decoder import Decoder

class TestDecoder(unittest.TestCase):
    def setUp(self):
        self.decoder = Decoder()

    def test_detect_stars(self):
        # Create a mock image with a bright region
        image_data = np.zeros((400, 400, 3), dtype=np.uint8)
        center = (200, 200)  # Center of the circular boundary
        boundary_radius = 150  # Radius of the circular boundary
        image_data[190:200, 190:200] = 255  # Bright region (simulating a star)
        stars = self.decoder.detect_stars(image_data, center, boundary_radius)
        self.assertGreater(len(stars), 0)  # Ensure at least one star is detected

    def test_analyze_twinkling(self):
        stars = [{"x": 10, "y": 10, "size": 10, "color": "white"}]
        twinkling_patterns = self.decoder.analyze_twinkling(stars)
        self.assertEqual(len(twinkling_patterns), len(stars))  # Ensure one pattern per star

    def test_decode_gradient(self):
        image_data = np.ones((400, 400, 3), dtype=np.uint8) * 128  # Uniform intensity
        gradient_metadata = self.decoder.decode_gradient(image_data)
        self.assertIn("gradient_metadata", gradient_metadata)  # Ensure gradient metadata is present

    def test_decode_star_map(self):
        image_data = np.zeros((400, 400, 3), dtype=np.uint8)
        center = (200, 200)  # Center of the circular boundary
        boundary_radius = 150  # Radius of the circular boundary
        image_data[190:200, 190:200] = 255  # Bright region (simulating a star)
        decoded_data = self.decoder.decode_star_map(image_data, center, boundary_radius)
        self.assertIn("stars", decoded_data)
        self.assertIn("twinkling_patterns", decoded_data)
        self.assertIn("gradient_metadata", decoded_data)
        self.assertGreater(len(decoded_data["stars"]), 0)  # Ensure stars are detected

if __name__ == "__main__":
    unittest.main()