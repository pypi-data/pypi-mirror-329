from yta_multimedia.video.edition.resize import resize_video
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.file.checker import FileValidator

import cv2


def get_video_size(video_filename: str):
        """
        Return a tuple containing the provided
        'video_filename' size (w, h) if the parameter
        is a filename of a valid video file.
        """
        # TODO: Refactor this method to allow any kind
        # of video parameter and I detect dynamically
        # if str to use this below, or clip to use moviepy
        if not PythonValidator.is_string(video_filename):
            raise Exception('The provided "video_filename" parameter is not a valid string.')
        
        if not FileValidator.file_is_video_file(video_filename):
            raise Exception('The provided "video_filename" is not a valid video file name.')

        v = cv2.VideoCapture(video_filename)

        return int(v.get(cv2.CAP_PROP_FRAME_WIDTH)), int(v.get(cv2.CAP_PROP_FRAME_HEIGHT))

__all__ = [
    resize_video,
    get_video_size
]

