from yta_general_utils.programming.enum import YTAEnum as Enum


class MANIM_RENDERER(Enum):
    """
    The different rendeders manim has available.

    These are some tests I made with these renderers:
    - ImageMobject + Cairo works, but positioning gets crazy.
    - ImageMobject + Opengl fails
    - OpenGLImageMobject + Opengl works perfectly.
    - VideoMobject (ImageMobject) + Cairo works, but positioning gets crazy.
    - VideoMobject (ImageMobject) + Opengl fails
    - VideoMobject (OpenGLImageMobject) + Opengl only shows the first frame, but positioning is perfect.
    - Didn't test anything else
    """
    CAIRO = 'cairo'
    OPENGL = 'opengl'