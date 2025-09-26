# pip install python-dotenv
import os
from dotenv import load_dotenv, find_dotenv


class Credentials:

    def __init__(self):
        load_dotenv(find_dotenv())

        self.pavlinbl4_bot = os.getenv('PAVLINBL4_BOT')
        self.admin = os.getenv('ADMIN_ID')
