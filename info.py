import re, time
from os import environ
 

id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.strip().lower() in ["on", "true", "yes", "1", "enable", "y"]: return True
    elif value.strip().lower() in ["off", "false", "no", "0", "disable", "n"]: return False
    else: return default


DATABASE_NAME = environ.get('DATABASE_NAME', "Mrsyd")
DATABASE_URL = environ.get('DATABASE_URL', "")
API_ID1 = environ.get('API_URL', "")
API_HASH1 = environ.get('API_URI', "")
API_ID2 = environ.get('API_URL2', "")
API_HASH2 = environ.get('API_URI2', "")
TELETHON_SESSION = environ.get('TELETHON_SESSION', "")
PHONE_NUMBER1 = environ.get('NUMB', "")
PHONE_NUMBER2 = environ.get('NUMB2', "")
VSYD = environ.get("VSYD", "True").lower() == "true"
SOURCE_CHAT_ID = -1002295881345  # Replace with source chat ID
DESTINATION_CHAT_ID = -1002377676305
auth_channel = environ.get('AUTH_CHANNEL', '')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
