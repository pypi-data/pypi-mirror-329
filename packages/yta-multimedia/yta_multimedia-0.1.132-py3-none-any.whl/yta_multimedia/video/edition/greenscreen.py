from yta_image.greenscreen.remover import ImageGreenscreenRemover
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.utils.ffmpeg_handler import FfmpegHandler, FfmpegPixelFormat
from yta_general_utils.temp import Temp
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileExtension
from typing import Union
from moviepy.Clip import Clip


def remove_greenscreen_from_video(
    video: Clip,
    output_filename: Union[str, None] = None
):
    """
    Removes the green screen from the 'video' video so
    you get a final 'output_filename' video with transparent
    layer.
    """
    video = VideoParser.to_moviepy(video)
    
    # TODO: I think I need to write the frame filenames in a file to be used
    # with the concat flag and ffmpeg library

    # Export all frames
    original_frames_array = []
    for frame in video.iter_frames():
        frame_name = Temp.create_custom_filename('tmp_frame_' + str(len(original_frames_array)) + '.png')
        original_frames_array.append(frame_name)
    video.write_images_sequence(Temp.create_custom_filename('tmp_frame_%01d.png'), logger = 'bar')

    # Remove green screen of each frame and store it
    processed_frames_array = []
    for index, frame in enumerate(original_frames_array):
        tmp_frame_filename = Temp.create_custom_filename('tmp_frame_processed_' + str(index) + '.png')
        processed_frames_array.append(tmp_frame_filename)
        ImageGreenscreenRemover.remove_greenscreen_from_image(frame, tmp_frame_filename)

    output_filename = Output.get_filename(output_filename, FileExtension.MOV)
    # TODO: What if 'output_filename' is not .mov but it has transparency,
    # maybe we should force '.mov'

    video, _ = FfmpegHandler.concatenate_images(processed_frames_array, frame_rate = 30, pixel_format = FfmpegPixelFormat.YUV420p, output_filename = output_filename)

    return video

    #parameters = ['ffmpeg', '-y', '-i', Temp.create_custom_filename('tmp_frame_processed_%01d.png'), '-r', '30', '-pix_fmt', 'yuva420p', output_filename]
    #run(parameters)
        
    # https://stackoverflow.com/a/77608713
    #ImageSequenceClip(processed_frames_array, fps = clip.fps).with_audio(clip.audio).write_videofile(output_filename, codec = 'hap_alpha', ffmpeg_params = ['-c:v', 'hap', '-format', 'hap_alpha', '-vf', 'chromakey=black:0.1:0.1'])
    # https://superuser.com/questions/1779201/combine-pngs-images-with-transparency-into-a-video-and-merge-it-on-a-static-imag
    # ffmpeg -y -i src/tmp/%d.png -c:v libx264 -vf fps=25 -pix_fmt yuva420p land.mov
    
    #clip = ImageSequenceClip(processed_frames_array, fps = clip.fps).with_audio(clip.audio).write_videofile(output_filename, codec = 'libx264', audio_codec = 'aac', temp_audiofile = 'temp-audio.m4a', remove_temp = True)