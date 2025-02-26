from yta_multimedia.video.edition.settings import SMALL_AMOUNT_TO_FIX


class VideoFrameTHelper:
    """
    Class to simplify and encapsulate the conversion
    between video and audio time frame moments 't' and
    frame indexes.
    """

    @staticmethod
    def get_number_of_frames(duration: float, fps: float):
        """
        Get the numbers of frames with the given 'duration'
        and 'fps'.
        """
        return int(duration * fps)

    @staticmethod
    def get_video_frames_indexes_from_duration_and_fps(duration: float, fps: float):
        """
        Get all the video frame indexes for a video with
        the given 'fps' and 'duration'. 
        """
        return [
            i
            for i in range(fps * duration)
        ]
    
    @staticmethod
    def get_video_frames_indexes_from_number_of_frames(number_of_frames: int):
        """
        Get all the video frame indexes for a video with
        the given 'number_of_frames'.
        """
        return [
            i
            for i in range(number_of_frames)
        ]

    @staticmethod
    def get_video_frames_ts_from_duration_and_fps(duration: float, fps: float):
        """
        Get all the 't' frames time moments for a video
        with the given 'fps' and 'duration'. Each 't'
        includes a small amount increased to ensure it
        fits the frame time range.
        """
        return [
            VideoFrameTHelper.get_frame_t_from_frame_index(i, fps)
            for i in VideoFrameTHelper.get_video_frames_indexes_from_duration_and_fps(duration, fps)
        ]
    
    @staticmethod
    def get_video_frames_ts_from_number_of_frames(number_of_frames: int, fps: float):
        """
        Get all the 't' frames time moments for a video
        with the given 'number_of_frames'. Each 't'
        includes a small amount increased to ensure it
        fits the frame time range.
        """
        return [
            VideoFrameTHelper.get_frame_t_from_frame_index(i, fps)
            for i in VideoFrameTHelper.get_video_frames_indexes_from_number_of_frames(number_of_frames)
        ]
    # TODO: Should I move this above to another class (?)

    @staticmethod
    def get_frame_t_base(t: float, fps: float):
        """
        Turn the provided 't' video frame time moment to
        the real base one (the one who is the start of
        the frame time interval, plus a minimum quantity
        to avoid floating point number issues).
        """
        return VideoFrameTHelper.get_frame_index_from_frame_t(t, fps) / fps + SMALL_AMOUNT_TO_FIX
    
    @staticmethod
    def get_frame_index_from_frame_t(t: float, fps: float):
        """
        Get the video audio frame 't' time moment base,
        which is the left (lower) limit of that 't' time
        moment.

        As a reminder, any 't' time moment goes from the
        lower limit (including it) to the upper limit 
        (not included). So, there is a time interval in 
        which any 't' time moment is included, which is
        defined by the range [lower_limit, upper_limit).

        For example, in a video with fps=30, any value
        between [0/30, 1/30) will be recognized as a 't'
        time moment for the frame index 0. As you can see,
        the 1/30 is not included, because it will be part
        of the next index, as it is its lower limit that
        is included.
        """
        frame_duration = 1 / fps

        return int((t + SMALL_AMOUNT_TO_FIX) // frame_duration)

    @staticmethod
    def get_frame_t_from_frame_index(index: int, fps: float):
        """
        Get the frame time moment t from the given
        frame 'index'.
        """
        return index / fps + SMALL_AMOUNT_TO_FIX
    
    @staticmethod
    def get_video_audio_tts_from_video_frame_t(video_t: float, video_fps: float, audio_fps: float):
        """
        Get all the audio time moments associated to
        the given 'video' 't' time moment, as an array.

        One video time moment 't' is associated with a lot
        of video audio time 't' time moments. The amount 
        of video audio frames per video frame is calculated
        with the divions of the audio fps by the video fps.

        The result is an array of 't' video audio time
        moments. Maybe you need to turn it into a numpy
        array before using it as audio 't' time moments.
        """
        from yta_general_utils.math.progression import Progression

        audio_frames_per_video_frame = int(audio_fps / video_fps)
        audio_frame_duration = 1 / audio_fps
        video_frame_duration = 1 / video_fps

        t = VideoFrameTHelper.get_frame_t_base(video_t, video_fps)

        return Progression(t, t + video_frame_duration - audio_frame_duration, audio_frames_per_video_frame).values

    @staticmethod
    def get_video_frame_t_from_video_audio_frame_t(audio_t: float, video_fps: float):
        """
        Get the video frame time moment t from the given
        video audio frame time moment 'audio_t'.
        """
        return VideoFrameTHelper.get_frame_t_base(audio_t , video_fps)

    @staticmethod
    def get_video_frame_index_from_video_audio_frame_index(audio_index: int, video_fps: float, audio_fps: float):
        """
        Get the video frame index from the given video
        audio frame index 'audio_index'.
        """
        return round(audio_index * (video_fps / audio_fps))

    @staticmethod
    def get_video_frame_t_from_video_audio_frame_index(audio_index: int, video_fps: float, audio_fps: float):
        """
        Get the video frame time moment t from the given
        video audio frame index 'audio_index'.
        """
        return VideoFrameTHelper.get_frame_t_from_frame_index(
            VideoFrameTHelper.get_video_frame_index_from_video_audio_frame_index(
                audio_index,
                video_fps,
                audio_fps
            ),
            video_fps
        )
    
    @staticmethod
    def get_video_frame_index_from_video_audio_frame_t(audio_t: float, video_fps: float, audio_fps: float):
        """
        Get the video frame index from the given video
        audio frame time moment 'audio_t'.
        """
        return VideoFrameTHelper.get_video_frame_index_from_video_audio_frame_index(
            VideoFrameTHelper.get_frame_index_from_frame_t(
                audio_t,
                audio_fps
            ),
            video_fps,
            audio_fps
        )