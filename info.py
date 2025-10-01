import re, time
from os import environ
 

id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.strip().lower() in ["on", "true", "yes", "1", "enable", "y"]: return True
    elif value.strip().lower() in ["off", "false", "no", "0", "disable", "n"]: return False
    else: return default


DATABASE_NAME = environ.get('DATABASE_NAME', "Mrsyd")
DATABASE_URL = environ.get('DATABASE_URL', "")
API_ID = environ.get('API_URL', "")
API_HASH = environ.get('API_URI', "")
TELETHON_SESSION = environ.get('TELETHON_SESSION', "")
PHONE_NUMBER = environ.get('NUMB', "")
SOURCE_CHAT_ID = -1002295881345  # Replace with source chat ID
DESTINATION_CHAT_ID = -1002377676305
auth_channel = environ.get('AUTH_CHANNEL', '')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
