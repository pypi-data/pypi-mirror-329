import unittest
from spssstar.core import StarEncoder, StarMap, EncodedStar


class TestStarEncoder(unittest.TestCase):
    def test_encode_position(self):
        encoder = StarEncoder(width=400, height=400, boundary_radius=150)
        x, y = encoder.encode_position("test-session", 0)
        self.assertTrue(0 <= x < 400)
        self.assertTrue(0 <= y < 400)

    def test_encode_color(self):
        encoder = StarEncoder()
        color = encoder.encode_color("test-session", priority="high")
        self.assertEqual(color, (255, 0, 0))

    def test_encode_twinkling_pattern(self):
        encoder = StarEncoder()
        pattern = encoder.encode_twinkling_pattern("test-session")
        self.assertIn("amplitude", pattern)
        self.assertIn("frequency", pattern)
        self.assertTrue(50 <= pattern["amplitude"] <= 150)
        self.assertTrue(1 <= pattern["frequency"] <= 5)

    def test_encode_star_map(self):
        encoder = StarEncoder()
        star_map = encoder.encode_star_map("test-session", num_stars=5)
        self.assertEqual(len(star_map.stars), 5)
        for star in star_map.stars:
            self.assertIsInstance(star, EncodedStar)


if __name__ == "__main__":
    unittest.main()