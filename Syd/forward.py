# plugins/forwarder.py
import asyncio
from asyncio import Semaphore
from telethon import events
from info import DESTINATION_CHAT_ID

# Semaphore to limit concurrent forwards (adjust as needed)
semaphore = Semaphore(2)

@events.register(events.NewMessage(chats=SOURCE_CHAT_ID))
async def forward_message(event):
    """Forwards messages from the source chat to the destination."""
    async with semaphore:
        try:
            print(f"Forwarding message from {event.chat_id} to {DESTINATION_CHAT_ID}...")
            await event.client.send_message(DESTINATION_CHAT_ID, event.message)
            print("Message forwarded successfully!")

            # Delay of 5 minutes before processing the next message
            await asyncio.sleep(300)

        except Exception as e:
            print(f"Error forwarding message: {e}")
