from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.parser import VideoParser
from moviepy.video.fx import TimeMirror
from moviepy import Clip


class ReversedEffect(Effect):
    """
    This method creates a new one but in reversa, also
    with the sound reversed.
    """
    def apply(self, video: Clip) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlinkEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        return TimeMirror().apply(video)
    
    # TODO: I don't need this
    def apply_over_video(self, video, background_video):
        return super().apply_over_video(video, background_video)