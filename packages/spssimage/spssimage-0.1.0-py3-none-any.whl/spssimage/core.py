import numpy as np
from PIL import Image


class Canvas:
    def __init__(self, width, height, mode="RGB", background=(0, 0, 0)):
        self.width = width
        self.height = height
        self.mode = mode
        self.pixels = np.full((height, width, len(mode)), background, dtype=np.uint8)

    def save(self, filename, format="PNG"):
        """Save the canvas as an image file."""
        img = Image.fromarray(self.pixels.astype('uint8'), self.mode)
        img.save(filename, format=format)

    def generate_twinkling_frames(self, pixel_positions, base_color, frames=30, duration=100, loop=0):
        """
        Generate a sequence of frames with twinkling pixels.
        :param pixel_positions: List of tuples, each containing (x, y) coordinates of pixels to twinkle.
        :param base_color: Base color of the twinkling pixels (e.g., (255, 255, 255)).
        :param frames: Number of frames in the animation.
        :param duration: Duration of each frame in milliseconds.
        :param loop: Number of loops (0 for infinite).
        :return: List of PIL.Image objects representing the frames.
        """
        frame_list = []
        for i in range(frames):
            frame = Canvas(self.width, self.height, self.mode)
            frame.pixels = self.pixels.copy()  # Start with the base canvas
            for x, y in pixel_positions:
                if 0 <= x < self.width and 0 <= y < self.height:
                    # Add random noise to the brightness of the pixel
                    noise = np.random.uniform(0.5, 1.5)  # Random factor between 0.5 and 1.5
                    brightened_color = tuple(min(255, int(c * noise)) for c in base_color)
                    frame.pixels[y, x] = brightened_color
            frame_list.append(Image.fromarray(frame.pixels.astype('uint8'), self.mode))
        return frame_list

    def save_gif(self, pixel_positions, base_color, filename, frames=30, duration=100, loop=0):
        """
        Save an animated GIF of twinkling pixels.
        :param pixel_positions: List of tuples, each containing (x, y) coordinates of pixels to twinkle.
        :param base_color: Base color of the twinkling pixels (e.g., (255, 255, 255)).
        :param filename: Output GIF file name.
        :param frames: Number of frames in the animation.
        :param duration: Duration of each frame in milliseconds.
        :param loop: Number of loops (0 for infinite).
        """
        frames_list = self.generate_twinkling_frames(pixel_positions, base_color, frames, duration, loop)
        frames_list[0].save(
            filename,
            save_all=True,
            append_images=frames_list[1:],
            duration=duration,
            loop=loop
        )