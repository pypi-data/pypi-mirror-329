
from yta_multimedia.video.generation.manim.classes.base_manim_animation import BaseManimAnimation
from yta_multimedia.video.generation.manim.enums import MANIM_RENDERER
from yta_multimedia.video.generation.manim.classes.base_manim_animation_wrapper import BaseManimAnimationWrapper, ManimAnimationType
from yta_multimedia.video.consts import MOVIEPY_SCENE_DEFAULT_SIZE
from yta_multimedia.video.generation.manim.utils.dimensions import fitting_text
from yta_multimedia.video.position import Position
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.programming.validator.number import NumberValidator
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileExtension
from manim import *
from typing import Union


class RainOfWordsManimAnimationWrapper(BaseManimAnimationWrapper):
    """
    This is a rain of the provided 'words' over the screen, that
    appear in random positions.
    """
    words: list[str] = None
    duration: float = None

    def __init__(self, words: list[str], duration: float):
        # TODO: This parameter validation could be done
        # by our specific parameter validator (under
        # construction yet)
        exception_messages = []

        if not PythonValidator.is_list_of_string(words):
            exception_messages.append('The "words" parameter provided is not a list of strings.')
        
        if not NumberValidator.is_positive_number(duration) or not NumberValidator.is_number_between(duration, 0, 100, do_include_lower_limit = False):
            exception_messages.append('The "duration" parameter provided is not a positive number between (0, 100] (zero is not valid).')

        if len(exception_messages) > 0:
            raise Exception('\n'.join([exception_message for exception_message in exception_messages]))
        
        self.words = words
        self.duration = duration
        super().__init__(RainOfWordsManimAnimationGenerator, ManimAnimationType.TEXT_ALPHA)

class RainOfWordsManimAnimationGenerator(BaseManimAnimation):
    """
    This is a rain of the provided 'words' over the screen, that
    appear in random positions.
    """
    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, parameters: dict, output_filename: Union[str, None] = None):
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
        each_word_time = self.parameters['duration'] / len(self.parameters['words'])
        # Adjust the divisor number to modify word size
        for word in self.parameters['words']:
            text = fitting_text(word, MOVIEPY_SCENE_DEFAULT_SIZE[0] / 6)
            # TODO: This was previously considering the limits to
            # make the text be always inside the scene, but now...
            #random_coords = Position.RANDOM_INSIDE.get_manim_position_center((text.width, text.height))
            random_coords = Position.RANDOM_INSIDE.get_manim_position_center()
            text.move_to(random_coords)
            self.add(text)
            self.wait(each_word_time)