import cv2
import numpy as np
from pathlib import Path
import json
from moviepy.editor import *
import os
class VideoGenerator:
    def __init__(self, story_path):
        self._scenes = {}

        self._video = {}
        self._video_path = story_path + "/Video"
        self._load_audio(story_path)

        # path = Path(self._video_path)
        # path.mkdir(parents=True)

    def _load_audio(self, story_path):
        pass
        scenes = [f.name for f in os.scandir(story_path) if f.is_dir()]
        scene_videos = []
        video_size = None
        for i, scene in enumerate(scenes):
            break_audio = AudioClip(duration=1)
            scene_audio = AudioFileClip(os.path.join(story_path, scene, "Audio.wav"))
            scene_video = ImageClip(os.path.join(story_path, scene, "Page.png"), duration=int(scene_audio.duration) + 2)
            scene_video = scene_video.set_position(lambda t: ('center', t * 10 + 50))
            scene_video.fps = 30
            scene_video.crossfadein(2.0)

            scene_video.audio = scene_audio
            scene_videos.append(scene_video)
            video_size = scene_video.size




        composite = concatenate_videoclips(scene_videos)
        composite.write_videofile(os.path.join(story_path, "Video.mp4"))

        # for path, directories, files in os.walk(story_path):
            #
            # for file in files:
            #     scene, extension = os.
            #     print(os.path.join(path, file))

        # audio_path = story_path + "/Audio"
        # page_path = story_path + "/Pages"
        # for filename in os.listdir(path=audio_path):
        #     print(filename)
        #     scene = Path(filename).stem
        #     # self._video[scene] = {}
        #     # self._video[scene]["Audio"] = AudioFileClip(filename)











