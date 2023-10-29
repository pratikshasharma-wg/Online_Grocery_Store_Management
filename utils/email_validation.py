import re
from config.config import Config

def valid_email():
    while True:
        email = input(Config.ASK_FOR_EMAIL)
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,7}$'
        if(re.match(pattern, email)):
            return email