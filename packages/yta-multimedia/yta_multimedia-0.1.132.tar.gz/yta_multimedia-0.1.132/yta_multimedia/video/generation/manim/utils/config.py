from yta_general_utils.file.writer import FileWriter
from yta_general_utils.file.reader import FileReader
from yta_general_utils.programming.path import get_project_abspath


CONFIG_MANIM_ABSPATH = f'{get_project_abspath()}manim_parameters.json'

class ManimConfig:
    """
    Class to simplify and encapsulate the functionality
    related to manim configuration file, that is a file
    in which we write some configuration to be able to
    be read by the manim engine.
    """

    @property
    def config(self):
        """
        Read the configuration file and return it as a json
        object.
        """
        return FileReader.read_json(CONFIG_MANIM_ABSPATH)

    @staticmethod
    def write(json_data):
        """
        Writes the the provided 'json_data' manim configuration
        in the configuration file so the parameters could be read
        later by the manim engine. This is the way to share 
        parameters to the process.
        """
        # TODO: Check that 'json_data' is valid and well-formatted
        FileWriter.write_json_to_file(json_data, CONFIG_MANIM_ABSPATH)