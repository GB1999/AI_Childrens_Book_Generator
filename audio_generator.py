
import os
import torch
import torchaudio
from transformers import AutoModelForCausalLM, AutoTokenizer
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voice
from pathlib import Path
import json
from time import time
class AudioGenerator:
    def __init__(self, story_path):
        self._scenes = {}
        self._load_scenes(story_path)
        self._story_path = story_path

    def _load_scenes(self, story_path):
        story_json = json.load(open(story_path + "/details.json"))
        self._scenes = story_json["Scenes"]

    def generate_audio(self):
        seed = int(time())
        tts = TextToSpeech()

        for scene in self._scenes.keys():
            save_path = os.path.join(self._story_path, scene, "Audio.wav")
            scene_audio = tts.tts_with_preset(text=self._scenes[scene]["Text"], preset='ultra_fast', voice="emma", use_deterministic_seed = seed)
            torchaudio.save(save_path,  scene_audio.squeeze(0).cpu(), 24000)
