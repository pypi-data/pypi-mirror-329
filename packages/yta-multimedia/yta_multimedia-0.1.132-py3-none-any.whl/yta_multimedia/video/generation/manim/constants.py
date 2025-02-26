"""
TODO: Please, put some structure here and more comments
"""
from yta_multimedia.video.consts import MANIM_SCENE_DEFAULT_SIZE


MANIM_RESOURCES_FOLDER = 'resources/manim/'

# Manim core
MANDATORY_CONFIG_PARAMETER = 1
OPTIONAL_CONFIG_PARAMETER = 0
# I obtained manim dimensions from here: https://docs.manim.community/en/stable/faq/general.html#what-are-the-default-measurements-for-manim-s-scene
LEFT_MARGIN = -MANIM_SCENE_DEFAULT_SIZE[0] / 2
UP_MARGIN = MANIM_SCENE_DEFAULT_SIZE[1] / 2
STANDARD_HEIGHT = 1080
"""
This is our standard height (in pixels) as we will create animation
videos of 1920x1080.
"""
STANDARD_WIDTH = 1920
"""
This is our standard width (in pixels) as we will create animation
videos of 1920x1080.
"""

