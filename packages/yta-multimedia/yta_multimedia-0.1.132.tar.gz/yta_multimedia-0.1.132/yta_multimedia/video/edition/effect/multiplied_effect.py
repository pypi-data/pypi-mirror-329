from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.parser import VideoParser
from yta_general_utils.programming.validator.number import NumberValidator
from moviepy import Clip, clips_array

import math


class MultipliedEffect(Effect):
    """
    Makes the provided 'video' appear repeated
    in the scene in 'rows' rows and columns, so
    the video appears the pow of the 'times' you
    provide.

    The larger the 'rows' number is, the longer
    it takes to render.
    """

    def apply(self, video: Clip, times: int) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlinkEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        if not NumberValidator.is_positive_number(times):
            raise Exception('The provided "times" value is not a positive number.')

        # TODO: This limitation is hardcoded
        if times > 6:
            raise Exception('Sorry, to large to render... Limited until we find a way to speed up the process.')

        times *= times

        audio = video.audio
        size = (video.w, video.h)

        # TODO: Try video.resized(1 / times)
        videos_array = [
            [video] * times
            for _ in range(times)
        ]

        return clips_array(videos_array).resized(size).with_audio(audio)

    # TODO: I don't need this
    def apply_over_video(self, video, background_video):
        return super().apply_over_video(video, background_video)