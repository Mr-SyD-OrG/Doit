from telethon import events
import asyncio
from bot import mrsyd


target_users = [6592320604]
# Define your handler

# Global response tracker
response_received = asyncio.Event()

@mrsyd.on(events.NewMessage(from_users=target_users))
async def handle_response(event):
    # Mark that a message was received
    response_received.set()

@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"^Check"))
async def trigger(event):
    await event.respond("Starting the daily /start loop.")

    while True:
        for user_id in target_users:
            await mrsyd.send_message(user_id, '/start')
            
            # Clear the event before waiting
            response_received.clear()

            try:
                # Wait for a response for up to 60 seconds
                await asyncio.wait_for(response_received.wait(), timeout=60)
            except asyncio.TimeoutError:
                await mrsyd.send_message(1733124290, f"No response from {user_id} within 60 seconds.")

            await asyncio.sleep(1)  # Small delay between each user
        
        await asyncio.sleep(8)  # You can change this to 86400 for a daily cycle
