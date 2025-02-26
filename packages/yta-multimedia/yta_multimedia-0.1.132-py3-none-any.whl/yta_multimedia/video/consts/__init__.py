DEFAULT_SCENE_SIZE = (1920, 1080)
"""
A default scene size (FullHD) defined in pixels.
This size is the same as in moviepy because this
engine works also with pixels.
"""
MOVIEPY_SCENE_DEFAULT_SIZE = (1920, 1080)
"""
This is the default moviepy scene size we
use to simplify the way we calculate and 
use coordinates to position videos over
other videos when working with moviepy
video engine.
"""
MANIM_SCENE_DEFAULT_SIZE = (8, 14 + (2 / 9))
"""
The manim equivalent of an scene of 1920x1080 pixels,
adapted to be able to work with it when using the
manim engine.
"""


__all__ = [
    'MANIM_SCENE_DEFAULT_SIZE',
    'MOVIEPY_SCENE_DEFAULT_SIZE',
    'DEFAULT_SCENE_SIZE'
]