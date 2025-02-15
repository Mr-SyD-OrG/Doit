# bot.py
from telethon import TelegramClient
from info import API_ID, API_HASH, PHONE_NUMBER, SOURCE_CHAT_ID

# Create Telegram client with plugin support
client = TelegramClient(
    "userbot_session",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
   # workers=200,
    plugins={"root": "Syd"},  # Load all plugins from "plugins" folder
  #  sleep_threshold=15,
)

# Ensure we only forward messages from the source chat
#client.add_event_handler(forward_message, events.NewMessage(chats=SOURCE_CHAT_ID))

async def start_bot():
    await client.start(PHONE_NUMBER)  # Userbot requires phone number login
    print("Userbot with plugins is running...")
    await client.run_until_disconnected()
