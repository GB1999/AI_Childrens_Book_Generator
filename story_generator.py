
import json
import os
import random
from collections import ChainMap
from pathlib import Path

import nltk
import openai
import base64
import re
import numpy as np
import cv2
import textwrap
from  nltk import tokenize

class StoryGenerator:
    def __init__(self, config_path):
        self._api_key : str = None
        self._directory : str = None
        self._chat_history = []
        self._story = {}

        self._page_height :int = None
        self._page_width :int = None

        self._font_size: int = None
        self._font_thickness: int = None

        self._load_config(config_path)


        os.chdir(os.path.dirname(__file__))

    def _load_config(self, config_path):

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
        story_ideas = self._generate_text(prompt="Brainstorm 5 ideas for a children's story book with a title and description. Your response should be in unformatted JSON" + "\n", prefix="""[{ "Title" : """, max_tokens=2048)
        story_ideas_stripped = story_ideas[story_ideas.index('['):]
        print(story_ideas_stripped)
        story_ideas_json = json.loads(story_ideas_stripped)

        # assumes story ideas follows {title:"", description:""} structure
        self._story = story_ideas_json[random.randint(0,4)]

        # save directory for later use

        self._directory = os.path.join(os.getcwd(), "Stories", self._story["Title"].replace(" ", "_"))
        os.mkdir(self._directory)

        self._story["Text"] = self._generate_text(prompt ="Write a children's story about " + self._story["Description"] + "Separate each scene. Your response should be in unformatted JSON" + "\n", prefix="""[{ "Scene_1" : """, max_tokens=2048)

        print(self._story["Text"])
        scenes_json = json.loads(self._story["Text"])
        scenes_json = dict(ChainMap(*scenes_json))

        print(scenes_json)

        self._story["Scenes"] = {}
        for key in scenes_json.keys():
            self._story["Scenes"][key] = {"Text": scenes_json[key]}



    def generate_images(self):
        descriptions = self._generate_text(self._story["Text"] + "\n" +
                            "For each scene in the story, give an visual description without names or context. Your response should be in unformatted JSON" + "\n"
                                           , prefix="""[{ "Scene_1" : """, max_tokens=3500)

        descriptions_json = json.loads(descriptions)
        descriptions_json = dict(ChainMap(*descriptions_json))
        for scene in descriptions_json.keys():
            self._story["Scenes"][scene]["Description"] = descriptions_json[scene]

        # make Path for images
        # path = Path(os.getcwd() + "/Stories/" + self._story["Title"].replace(" ", "_") + "/Images")
        # path.mkdir(parents=True)
        #
        # path = Path(os.getcwd() + "/Stories/" + self._story["Title"].replace(" ", "_") + "/Pages")
        # path.mkdir(parents=True)

        for scene in self._story["Scenes"].keys():
            scene_path = os.path.join(self._directory, scene)
            os.mkdir(scene_path)

            image_b64 = self._generate_image(prompt=self._story["Scenes"][scene]["Description"] + ",watercolor, storybook, illustration", file_name=os.path.join(scene_path, "Image.png"))

            np_arr = np.fromstring(base64.decodebytes(image_b64), np.uint8)
            image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            self._generate_page(image_np, self._story["Scenes"][scene]["Text"], int(scene.lstrip("Scene_")))




    def _generate_text(self, prompt, max_tokens, prefix ="", linebreak = False):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=  prompt + prefix,
            temperature=.5,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0
        )
        print(response)

        if linebreak:
            return prefix + response['choices'][0]['text']

        return prefix + response['choices'][0]['text'].replace('\n', '')

    def _generate_image(self, prompt, file_name):
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512",
                response_format="b64_json"
            )

            image_b64 = bytes(response['data'][0]['b64_json'], encoding='utf-8')
            self.save_image(b64_str= image_b64, file_name = file_name)
            return image_b64

        except openai.error.OpenAIError as e:
            print(e.http_status)

    def _generate_page(self, image, text, index):
        blank_page = 255 * np.ones((self._page_height, self._page_width, 3), np.uint8)
        background_image = cv2.resize(image, (self._page_width, self._page_width), interpolation=cv2.INTER_AREA)
        background_image = cv2.GaussianBlur(background_image,(49,49),50)
        background_image = background_image[0:self._page_height, 0:self._page_width]
        background_image = cv2.addWeighted(background_image, .5, blank_page, 0.1, 0)

        image_feathered = self._feather_image(image, 50)
        h, w, c = image_feathered.shape

        index_offset = ((index % 2 * 2) + 1)
        even = index % 2 == 0

        print(f'index offset is {index_offset}')

        offset_x = int(abs((index_offset * (self._page_width/4)) - w/2) )
        offset_y = int(abs(self._page_height/4 - h/2))

        print(f'offset is {(offset_x, offset_y)}')

        # alpha channel from feathered image
        alpha_mask = image_feathered[:, :, 3] / 255.0

        #color channel for result
        img_result = background_image[:, :, :3].copy()
        img_overlay = image_feathered[:, :, :3]

        self.overlay_image_alpha(img_result, img_overlay, offset_x, offset_y, alpha_mask)

        if even:
            img_result[:, int(self._page_width/2):self._page_width,:3 ] = 255
        else:
            img_result[:, 0:int(self._page_width / 2), :3] = 255


        final_page = self._add_page_text(img_result, text, cv2.FONT_HERSHEY_TRIPLEX, index, 10)
        cv2.imwrite(os.path.join(self._directory, "Scene_"+str(index), "Page.png"), final_page)

    def _add_page_text(self, image, text, font, index, spacing):
        #split text into sentences
        sentences = tokenize.sent_tokenize(text)
        sentence_offset = 0
        sentence_heights = [0] * (len(sentences) + 1)
        h,w,c = image.shape

        # calculate total space for paragraph
        for i, sentence in enumerate(sentences):
            wrapped_text = textwrap.wrap(sentence, width=30)

            # for each line in textwrap, add height to sentence height
            for j, line in enumerate(wrapped_text):
                textsize = cv2.getTextSize(line, font, self._font_size, self._font_thickness)[0]
                sentence_heights[i+1] += textsize[1] + spacing
                print(f"line {line} has a text size of {textsize}")

            sentence_heights[i + 1] += 30
        paragraph_height = sum(sentence_heights)

        for i, sentence in enumerate(sentences):
            sentence_count = 0
            wrapped_text = textwrap.wrap(sentence, width=30)

            # for each line in textwrap, put line on image with offset
            for j, line in enumerate(wrapped_text):
                textsize = cv2.getTextSize(line, font, self._font_size, self._font_thickness)[0]
                index_offset = ((index % 2 * -2) + 3)
                gap = textsize[1] + 10
                sentence_count += 1

                print(sentence_heights)
                y = int((h -paragraph_height)/2) + (j * gap) + sum(sentence_heights[:i+1])
                #y = int((image.shape[0] + textsize[1]) / 2) + ((j-int(len(wrapped_text)/2)) * gap) + sentence_offset
                x = int(abs((index_offset * (self._page_width/4) - textsize[0]/2)))

                print(f'placing sentence {i} line {j} at {(x,y)} with an offset of {sum(sentence_heights[:i])}')

                cv2.putText(image, line, (x, y), font,
                            self._font_size,
                            (0, 0, 0),
                            self._font_thickness,
                            lineType=cv2.LINE_AA)


        return image

    def _feather_image(self, image, border_size):
        # create mask defined by image size and border_size
        h,w,c = image.shape

        border_mask = 255 * np.ones(shape=(h,w,1), dtype=np.uint8)
        border_mask = cv2.copyMakeBorder(border_mask, top=border_size, bottom=border_size, left=border_size, right=border_size, borderType=cv2.BORDER_CONSTANT, value=[0,0,0])
        border_mask_blurred = cv2.GaussianBlur(border_mask,(21,21),50)
        border_mask_blurred = cv2.resize(border_mask_blurred, (w,h), interpolation=cv2.INTER_AREA)

        # create rgba image from mask
        image_rgba = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
        image_rgba[:, :, 3] = border_mask_blurred


        return image_rgba

    def overlay_image_alpha(self, img, img_overlay, x, y, alpha_mask):
        """Overlay `img_overlay` onto `img` at (x, y) and blend using `alpha_mask`.

        `alpha_mask` must have same HxW as `img_overlay` and values in range [0, 1].
        """
        # Image ranges
        y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
        x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

        # Overlay ranges
        y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
        x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

        # Exit if nothing to do
        if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
            return

        # Blend overlay within the determined ranges
        img_crop = img[y1:y2, x1:x2]
        img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]
        alpha = alpha_mask[y1o:y2o, x1o:x2o, np.newaxis]
        alpha_inv = 1.0 - alpha

        img_crop[:] = alpha * img_overlay_crop + alpha_inv * img_crop

    def save_image(self, b64_str, file_name):
        with open(file_name, "wb") as fh:
            fh.write(base64.decodebytes(b64_str))

    def save_details(self):
        with open("Stories/" + self._story["Title"].replace(" ", "_") + "/details.json", 'w') as fp:
            json.dump(self._story, fp)

    def get_dir(self):
        return self._directory
