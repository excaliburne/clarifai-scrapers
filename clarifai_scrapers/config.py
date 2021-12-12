# SYSTEM
import os

# PACKAGES
from dotenv import load_dotenv, find_dotenv


class Config:

    def __init__(self):
        self._env = load_dotenv(find_dotenv())
    

    def get(self, key):
        return os.environ.get(key)