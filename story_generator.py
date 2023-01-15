
import json
import os
import random
from collections import ChainMap

import openai
import base64
import re
class StoryGenerator:
    def __init__(self, config_path):
        self._api_key : str = None
        self._chat_history = []
        self._story = {}

        self.load_config(config_path)

        self._commands = {
            "brainstorm": "Brainstorm 5 ideas for a children's story book with a title and description. Your response should be in unformatted JSON",
            "write": "Write a children's story about ",
            "describe" : "For each scene in the story, give an audio description. Your response should be in unformatted JSON"
        }

    def load_config(self, config_path):
        # load login credentials from json file
        if os.path.exists(config_path):
            self._config_path = config_path
            try:
                config = {}
                with open(config_path, "r") as f:
                    config.update(json.load(f))

                for key, value in config.items():
                    if value is not None:
                        if hasattr(self, "_{}".format(key)):
                            setattr(self, "_{}".format(key), value)

                if self._api_key:
                    openai.api_key = self._api_key

            except Exception as e:
                print(e)


    def pick_story(self):
        story_ideas = self.text_gen(prompt="Brainstorm 5 ideas for a children's story book with a title and description. Your response should be in unformatted JSON" + "\n" , prefix= """[{ "Title" : """, max_tokens=2048)
        story_ideas_stripped = story_ideas[story_ideas.index('['):]
        print(story_ideas_stripped)
        story_ideas_json = json.loads(story_ideas_stripped)
        self._story = story_ideas_json[random.randint(0,4)]

        self._story["text"] = self.text_gen(prompt = "Write a children's story about " + self._story["Description"] + "Separate each scene. Your response should be in unformatted JSON" + "\n" , prefix="""[{ "Scene 1" : """, max_tokens=2048)

        print(self._story["text"])
        scenes_json = json.loads(self._story["text"])
        scenes_json = dict(ChainMap(*scenes_json))

        print(scenes_json)

        self._story["scenes"] = {}
        for key in scenes_json.keys():
            self._story["Scenes"][key] = {"Text": scenes_json[key]}



    def visualize_story(self):
        descriptions = self.text_gen(self._story["text"] + "\n" +
                            "For each scene in the story, give an visual description without names or context. Your response should be in unformatted JSON" + "\n"
                            , prefix="""[{ "Scene 1" : """,  max_tokens=3500 )

        descriptions_json = json.loads(descriptions)
        descriptions_json = dict(ChainMap(*descriptions_json))
        for key in descriptions_json.keys():
            self._story["Scenes"][key]["Description"] = descriptions_json[key]

        for key in self._story["Scenes"].keys():
            self.image_gen(prompt=self._story["Scenes"][key]["Description"], file_name=key)
        print(self._story)




    def text_gen(self, prompt,  max_tokens, prefix = "", linebreak = False):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=  prompt + prefix,
            temperature=.5,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0
        )
        raw_response = response['choices'][0]['text']

        if linebreak:
            return prefix + response['choices'][0]['text']

        return prefix + response['choices'][0]['text'].replace('\n', '')

    def image_gen(self, prompt, file_name):
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024",
                response_format="b64_json"
            )

            image_b64 = bytes(response['data'][0]['b64_json'], encoding='utf-8')
            self.save_image(b64_str= image_b64, file_name = file_name)

        except openai.error.OpenAIError as e:
            print(e.http_status)

    def save_image(self, b64_str, file_name):
        with open(file_name + "png", "wb") as fh:
            fh.write(base64.decodebytes(b64_str))

