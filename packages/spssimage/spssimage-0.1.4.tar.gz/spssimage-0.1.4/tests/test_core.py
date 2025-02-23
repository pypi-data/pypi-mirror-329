import unittest
from spssimage.core import Canvas
import os


class TestCanvas(unittest.TestCase):
    def test_canvas_creation(self):
        canvas = Canvas(100, 100, background=(255, 255, 255))
        self.assertEqual(canvas.pixels.shape, (100, 100, 3))

    def test_generate_gif(self):
        canvas = Canvas(100, 100, background=(0, 0, 0))
        pixel_positions = [(20, 20), (50, 50), (80, 80)]
        base_color = (255, 255, 255)
        canvas.save_gif(pixel_positions, base_color, "test_gif.gif", frames=10, duration=100, loop=0)
        self.assertTrue(os.path.exists("test_gif.gif"))


if __name__ == "__main__":
    unittest.main()