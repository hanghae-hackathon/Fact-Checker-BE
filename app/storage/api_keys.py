import os
from dotenv import load_dotenv

class APIKeys:
    @staticmethod
    def load_key(key_name):
        load_dotenv()
        return os.getenv(key_name)