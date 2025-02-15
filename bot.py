# bot.py
from telethon import TelegramClient
from info import API_ID, API_HASH, PHONE_NUMBER, SOURCE_CHAT_ID
import glob
import importlib.util
import os

# Create Telegram client
client = TelegramClient("userbot_session", API_ID, API_HASH)

# Function to dynamically load plugins from the 'Syd' directory
def load_plugins():
    plugins_path = "Syd"  # Change from "plugins" to "Syd"
    for file in glob.glob(f"{plugins_path}/*.py"):
        module_name = os.path.basename(file)[:-3]  # Remove .py extension
        module_path = f"{plugins_path}.{module_name}"
        spec = importlib.util.spec_from_file_location(module_path, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"Loaded plugin: {module_name}")

async def start_bot():
    await client.start(PHONE_NUMBER)  # Userbot requires phone number login
    print("Userbot is running...")

    # Load plugins manually from Syd/
    load_plugins()

    await client.run_until_disconnected()
