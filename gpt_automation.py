import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

import os
import json



class GPT:
    _options: Options = None
    _config: str = None
    _urls = {"login": "https://chat.openai.com/auth/login", "home": "https://openai.com/blog/chatgpt/", "chat":"https://chat.openai.com/"}
    _driver = None
    _user_agent:UserAgent = None

    def __init__(
        self,
        config_path
    ):

        if config_path is not None:
            self.load_config(config_path)

        self._user_agent = UserAgent().random

        self._options = Options()
        self._options.add_argument(f'user-agent={self._user_agent}')
        self._driver = webdriver.Chrome(options=self._options, executable_path= './chromedriver')
        self._driver.maximize_window()



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

                return config

            except Exception as e:
                print(e)

    def verify_humanity(self):
        print("check")
        time.sleep(10)

    def login(self):
        wait = WebDriverWait(self._driver, 100)
        short_wait = WebDriverWait(self._driver, 5)

        self._driver.get(self._urls['home'])
        self._driver.implicitly_wait(10)

        try_button = self._driver.find_element(By.XPATH, '//a[@href="'+self._urls['chat']+'"]')
        try_button.click()

        challenge_running = self._driver.find_element(By.ID, 'challenge-running')
        # while challenge_running.is_displayed():
        #     self.verify_humanity()

        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Log')]")))
        login_button.click()

        google_login = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@ndata-provider="google"]')))
        google_login.click()


chatGPT = GPT('config.json')
chatGPT.login()
