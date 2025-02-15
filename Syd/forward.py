# plugins/forwarder.py
import asyncio
from asyncio import Semaphore
from telethon import events
from info import DESTINATION_CHAT_ID, SOURCE_CHAT_ID

# Semaphore to limit concurrent forwards (adjust as needed)
semaphore = Semaphore(2)
DESTINATION_CHAT_ID = [-1002433450358, -1002464733363]
SOURCE_CHAT_ID = 
@client.on(events.NewMessage(chats=SOURCE_CHAT_ID))
async def forward_if_allowed(event):
    if event.message.forward:  # Check if forwarding is allowed
        async with semaphore:  # Limit concurrent forwards
            try:
                await client.forward_messages(DESTINATION_CHAT_ID, event.message)
                print("✅ Message forwarded successfully.")
                await asyncio.sleep(300)
            except Exception as e:
                print(f"⚠️ Error forwarding message: {e}")
    else:
        print("❌ Forwarding not allowed for this message. Skipping...")
