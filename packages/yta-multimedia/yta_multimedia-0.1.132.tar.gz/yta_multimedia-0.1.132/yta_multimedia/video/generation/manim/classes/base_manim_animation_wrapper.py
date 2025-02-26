from yta_multimedia.video.generation.manim.classes.base_manim_animation import BaseManimAnimation
from yta_multimedia.video.generation.manim.classes.base_three_d_manim_animation import BaseThreeDManimAnimation
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.programming.attribute_obtainer import AttributeObtainer
from yta_general_utils.programming.enum import YTAEnum as Enum
from typing import Union


class ManimAnimationType(Enum):
    GENERAL = 'general'
    """
    Manim animation which doesn't have an specific
    type by now, so it is classified as a general
    animation.
    """
    TEXT_ALPHA = 'text_alpha'
    """
    Manim animation which is text with a transparent 
    background, intented to be used as a main video
    overlay.
    """

class BaseManimAnimationWrapper:
    """
    Base class for all the manim animation generator
    classes that we want to have in our system.

    This wrapper is to define the attributes that 
    are needed and the manim animation generator
    class that will be used to generate it.
    """
    # TODO: What is this 'types' for (?)
    types: list[ManimAnimationType] = None
    animation_generator_instance: Union[BaseManimAnimation, BaseThreeDManimAnimation] = None

    def __init__(
        self,
        animation_generator_instance_or_class: Union[BaseManimAnimation, BaseThreeDManimAnimation],
        types: Union[list[ManimAnimationType], ManimAnimationType] = ManimAnimationType.GENERAL):
        if (
            not PythonValidator.is_subclass(animation_generator_instance_or_class, BaseManimAnimation) and
            not PythonValidator.is_subclass(animation_generator_instance_or_class, BaseThreeDManimAnimation)
        ):
            raise Exception('The provided "animation_generator_instance_or_class" is not a subclass nor an instance of a subclass of BaseManimAnimation or BaseThreeDManimAnimation classes.')
        
        if PythonValidator.is_a_class(animation_generator_instance_or_class):
            animation_generator_instance_or_class = animation_generator_instance_or_class()

        if types is None:
            types = [ManimAnimationType.GENERAL]
        elif not PythonValidator.is_list(types):
            types = [types]

        types = [
            ManimAnimationType.to_enum(type)
            for type in types
        ]

        self.animation_generator_instance = animation_generator_instance_or_class

    @property
    def attributes(
        self
    ):
        """
        Only the values that are actually set on the
        instance are obtained with 'vars'. If you set
        'var_name = None' but you don't do 
        'self.var_name = 33' in the '__init__' method,
        it won't be returned by the 'vars()' method.
        """
        return AttributeObtainer.get_attributes_from_instance(
            self,
            attributes_to_ignore = ['animation_generator_instance', 'attributes', 'types']
        )

    def generate(self):
        """
        Generate the manim animation if the parameters are
        valid and returns the filename of the generated
        video to be used in the app (you should handle it
        with a 'VideoFileClip(o, has_mask = True)' to load
        it with mask and to be able to handle it).
        """
        return self.animation_generator_instance.generate(
            self.attributes,
            output_filename = 'output.mov'
        )