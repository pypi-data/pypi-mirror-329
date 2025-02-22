from moviepy.editor import VideoFileClip

Video = "avi"

def clip(input_file, output_file, start_time, end_time):
    """视频剪辑"""
    try:
        video = VideoFileClip(input_file)
        clipped_video = video.subclip(start_time, end_time)
        clipped_video.write_videofile(output_file, codec='png')
        video.close()
        clipped_video.close()
    except Exception as e:
        print(f"视频剪辑过程中出现错误: {e}")


def convert(input_file, output_file):
    """视频格式转换"""
    try:
        video = VideoFileClip(input_file)
        video.write_videofile(output_file, codec='png')
        video.close()
    except Exception as e:
        print(f"视频格式转换过程中出现错误: {e}")


def extract_audio(input_file, output_file):
    """音频提取"""
    try:
        video = VideoFileClip(input_file)
        audio = video.audio
        audio.write_audiofile(output_file)
        video.close()
        audio.close()
    except Exception as e:
        print(f"音频提取过程中出现错误: {e}")


from moviepy.editor import TextClip, CompositeVideoClip
import pysrt

def subtitles(input_file, output_file, subtitle_file):
    """添加字幕"""
    try:
        video = VideoFileClip(input_file)
        subs = pysrt.open(subtitle_file)
        clips = []
        for sub in subs:
            text_clip = TextClip(sub.text, fontsize=24, color='white', bg_color='black')
            text_clip = text_clip.set_start(sub.start.seconds + sub.start.milliseconds / 1000)
            text_clip = text_clip.set_end(sub.end.seconds + sub.end.milliseconds / 1000)
            text_clip = text_clip.set_position(('center', 'bottom'))
            clips.append(text_clip)
        final_clip = CompositeVideoClip([video] + clips)
        final_clip.write_videofile(output_file, codec='png')
        video.close()
        final_clip.close()
    except Exception as e:
        print(f"字幕添加过程中出现错误: {e}")


from moviepy.editor import concatenate_videoclips

def merge_videos(input_files, output_file):
    """合并视频"""
    try:
        clips = [VideoFileClip(file) for file in input_files]
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(output_file, codec='png')
        for clip in clips:
            clip.close()
        final_clip.close()
    except Exception as e:
        print(f"视频合并过程中出现错误: {e}")


def adjust_video_speed(input_file, output_file, speed_factor):
    """调整视频速度,1是正常速度"""
    try:
        video = VideoFileClip(input_file)
        new_video = video.fx(VideoFileClip.speedx, speed_factor)
        new_video.write_videofile(output_file, codec='png')
        video.close()
        new_video.close()
    except Exception as e:
        print(f"调整视频播放速度时出现错误: {e}")


def split_video(input_file, output_prefix, segment_duration):
    """分割视频,segment_duration是每个片段的时长"""
    try:
        video = VideoFileClip(input_file)
        total_duration = video.duration
        segment_num = 0
        start_time = 0

        while start_time < total_duration:
            end_time = start_time + segment_duration
            if end_time > total_duration:
                end_time = total_duration
            segment = video.subclip(start_time, end_time)
            output_file = f"{output_prefix}_{segment_num}.avi"
            segment.write_videofile(output_file, codec='png')
            segment.close()
            start_time = end_time
            segment_num += 1

        video.close()
    except Exception as e:
        print(f"视频分割过程中出现错误: {e}")


def merge_videos_moviepy(input_files, output_file):
    """合并视频"""
    try:
        clips = [VideoFileClip(file) for file in input_files]
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(output_file, codec='png')
        for clip in clips:
            clip.close()
        final_clip.close()
    except Exception as e:
        print(f"合并视频时出现错误: {e}")