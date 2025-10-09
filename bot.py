# bot.py
from telethon import TelegramClient
from telethon.sessions import StringSession
from info import API_ID, API_HASH, PHONE_NUMBER, SOURCE_CHAT_ID
import glob
from aiohttp import web
from Syd.web_support import web_server
import importlib.util
import os
from pyrogram import Client
#from pyrogram.types import StringSession

# Create Telegram client
mrsyd = TelegramClient(StringSession(PHONE_NUMBER), API_ID, API_HASH)

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
    await mrsyd.start()
  #  await app.start() # Userbot requires phone number login
    print("Userbot is running...")

    # Load plugins manually from Syd/
    load_plugins()
    appp = web.AppRunner(await web_server())
    await appp.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(appp, bind_address, 8080).start()

    await mrsyd.run_until_disconnected()
