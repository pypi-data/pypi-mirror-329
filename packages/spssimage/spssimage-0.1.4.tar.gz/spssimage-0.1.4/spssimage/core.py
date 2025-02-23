import numpy as np
from PIL import Image


class Canvas:
    def __init__(self, width, height, mode="RGB", background=(0, 0, 0)):
        self.width = width
        self.height = height
        self.mode = mode
        self.pixels = np.full((height, width, len(mode)), background, dtype=np.uint8)

    def draw_circle(self, x, y, radius, color):
        """Draw a circle using Bresenham's Circle Algorithm."""
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx**2 + dy**2 <= radius**2:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        self.pixels[ny, nx] = color

    def generate_twinkling_frames(self, stars, frames=30, duration=100, loop=0):
        """
        Generate a sequence of frames with stars that flicker rapidly.
        :param stars: List of dictionaries, each containing 'x', 'y', 'radius', 'base_color'.
        :param frames: Number of frames in the animation.
        :param duration: Duration of each frame in milliseconds.
        :param loop: Number of loops (0 for infinite).
        :return: List of PIL.Image objects representing the frames.
        """
        frame_list = []
        num_stars = len(stars)
        random.seed(42)  # Seed for reproducibility
        for i in range(frames):
            frame = Canvas(self.width, self.height, self.mode)
            frame.pixels = self.pixels.copy()  # Start with the base canvas
            for idx, star in enumerate(stars):
                x, y, radius, base_color = star['x'], star['y'], star['radius'], star['base_color']
                # Randomize flickering interval for each star
                flicker_interval = random.randint(1, 3)  # Flicker every 1-3 frames
                # Determine if the star should be "on" or "off"
                is_on = ((i // flicker_interval) % 2 == 0)
                # Draw the star if it's "on", otherwise skip
                if is_on:
                    frame.draw_circle(x, y, radius, base_color)
            frame_list.append(Image.fromarray(frame.pixels.astype('uint8'), self.mode))
        return frame_list

    def save_gif(self, stars, filename, frames=30, duration=100, loop=0):
        """
        Save an animated GIF of flickering stars.
        :param stars: List of dictionaries, each containing 'x', 'y', 'radius', 'base_color'.
        :param filename: Output GIF file name.
        :param frames: Number of frames in the animation.
        :param duration: Duration of each frame in milliseconds.
        :param loop: Number of loops (0 for infinite).
        """
        frames_list = self.generate_twinkling_frames(stars, frames, duration, loop)
        frames_list[0].save(
            filename,
            save_all=True,
            append_images=frames_list[1:],
            duration=duration,
            loop=loop
        )