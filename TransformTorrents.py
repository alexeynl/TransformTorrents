import glob, os
from pathlib import Path
from ffmpeg import FFmpeg, Progress
from shlex import quote
import re
import Settings

def __transform(video, outpath):
        ffmpeg_inputs = []
        ffmpeg_inputs.append(video['filepath'])
        ffmpeg_inputs.append(video['audio_tracks'])
        ffmpeg_inputs.append(video['subtitles'])
        ffmpeg_output_path = os.path.join(Settings.transformed_path, video['filename']) + ".mkv"
        map = ["0:0", "0:1"]
        ffmpeg = (
            FFmpeg()
            .option("y")
            .option("hwaccel", "d3d11va")
            .input(video['filepath'])
        )

        ffmpeg._executable = Settings.ffmpeg_exec_path
        
        i = 1

        for audio_track in video['audio_tracks']:
              ffmpeg.input(audio_track)
              map.append(str(i) + ":a")
              i += 1

        for subtitle in video['subtitles']:
              ffmpeg.input(subtitle)
              map.append(str(i) + ":s")
              i += 1
        #vf2 = "ass=" + r"\'C:\\Users\\homeadmin\\Downloads\\Anime\\Vinland.Saga.Season2.WEBRip.1080p\\transformed\\test.ass\'"
        #vf1 = "ass=" + r"\'" + r"C:\\Users\\homeadmin\\Downloads\\Anime\\Vinland.Saga.Season2.WEBRip.1080p\\\test\[1\] test.ass" + r"\'"
        #vf1 = "ass=" + r"\'" + video['subtitles'][0].replace("\\", "\\\\").replace("[",r"\[").replace("]",r"\]").replace(":","\:") + r"\'"
        #vf3 = "ass=" + quote(r"C:\Users\homeadmin\Downloads\Anime\Vinland.Saga.Season2.WEBRip.1080p\test[1] test.ass")
        if len(video['subtitles']) > 0:
              vf = "ass=" + r"\'" + re.escape(video['subtitles'][0]) + r"\'"
        
        ffmpeg.output(
            ffmpeg_output_path,
            {"codec:v": "hevc_amf", "qp_p": "15", "qp_i": "15", "codec:a": "copy", "codec:a": "copy"},
            vf = vf,
            map = map
        )
        
        #ffmpeg.
        #@ffmpeg.on("progress")
        #def on_progress(progress: Progress):
        #        print(progress)
        ffmpeg.execute()
        
        


#transformed_path = "C:\\transformed"


audio_extensions = [".mka"]
subtitle_extensions = [".ass"]

all_files_paths = glob.glob(Settings.torrent_path + '\\**\\*', recursive=True)

video_paths = []

video_paths = list (filter(lambda x:x.endswith(".mkv"), all_files_paths))

for video_path in video_paths:
    video_file_name = Path(video_path).stem
    related_files = list (filter(lambda x:Path(x).stem==video_file_name, all_files_paths))
    audio_tracks = list (filter(lambda x:Path(x).suffix in audio_extensions, related_files))
    subtitles = list (filter(lambda x:Path(x).suffix in subtitle_extensions, related_files))
    video = {'filename': video_file_name, 'filepath': video_path, 'audio_tracks': audio_tracks, 'subtitles': subtitles }
    __transform(video, Settings.transformed_path)
    print (video)



#print (video_paths)