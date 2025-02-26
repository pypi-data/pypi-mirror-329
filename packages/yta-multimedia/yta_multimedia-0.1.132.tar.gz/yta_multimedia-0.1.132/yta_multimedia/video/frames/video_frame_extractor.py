from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.edition.video_frame_t_helper import VideoFrameTHelper
from yta_image.converter import ImageConverter
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.programming.validator.number import NumberValidator
from moviepy.Clip import Clip
from imageio import imsave
from typing import Union

import numpy as np


class FrameExtractionType(Enum):
    """
    Enum to simplify the way we indicate the frame extraction
    operation we want to execute.
    """
    FRAME_TIME_MOMENT = 'frame_time_moment'
    """
    Use the frame time moments, which are the time moments 
    that belong to the time in which the frame is being
    displayed according to its duration and fps.
    """
    FRAME_INDEX = 'frame_index'
    """
    Use the frame indexes, which are the indexes of the
    frames, one after the other.
    """

class VideoFrameExtractor:
    """
    Class to simplify the process of extracting video frames by time
    or frame number.

    A moviepy clip is built by consecutive frames. The first frame is
    on t = 0, and the next frames are obtained by applying a (a, b]
    interval. This means that if we a have a video of 10 fps, each 
    frame will last 0.1s. So, considering the previous condition, the
    second frame will be at 0.1s, so you will be able to access it by
    providing a time between (0.000000000001, 0.1].
    """

    # TODO: Implement the 'output_filename' optional parameter to store
    # the frames if parameter is provided.

    @staticmethod
    def get_frame_by_index(
        video: Clip,
        index: int = 0,
        output_filename: Union[str, None] = None
    ):
        """
        Get the frame 't' of the provided 'video'. The frame number
        must be a valid one.
        """
        frame = VideoFrameExtractor.get_frame(video, FrameExtractionType.FRAME_INDEX, index)

        if output_filename:
            # TODO: Why type (?)
            #imsave(output_filename, frame.astype("uint8"))
            imsave(output_filename, frame)

        return frame

    @staticmethod
    def get_frames_by_index(
        video: Clip,
        indexes: list[float] = [0]
    ):
        """
        Get all the 't' frames of the provided 'video'. Those frame
        numbers must be valid.
        """
        if not PythonValidator.is_list(indexes):
            if NumberValidator.is_positive_number(indexes):
                indexes = [indexes]
            else:
                raise Exception('The provided "indexes" is not an array of frame numbers nor a single one.')
            
        return [
            VideoFrameExtractor.get_frame(video, FrameExtractionType.FRAME_INDEX, index)
            for index in indexes
        ]
    
    @staticmethod
    def get_frame_by_t(
        video: Clip,
        t: float = 0.0,
        output_filename: Union[str, None] = None
    ):
        """
        Get the frame in the given 't' time moment of the
        provided 'video'. The frame time must be a valid one,
        between 0 and the video duration.
        """
        frame = VideoFrameExtractor.get_frame(video, FrameExtractionType.FRAME_INDEX, t)

        if output_filename:
            # TODO: Why type (?)
            #imsave(output_filename, frame.astype("uint8"))
            imsave(output_filename, frame)

        return frame

    @staticmethod
    def get_frames_by_t(
        video: Clip,
        t: list[float] = [0.0]
    ):
        """
        Get all the frame corresponding to the time moments in
        provided 't' of the provided 'video'. All frame times
        must be valid, between 0 and the video duration.
        """
        if not PythonValidator.is_list(t):
            if NumberValidator.is_positive_number(t):
                t = [t]
            else:
                raise Exception('The provided "t" is not an array of frame times nor a single one.')
            
        return [
            VideoFrameExtractor.get_frame(video, FrameExtractionType.FRAME_TIME_MOMENT, t_)
            for t_ in t
        ]
    
    @staticmethod
    def get_frame(
        video: Clip,
        mode: FrameExtractionType = FrameExtractionType.FRAME_INDEX,
        t: Union[float, int] = 0
    ):
        """
        Get the frame corresponding to the provided 't' frame number
        or time moment. Feel free to use the moviepy .get_frame()
        method instead.

        This is my own method due to some problems with the original
        moviepy .get_frame() and because of its laxity.
        """
        video = VideoParser.to_moviepy(video)
        mode = FrameExtractionType.to_enum(mode)

        if not NumberValidator.is_positive_number(t):
            raise Exception('The provided "t" value is not a positive number.')

        t = {
            FrameExtractionType.FRAME_INDEX: VideoFrameTHelper.get_frame_t_from_frame_index(int(t), video.fps),
            FrameExtractionType.FRAME_TIME_MOMENT: float(t)
        }[mode]

        return video.get_frame(t)

    @staticmethod
    def get_all_frames(
        video: Clip
    ):
        """
        Returns all the frames from the provided 'video'.
        """
        video = VideoParser.to_moviepy(video)

        return [
            frame
            for frame in video.iter_frames()
        ]
    
    @staticmethod
    def get_first_frame(
        video: Clip
    ):
        """
        Obtain the first frame of the provided 'video' as a ndim=3
        numpy array containing the clip part (no mask) as not
        normalized values (between 0 and 255).
        """
        video = VideoParser.to_moviepy(video)

        return VideoFrameExtractor.get_frame_by_index(video, 0)
    
    @staticmethod
    def get_last_frame(
        video: Clip
    ):
        """
        Obtain the last frame of the provided 'video' as a ndim=3
        numpy array containing the clip part (no mask) as not
        normalized values (between 0 and 255).
        """
        video = VideoParser.to_moviepy(video)

        number_of_frames = VideoFrameTHelper.get_number_of_frames(video.duration, video.fps)

        return VideoFrameExtractor.get_frame_by_index(len(number_of_frames) - 1)
    
    # TODO: Would be perfect to have some methods to turn frames into
    # RGBA denormalized (0, 255) or normalized (0, 1) easier because
    # it is needed to work with images and other libraries. Those 
    # methods would iterate over the values and notice if they are in
    # an specific range so they need to be change or even if they are
    # invalid values (not even in [0, 255] range because they are not
    # rgb or rgba colors but math calculations).
    # This is actually being done by the VideoMaskHandler
    @staticmethod
    def get_frame_as_rgba_by_t(
        video: Clip,
        t: float,
        do_normalize: bool = False,
        output_filename: str = None
    ):
        """
        Gets the frame of the requested 't' time moment of the
        provided 'video' as a normalized RGBA numpy array that
        is built by joining the rgb frame (from main clip) and
        the alpha (from .mask clip), useful to detect transparent
        regions.
        """
        video = VideoParser.to_moviepy(video, do_include_mask = True)

        # We first normalize the clips
        main_frame = VideoFrameExtractor.get_frame_by_t(video, t) / 255  # RGB numpy array normalized 3d <= r,g,b
        mask_frame = VideoFrameExtractor.get_frame_by_t(video.mask, t)[:, :, np.newaxis]  # Alpha numpy array normalized 1d <= alpha
        # Combine RGB of frame and A from mask to RGBA numpy array (it is normalized)
        frame_rgba = np.concatenate((main_frame, mask_frame), axis = 2) # 4d <= r,g,b,alpha

        if output_filename:
            # TODO: Check extension
            ImageConverter.numpy_image_to_pil(frame_rgba).save(output_filename)
            # TODO: Write numpy as file image
            # Video mask is written as 0 or 1 (1 is transparent)
            # but main frame is written as 0 to 255, and the
            # 'numpy_image_to_pil' is expecting from 0 to 1
            # (normalized) instead of from 0 to 255 so it won't
            # work

        if not do_normalize:
            frame_rgba *= 255

        return frame_rgba
    