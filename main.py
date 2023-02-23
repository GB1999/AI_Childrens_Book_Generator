# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from story_generator import StoryGenerator
from audio_generator import AudioGenerator
from video_generator import VideoGenerator
# Press the green button in the gutter to run the script.
import os
import torch
import torchaudio
from transformers import AutoModelForCausalLM, AutoTokenizer
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voice

if __name__ == '__main__':
    sg = StoryGenerator("config.json")
    sg.pick_story()

    # sg.generate_images()
    # sg.save_details()

    # story_dir = sg.get_dir()
    # ag = AudioGenerator(r"B:\Coding Projects\Python\YouTube\bookGenerator\Stories\The_Adventures_of_Little_Red_Riding_Hood")
    # ag.generate_audio()

    # vg = VideoGenerator(r"B:\Coding Projects\Python\YouTube\bookGenerator\Stories\The_Brave_Little_Princess")

# voice_samples, conditioning_latents = load_voice('rick', extra_voice_dirs=['voices'])
# tts = TextToSpeech()
# gen = tts.tts_with_preset("I turned myself into an inmate Morty! I'm inmate Rick!", voice_samples=voice_samples, conditioning_latents=conditioning_latents,
#                           preset='standard')
# torchaudio.save('standard.wav', gen.squeeze(0).cpu(), 24000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
