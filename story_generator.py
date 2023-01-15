
import json
import os
import random

import openai
import base64

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
        story_ideas = json.loads(self.text_gen("Brainstorm 5 ideas for a children's story book with a title and description. Your response should be in unformatted JSON"))
        self._story = story_ideas[random.randint(0,4)]


        self._story["text"] = self.text_gen("Write a children's story about " + self._story["description"])


    def visualize_story(self):




    def text_gen(self, prompt):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt= prompt,
            temperature=(random.randint(0,9)/10),
            max_tokens=2038,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0
        )
        raw_response = response['choices'][0]['text']
        print(response['choices'][0]['text'].replace('\n', ''))
        return response['choices'][0]['text'].replace('\n', '')

    def image_gen(self, prompt):
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024",
                response_format="b64_json"
            )

            image_b64 = bytes(response['data'][0]['b64_json'], encoding='utf-8')
            self.save_image(image_b64)

        except openai.error.OpenAIError as e:
            print(e.http_status)

    def save_image(self, b64_str):
        with open("imageToSave.png", "wb") as fh:
            fh.write(base64.decodebytes(b64_str))

