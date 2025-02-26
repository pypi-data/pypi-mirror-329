from yta_multimedia.video.generation.manim.classes.base_manim_animation import BaseManimAnimation
from yta_multimedia.video.consts import MANIM_SCENE_DEFAULT_SIZE
from yta_multimedia.video.generation.manim.enums import MANIM_RENDERER
from yta_multimedia.video.generation.manim.classes.base_manim_animation_wrapper import BaseManimAnimationWrapper
from yta_general_utils.programming.validator.number import NumberValidator
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileExtension
from typing import Union
from manim import *


class CinematicBarsManimAnimationWrapper(BaseManimAnimationWrapper):
    """
    Black bars that appear to make the scene cinematic.
    """
    duration: float = None

    def __init__(self, duration: float):
        # TODO: This parameter validation could be done
        # by our specific parameter validator (under
        # construction yet)
        exception_messages = []

        if not NumberValidator.is_positive_number(duration) or not NumberValidator.is_number_between(duration, 0, 100, do_include_lower_limit = False):
            exception_messages.append('The "duration" parameter provided is not a positive number between (0, 100] (zero is not valid).')

        if len(exception_messages) > 0:
            raise Exception('\n'.join([exception_message for exception_message in exception_messages]))
        
        self.duration = duration
        super().__init__(CinematicBarsManimAnimationGenerator)

class CinematicBarsManimAnimationGenerator(BaseManimAnimation):
    """
    Black bars that appear to make the scene cinematic.
    """
    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(
        self,
        parameters: dict,
        output_filename: Union[str, None] = None
    ):
        """
        Build the manim animation video and stores it
        locally as the provided 'output_filename', 
        returning the final output filename.

        This method will call the '.animate()' method
        to build the scene with the instructions that
        are written in that method.
        """
        output_filename = Output.get_filename(output_filename, FileExtension.MOV)

        return super().generate(
            parameters,
            renderer = MANIM_RENDERER.CAIRO,
            output_filename = output_filename
        )
    
    def animate(self):
        top_bar = Rectangle(BLACK, stroke_width = 0, fill_color = BLACK, fill_opacity = 1, height = MANIM_SCENE_DEFAULT_SIZE[1] * 0.15, width = MANIM_SCENE_DEFAULT_SIZE[0])
        bottom_bar = top_bar.copy()

        START_TOP_POSITION = (0, MANIM_SCENE_DEFAULT_SIZE[1] / 2 + (top_bar.height / 2), 0)
        STAY_TOP_POSITION = (0, MANIM_SCENE_DEFAULT_SIZE[1] / 2, 0)
        START_BOTTOM_POSITION = (0, -MANIM_SCENE_DEFAULT_SIZE[1] / 2 - (bottom_bar.height / 2), 0)
        STAY_BOTTOM_POSITION = (0, -MANIM_SCENE_DEFAULT_SIZE[1] / 2, 0)

        top_bar.move_to(START_TOP_POSITION)
        bottom_bar.move_to(START_BOTTOM_POSITION)

        self.add(top_bar)
        self.add(bottom_bar)

        # Appearing and dissapearing animation can be 2 seconds
        # longer as maximum (each one). If this happens, the 
        # stay will be longer
        animation_duration = 0.2 * self.parameters['duration']
        stay_duration = 0.6 * self.parameters['duration']
        if animation_duration > 2:
            stay_duration += (animation_duration - 2) * 2

        self.play(AnimationGroup([
            top_bar.animate.move_to(STAY_TOP_POSITION),
            bottom_bar.animate.move_to(STAY_BOTTOM_POSITION)
        ]), run_time = animation_duration, rate_func = linear)

        self.wait(stay_duration)

        self.play(AnimationGroup([
            top_bar.animate.move_to(START_TOP_POSITION),
            bottom_bar.animate.move_to(START_BOTTOM_POSITION)
        ]), run_time = animation_duration, rate_func = linear)







# class CinematicBarsManimAnimation(BaseManimAnimation):
#     """
#     Black bars that appear to make the scene cinematic.
#     """
#     def construct(self):
#         """
#         This method is called by manim when executed by shell and
#         will call the scene animation render method to be processed
#         and generated.
#         """
#         self.animate()

#     def generate(self, duration: float = 2, output_filename: str = 'output.mov'):
#         """
#         Checks and validates the provided parameters and generates
#         the manim animation if those parameters are valid.
#         """
#         # Check and validate all parameters
#         parameters = {}

#         if super().parameter_is_mandatory('duration', self.required_parameters) and not duration:
#             raise Exception('Field "duration" is mandatory. Aborting manim creation...')
#         if duration < 0 or duration > 100:
#             raise Exception('Field "duration" value is not valid. Must be between 0 and 100')
        
#         parameters['duration'] = duration

#         if not output_filename:
#             output_filename = 'output.mov'

#         # Generate the animation when parameters are valid
#         super().generate(parameters, output_filename = output_filename)

#         return output_filename

#     def animate(self):
#         top_bar = Rectangle(BLACK, stroke_width = 0, fill_color = BLACK, fill_opacity = 1, height = MANIM_SCENE_DEFAULT_SIZE[1] * 0.15, width = MANIM_SCENE_DEFAULT_SIZE[0])
#         bottom_bar = top_bar.copy()

#         START_TOP_POSITION = (0, MANIM_SCENE_DEFAULT_SIZE[1] / 2 + (top_bar.height / 2), 0)
#         STAY_TOP_POSITION = (0, MANIM_SCENE_DEFAULT_SIZE[1] / 2, 0)
#         START_BOTTOM_POSITION = (0, -MANIM_SCENE_DEFAULT_SIZE[1] / 2 - (bottom_bar.height / 2), 0)
#         STAY_BOTTOM_POSITION = (0, -MANIM_SCENE_DEFAULT_SIZE[1] / 2, 0)

#         top_bar.move_to(START_TOP_POSITION)
#         bottom_bar.move_to(START_BOTTOM_POSITION)

#         self.add(top_bar)
#         self.add(bottom_bar)

#         # Appearing and dissapearing animation can be 2 seconds
#         # longer as maximum (each one). If this happens, the 
#         # stay will be longer
#         animation_duration = 0.2 * self.parameters['duration']
#         stay_duration = 0.6 * self.parameters['duration']
#         if animation_duration > 2:
#             stay_duration += (animation_duration - 2) * 2

#         self.play(AnimationGroup([
#             top_bar.animate.move_to(STAY_TOP_POSITION),
#             bottom_bar.animate.move_to(STAY_BOTTOM_POSITION)
#         ]), run_time = animation_duration, rate_func = linear)

#         self.wait(stay_duration)

#         self.play(AnimationGroup([
#             top_bar.animate.move_to(START_TOP_POSITION),
#             bottom_bar.animate.move_to(START_BOTTOM_POSITION)
#         ]), run_time = animation_duration, rate_func = linear)