"""
Nice help: https://www.bannerbear.com/blog/how-to-use-ffmpeg-in-python-with-examples/
Official doc: https://www.ffmpeg.org/ffmpeg-resampler.html
More help: https://kkroening.github.io/ffmpeg-python/
Nice guide: https://img.ly/blog/ultimate-guide-to-ffmpeg/
Available flags: https://gist.github.com/tayvano/6e2d456a9897f55025e25035478a3a50

Interesting usage: https://stackoverflow.com/a/20325676
Maybe avoid writting on disk?: https://github.com/kkroening/ffmpeg-python/issues/500#issuecomment-792281072
"""
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.dimensions import get_video_size
from yta_multimedia.utils.resize import get_cropping_points_to_keep_aspect_ratio
from yta_multimedia.video.position import validate_size
from yta_audio.parser import AudioParser
from yta_image.parser import ImageParser
from yta_general_utils.file.handler import FileHandler
from yta_general_utils.temp import Temp
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.file.writer import FileWriter
from yta_general_utils.file.checker import FileValidator
from yta_general_utils.date import seconds_to_hh_mm_ss
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.programming.validator.number import NumberValidator
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from typing import Union
from subprocess import run


class FfmpegAudioCodec(Enum):
    """
    TODO: Fill this

    Should be used in the **-c:a {codec}** flag.
    """
    AAC = 'aac'
    """
    Default encoder.
    """
    AC3 = 'ac3'
    """
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-ac3-and-ac3_005ffixed
    """
    AC3_FIXED = 'ac3_fixed'
    """
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-ac3-and-ac3_005ffixed
    """
    FLAC = 'flac'
    """
    FLAC (Free Lossless Audio Codec) Encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-flac-2
    """
    OPUS = 'opus'
    """
    This is a native FFmpeg encoder for the Opus format. Currently, it's
    in development and only implements the CELT part of the codec. Its
    quality is usually worse and at best is equal to the libopus encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-opus
    """
    LIBFDK_AAC = 'libfdk_aac'
    """
    libfdk-aac AAC (Advanced Audio Coding) encoder wrapper. The libfdk-aac
    library is based on the Fraunhofer FDK AAC code from the Android project.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libfdk_005faac
    """
    LIBLC3 = 'liblc3'
    """
    liblc3 LC3 (Low Complexity Communication Codec) encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-liblc3
    """
    LIBMP3LAME = 'libmp3lame'
    """
    LAME (Lame Ain't an MP3 Encoder) MP3 encoder wrapper.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libmp3lame-1
    """
    LIBOPENCORE_AMRNB = 'libopencore_amrnb'
    """
    OpenCORE Adaptive Multi-Rate Narrowband encoder.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libopencore_002damrnb-1ss
    """
    LIBOPUS = 'libopus'
    """
    libopus Opus Interactive Audio Codec encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libopus-1
    """
    LIBSHINE = 'libshine'
    """
    Shine Fixed-Point MP3 encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libshine-1
    """
    LIBTWOLAME = 'libtwolame'
    """
    TwoLAME MP2 encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libtwolame
    """
    LIBVO_AMRWBENC = 'libvo-amrwbenc'
    """
    VisualOn Adaptive Multi-Rate Wideband encoder.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libvo_002damrwbenc
    """
    LIBVORBIS = 'libvorbis'
    """
    libvorbis encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libvorbis
    """
    MJPEG = 'mjpeg'
    """
    Motion JPEG encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-mjpeg
    """
    WAVPACK = 'wavpack'
    """
    WavPack lossless audio encoder.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-wavpack
    """
    COPY = 'copy'
    """
    Indicates that the codec must be copied from 
    the input.
    """

class FfmpegVideoCodec(Enum):
    """
    These are the video codecs available as Enums. The amount of codecs
    available depends on the ffmpeg built version.
    
    Should be used in the **-c:v {codec}** flag.
    """
    A64_MULTI = 'a64_multi'
    """
    A64 / Commodore 64 multicolor charset encoder. a64_multi5 is extended with 5th color (colram).

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-a64_005fmulti_002c-a64_005fmulti5
    """
    A64_MULTI5 = 'a64_multi5'
    """
    A64 / Commodore 64 multicolor charset encoder. a64_multi5 is extended with 5th color (colram).

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-a64_005fmulti_002c-a64_005fmulti5
    """
    CINEPAK = 'Cinepak'
    """
    Cinepak aka CVID encoder. Compatible with Windows 3.1 and vintage MacOS.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-Cinepak
    """
    GIF = 'GIF'
    """
    GIF image/animation encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-Cinepak
    """
    HAP = 'Hap'
    """
    Vidvox Hap video encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-Hap
    """
    JPEG2000 = 'jpeg2000'
    """
    The native jpeg 2000 encoder is lossy by default

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-jpeg2000
    """
    LIBRAV1E = 'librav1e'
    """
    rav1e AV1 encoder wrapper.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-librav1e
    """
    LIBAOM_AV1 = 'libaom-av1'
    """
    libaom AV1 encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libaom_002dav1
    """
    # TODO: Continue with this (https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libsvtav1)
    QTRLE = 'qtrle'
    """
    TODO: Find information about this video codec.

    More info: ???
    """
    PRORES = 'prores'
    """
    Apple ProRes encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-ProRes
    """
    COPY = 'copy'
    """
    Indicates that the codec must be copied from 
    the input.
    """

class FfmpegVideoFormat(Enum):
    """
    Enum list to simplify the way we choose a video format for
    the ffmpeg command. This should be used with the FfmpegFlag
    '-f' flag that forces that video format.

    Should be used in the **-f {format}** flag.
    """
    CONCAT = 'concat'
    """
    The format will be the concatenation.
    """
    AVI = 'avi'
    """
    Avi format.

    # TODO: Explain more
    """
    PNG = 'png'
    """
    # TODO: Look for mor information about this vcodec
    # TODO: I don't know if this one is actually an FfmpegVideoFormat
    # or if I need to create another Enum class. This option us used
    # in the '-vcodec' option, and the other ones are used in the
    # 'c:v' option.
    """
    # TODO: Keep going

class FfmpegFilter(Enum):
    """
    Enum list to simplify the way we use a filter for the
    ffmpeg command.

    Should be used in the **-filter {filter}** flag.
    """
    THUMBNAIL = 'thumbnail'
    """
    Chooses the most representative frame of the video to be used
    as a thumbnail.
    """

class FfmpegPixelFormat(Enum):
    """
    Enum list to simplify the way we use a pixel format for
    the ffmpeg command.

    Should be used in the **-pix_fmt {format}** flag.
    """
    YUV420p = 'yuv420p'
    """
    This is de default value. TODO: Look for more information about it
    """
    RGB24 = 'rgb24'
    """
    TODO: Look for more information about this pixel format.
    """
    ARGB = 'argb'
    """
    TODO: Look for more information about this pixel format
    """
    YUVA444P10LE = 'yuva444p10le'
    """
    TODO: Look for more information about this pixel format
    """

class FfmpegFlag:
    """
    Class to simplify the way we push flags into the ffmpeg command.
    """
    overwrite: str = '-y'
    """
    Overwrite the output file if existing.

    Notation: **-y**
    """

    @staticmethod
    def force_format(format: FfmpegVideoFormat):
        """
        Force the output format to be the provided 'format'.

        Notation: **-f {format}**
        """
        format = FfmpegVideoFormat.to_enum(format).value

        return f'-f {format}'
    
    @staticmethod
    def safe_routes(value: int):
        """
        To enable or disable unsafe paths.

        Notation: **-safe {value}**
        """
        # TODO: Check that 'value' is a number between -1 and 1

        return f'-safe {str(value)}'
    
    @staticmethod
    def input(input: str):
        """
        To set the input (or inputs) we want.

        Notation: **-i {input}**
        """
        # TODO: I don't know how to check this or format it from 'input' param

        return f'-i {input}'
    
    @staticmethod
    def audio_codec(codec: Union[FfmpegAudioCodec, str]):
        """
        Sets the general audio codec.

        Notation: **-c:a {codec}**
        """
        # We cannot control the big amount of audio codecs that
        # are available so we allow any string as parameter
        try:
            codec = FfmpegAudioCodec.to_enum(codec).value
        except:
            pass

        return f'-c:a {codec}'
    
    @staticmethod
    def video_codec(codec: Union[FfmpegVideoCodec, str]):
        """
        Sets the general video codec.

        Notation: **-c:v {codec}**
        """
        # We cannot control the big amount of video codecs that
        # are available so we allow any string as parameter
        try:
            codec = FfmpegVideoCodec.to_enum(codec).value
        except:
            pass

        return f'-c:v {codec}'

    @staticmethod
    def v_codec(codec: Union[FfmpegVideoCodec, str]):
        """
        Sets the video codec.

        TODO: I don't know exactly the difference between '-c:v {codec}'
        and the '-vcodec' generated in this method. I keep this method
        until I actually find the difference. I don't even know if the
        video codecs I can provide as values are the same as in the other
        method.

        Notation: **-vcodec {codec}**
        """
        # We cannot control the big amount of video codecs that
        # are available so we allow any string as parameter
        try:
            codec = FfmpegVideoCodec.to_enum(codec).value
        except:
            pass

        return f'-vcodec {codec}'

    @staticmethod
    def codec(codec: Union[FfmpegVideoCodec, FfmpegAudioCodec, str]):
        """
        Sets the general codec with '-c {codec}'.

        -c copy indica que se deben copiar los flujos de audio y video sin recodificación, lo que hace que la operación sea rápida y sin pérdida de calidad. TODO: Turn this 'copy' to AudioCodec and VideoCodec (?)

        Notation: **-c {codec}**
        """
        # We cannot control the big amount of video codecs that
        # are available so we allow any string as parameter

        # TODO: Validate provided 'codec'
        # TODO: This method has a variation, it can be '-c:a' or '-c:v'
        if not PythonValidator.is_instance(codec, [FfmpegVideoCodec, FfmpegAudioCodec]):
            try:
                codec = FfmpegVideoCodec.to_enum(codec)
            except:
                pass

        if not PythonValidator.is_instance(codec, [FfmpegVideoCodec, FfmpegAudioCodec]):
            try:
                codec = FfmpegAudioCodec.to_enum(codec)
            except:
                pass

        if PythonValidator.is_instance(codec, [FfmpegVideoCodec, FfmpegAudioCodec]):
            codec = codec.value

        return f'-c {codec}'
    
    @staticmethod
    def map(map: str):
        """
        Set input stream mapping.
        -map [-]input_file_id[:stream_specifier][,sync_file_id[:stream_s set input stream mapping

        # TODO: Improve this

        Notation: **-map {map}**
        """
        return f'-map {map}'
    
    @staticmethod
    def filter(filter: FfmpegFilter):
        """
        Sets the expected filter to be used.

        Notation: **-filter {filter}**
        """
        filter = FfmpegFilter.to_enum(filter).value

        return f'-filter {filter}'
    
    @staticmethod
    def frame_rate(frame_rate: int):
        """
        Sets the frame rate (Hz value, fraction or abbreviation)

        Notation: **-r {frame_rate}**
        """
        # TODO: Validate 'frame_rate'

        return f'-r {str(frame_rate)}'
    
    @staticmethod
    def pixel_format(format: FfmpegPixelFormat):
        """
        Set the pixel format.

        Notation: **-pix_fmt {format}**
        """
        format = FfmpegPixelFormat.to_enum(format).value

        return f'-pix_fmt {format}'
    
    @staticmethod
    def scale_with_size(size: tuple):
        """
        Set a new size.

        Notation: **-vf scale=size[0]:size[1]**
        """
        return f'-vf scale={str(int(size[0]))}:{str(int(size[1]))}'

    @staticmethod
    def scale_with_factor(w_factor: float, h_factor: float):
        """
        Set a new size multiplying by a factor.

        Notation: **-vf "scale=iw*w_factor:ih*h_factor"**
        """
        return f'-vf "scale=iw*{str(w_factor)}:ih*{str(h_factor)}"'

    @staticmethod
    def crop(size: tuple, origin: tuple):
        """
        Crop the video to a new with the provided 'size'
        starting with the top left corner at the given
        'origin' position of the original video.
        
        Notation: **-vf "crop=size[0]:size[1]:origin[0]:origin[1]"**
        """
        return f"-vf \"crop={str(int(size[0]))}:{str(int(size[1]))}:{str(int(origin[0]))}:{str(int(origin[1]))}\""
    
    @staticmethod
    def seeking(seconds: int):
        """
        Skip the necessary amount of time to go directly
        to the provided 'seconds' time of the input (that
        must be provided after this).

        Notation: **-ss 00:00:03**
        """
        return f'-ss {seconds_to_hh_mm_ss(seconds)}'
    
    @staticmethod
    def to(seconds: int):
        """
        Used with 'seeking' to match the duration we want
        to apply to the new trimmed input. In general, 
        this will be the amount of 'seconds' to be played.

        Notation: **-to 00:00:05**
        """
        return f'-to {seconds_to_hh_mm_ss(seconds)}'
    
class FfmpegCommand:
    """
    Class to represent a command to be built and
    executed by the FfmpegHandler.

    A valid example of a command is built like this:
    
    FfmpegCommand([
        FfmpegFlag.force_format(FfmpegVideoFormat.CONCAT),
        FfmpegFlag.safe_routes(0),
        FfmpegFlag.overwrite,
        FfmpegFlag.frame_rate(frame_rate),
        FfmpegFlag.input(concat_filename),
        FfmpegFlag.video_codec(FfmpegVideoCodec.QTRLE),
        FfmpegFlag.pixel_format(pixel_format), # I used 'argb' in the past
        output_filename
    ])
    """
    args: list[Union[FfmpegFlag, any]] = None
    
    def __init__(self, args: list[Union[FfmpegFlag, any]]):
        # TODO: Validate args
        self.args = args

    def run(self):
        """
        Run the command.
        """
        run(self.__str__())

    def __str__(self):
        """
        Turn the command to a string that can be directly
        executed as a ffmpeg command.
        """
        # TODO: Clean args (?)
        # Remove 'None' args, our logic allows them to make it easier
        args = [arg for arg in self.args if arg is not None]

        return f"ffmpeg {' '.join(args)}"

class FfmpegHandler:
    """
    Class to simplify and encapsulate ffmpeg functionality.
    """
    @staticmethod
    def validate_video_filename(video_filename: str):
        # TODO: Validate and raise Exception if invalid
        pass

    @staticmethod
    def write_concat_file(filenames: str):
        """
        Writes the files to concat in a temporary text file with
        the required format and returns that file filename. This
        is required to use different files as input.
        """
        text = ''
        for filename in filenames:
            text += f"file '{filename}'\n"

        # TODO: Maybe this below is interesting for the 'yta_general_utils.file.writer'
        # open('concat.txt', 'w').writelines([('file %s\n' % input_path) for input_path in input_paths])
        filename = Temp.create_filename('concat_ffmpeg.txt')
        FileWriter.write_file(text, filename)

        return filename

    @staticmethod
    def run_command(command: Union[list[FfmpegFlag, any], FfmpegCommand]):
        """
        Runs the provided ffmpeg 'command'.
        """
        if not PythonValidator.is_instance(command, FfmpegCommand):
            command = FfmpegCommand(command)

        command.run()

    # TODO: Check this one below
    @staticmethod
    def get_audio_from_video_deprecated(
        video_filename: str,
        codec: FfmpegAudioCodec = None,
        output_filename: Union[str, None] = None
    ):
        """
        Exports the audio of the provided video to a local file named
        'output_filename' if provided or as a temporary file.

        # TODO: This has not been tested yet.

        This methods returns a tuple with the audio as a moviepy audio 
        in the first place and the filename of the file generated in
        the second place.
        """
        FfmpegHandler.validate_video_filename(video_filename)
        
        output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)

        if codec:
            codec = FfmpegAudioCodec.to_enum(codec)

        FfmpegCommand([
            FfmpegFlag.input(video_filename),
            FfmpegFlag.audio_codec(codec) if codec else None,
            output_filename
        ]).run()

        # TODO: This was .to_audiofileclip() before,
        # remove this comment if working
        return AudioParser.as_audioclip(output_filename), output_filename
    
    @staticmethod
    def get_audio_from_video(video_filename: str, output_filename: str = None):
        """
        Exports the audio of the provided video to a local file named
        'output_filename' if provided or as a temporary file.

        This methods returns a tuple with the audio as a moviepy audio 
        in the first place and the filename of the file generated in
        the second place.
        """
        FfmpegHandler.validate_video_filename(video_filename)
        
        output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)

        # TODO: Verify valid output_filename extension

        FfmpegCommand([
            FfmpegFlag.input(video_filename),
            FfmpegFlag.map('0:1'),
            output_filename
        ]).run()

        # TODO: This was .to_audiofileclip() before,
        # remove this comment if working
        return AudioParser.as_audioclip(output_filename), output_filename

    @staticmethod
    def get_best_thumbnail(video_filename: str, output_filename: str = None):
        """
        Gets the best thumbnail of the provided 'video_filename'.

        This methods returns a tuple with the thumbnail as a pillow 
        image in the first place and the filename of the file generated
        in the second place.
        """
        FfmpegHandler.validate_video_filename(video_filename)

        output_filename = Output.get_filename(output_filename, FileTypeX.IMAGE)

        FfmpegCommand([
            FfmpegFlag.input(video_filename),
            FfmpegFlag.filter(FfmpegFilter.THUMBNAIL),
            output_filename
        ]).run()

        return ImageParser.to_pillow(output_filename), output_filename
    
    @staticmethod
    def concatenate_videos(video_filenames: str, output_filename: str = None):
        """
        Concatenates the provided 'video_filenames' in the order in
        which they are provided.

        This methods returns a tuple with the new video as a moviepy
        video in the first place and the filename of the file generated
        in the second place.
        """
        for video_filename in video_filenames:
            FfmpegHandler.validate_video_filename(video_filename)

        output_filename = Output.get_filename(output_filename, FileTypeX.VIDEO)

        concat_filename = FfmpegHandler.write_concat_file(video_filenames)

        FfmpegCommand([
            FfmpegFlag.overwrite,
            FfmpegFlag.force_format(FfmpegVideoFormat.CONCAT),
            FfmpegFlag.safe_routes(0),
            FfmpegFlag.input(concat_filename),
            FfmpegFlag.codec('copy'),
            output_filename
        ]).run()

        return VideoParser.to_moviepy(output_filename), output_filename
    
    @staticmethod
    def concatenate_images(image_filenames: str, frame_rate = 60, pixel_format: FfmpegPixelFormat = FfmpegPixelFormat.YUV420p, output_filename: str = None):
        """
        Concatenates the provided 'image_filenames' in the order in
        which they are provided.

        This methods returns a tuple with the new video as a moviepy
        video in the first place and the filename of the file generated
        in the second place.
        """
        for image_filename in image_filenames:
            FfmpegHandler.validate_video_filename(image_filename)

        output_filename = Output.get_filename(output_filename, FileTypeX.VIDEO)

        concat_filename = FfmpegHandler.write_concat_file(image_filenames)

        # TODO: Should we check the pixel format or give freedom (?)
        # pixel_format = FfmpegPixelFormat.to_enum(pixel_format)

        FfmpegCommand([
            FfmpegFlag.force_format(FfmpegVideoFormat.CONCAT),
            FfmpegFlag.safe_routes(0),
            FfmpegFlag.overwrite,
            FfmpegFlag.frame_rate(frame_rate),
            FfmpegFlag.input(concat_filename),
            FfmpegFlag.video_codec(FfmpegVideoCodec.QTRLE),
            FfmpegFlag.pixel_format(pixel_format), # I used 'argb' in the past
            output_filename
        ]).run()

        return VideoParser.to_moviepy(output_filename), output_filename

    @staticmethod
    def resize_video(video_filename: str, size: tuple, output_filename: Union[str, None] = None):
        """
        Resize the provided 'video_filename', by keeping
        the aspect ratio (cropping if necessary), to the
        given 'size' and stores it locally as
        'output_filename'.

        See more: 
        https://www.gumlet.com/learn/ffmpeg-resize-video/
        """
        if not PythonValidator.is_string(video_filename):
            raise Exception('The provided "video_filename" parameter is not a valid string.')
        
        if not PythonValidator.is_tuple(size):
            raise Exception('The provided "size" parameter is not a tuple.')
        
        if not PythonValidator.is_string(output_filename):
            raise Exception('The provided "output_filename" parameter is not a valid string.')
        
        if not FileValidator.file_is_video_file(video_filename):
            raise Exception('The provided "video_filename" is not a valid video file name.')
        
        output_filename = Output.get_filename(output_filename, FileTypeX.VIDEO)

        validate_size(size, 'size')

        w, h = get_video_size(video_filename)

        if (w, h) == size:
            # No need to resize, we just copy it to output
            FileHandler.copy_file(video_filename, output_filename)
        else:
            # First, we need to know if we need to scale it
            original_ratio = w / h
            new_ratio = size[0] / size[1]

            if original_ratio > new_ratio:
                # Original video is wider than the expected one
                new_size = w * (size[1] / h), size[1]
            elif original_ratio < new_ratio:
                # Original video is higher than the expected one
                new_size = size[0], h * (size[0] / w)
            else:
                new_size = size[0], size[1]

            tmp_filename = Temp.create_filename('tmp_ffmpeg_scaling.mp4')

            # Scale to new dimensions
            FfmpegCommand([
                FfmpegFlag.input(video_filename),
                FfmpegFlag.scale_with_size(new_size),
                tmp_filename
            ]).run()

            # Now, with the new video resized, we look for the
            # cropping points we need to apply and we crop it
            top_left, _ = get_cropping_points_to_keep_aspect_ratio(new_size, size)

            # Second, we need to know if we need to crop it
            FfmpegCommand([
                FfmpegFlag.input(tmp_filename),
                FfmpegFlag.crop(size, top_left),
                FfmpegFlag.overwrite,
                output_filename
            ]).run()

        return output_filename
    
    @staticmethod
    def trim(video_filename: str, start_seconds: int, duration_seconds: int, output_filename: Union[str, None] = None):
        """
        Trims the provided 'video_filename' and generates a
        shorter resource that is stored as 'output_filename'.
        This new resource will start from 'start_seconds' and
        last the provided 'duration_seconds'.

        Thank you:
        https://www.plainlyvideos.com/blog/ffmpeg-trim-videos
        https://trac.ffmpeg.org/wiki/Seeking
        """
        if not PythonValidator.is_string(video_filename):
            raise Exception('The provided "video_filename" parameter is not a valid string.')
        
        if not NumberValidator.is_positive_number(start_seconds, do_include_zero = True):
            raise Exception('The provided "start_seconds" is a negative number.')

        if not NumberValidator.is_positive_number(duration_seconds, do_include_zero = True):
            raise Exception('The provided "duration_seconds" is a negative number.')
        
        output_filename = Output.get_filename(output_filename, FileTypeX.VIDEO)

        command = FfmpegCommand([
            FfmpegFlag.seeking(start_seconds),
            FfmpegFlag.input(video_filename),
            FfmpegFlag.to(duration_seconds),
            FfmpegFlag.codec(FfmpegVideoCodec.COPY),
            FfmpegFlag.overwrite,
            output_filename
        ])
        print(command)
        command.run()

        #ffmpeg_command = f'-ss 00:02:05 -i {video} -to 00:03:10 -c copy video-cutted-ffmpeg.mp4'
        return output_filename

    # TODO: This method must replace the one in 
    # yta_multimedia\video\audio.py > set_audio_in_video_ffmpeg
    @staticmethod
    def set_audio(video_filename: str, audio_filename: str, output_filename: Union[str, None] = None):
        if not PythonValidator.is_string(video_filename):
            raise Exception('The provided "video_filename" parameter is not a valid string.')
        
        if not PythonValidator.is_string(audio_filename):
            raise Exception('The provided "audio_filename" parameter is not a valid string.')
        
        if not PythonValidator.is_string(output_filename):
            raise Exception('The provided "output_filename" parameter is not a valid string.')
        
        if not FileValidator.file_is_audio_file(audio_filename):
            raise Exception('The provided "audio_filename" is not a valid audio file name.')
        
        if not FileValidator.file_is_video_file(video_filename):
            raise Exception('The provided "video_filename" is not a valid video file name.')

        output_filename = Output.get_filename(output_filename, FileTypeX.VIDEO)
        
        # cls.run_command([
        #     FfmpegFlag.input(video_filename),
        #     FfmpegFlag.input(audio_filename),
        #     output_filename
        # # TODO: Unfinished
        # ])

        # TODO: Is this actually working (?)
        run(f"ffmpeg -i {video_filename} -i {audio_filename} -c:v copy -c:a aac -strict experimental -y {output_filename}")
        
        # Apparently this is the equivalent command according
        # to ChatGPT, but maybe it doesn't work
        # ffmpeg -i input_video -i input_audio -c:v copy -c:a aac -strict experimental -y output_filename

        # There is also a post that says this:
        # ffmpeg -i input.mp4 -i input.mp3 -c copy -map 0:v:0 -map 1:a:0 output.mp4
        # in (https://superuser.com/a/590210)


        # # TODO: What about longer audio than video (?)
        # # TODO: This is what was being used before FFmpegHandler
        # input_video = ffmpeg.input(video_filename)
        # input_audio = ffmpeg.input(audio_filename)

        # ffmpeg.concat(input_video, input_audio, v = 1, a = 1).output(output_filename).run(overwrite_output = True)

    
    # TODO: Create a 'set_audio_in_video' method to replace the
    # yta_multimedia\video\audio.py > set_audio_in_video_ffmpeg

    # TODO: Keep going

    # https://www.reddit.com/r/ffmpeg/comments/ks8zfs/comment/gieu7x6/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    # https://stackoverflow.com/questions/38368105/ffmpeg-custom-sequence-input-images/51618079#51618079
    # https://stackoverflow.com/a/66014158