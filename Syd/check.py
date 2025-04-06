from telethon import events
import asyncio
from bot import mrsyd


target_users = [6592320604]  # Replace with real user IDs

# Replace with your admin user ID
admin_user_id = 1733124290

# Create a response tracker for each user
user_response_events = {user_id: asyncio.Event() for user_id in target_users}

@mrsyd.on(events.NewMessage())
async def handle_response(event):
    sender = event.sender_id
    if sender in user_response_events:
        print(f"[DEBUG] Got message from {sender}: {event.text}")
        user_response_events[sender].set()

@mrsyd.on(events.NewMessage(from_users=[admin_user_id], pattern=r"^Check"))
async def trigger(event):
    await event.respond("Starting the daily /start loop.")

    while True:
        for user_id in target_users:
            # Reset the response event before sending
            user_response_events[user_id].clear()

            await mrsyd.send_message(user_id, '/start')

            try:
                # Wait up to 60 seconds for this specific user's response
                await asyncio.wait_for(user_response_events[user_id].wait(), timeout=60)
                print(f"[DEBUG] Received response from {user_id}")
            except asyncio.TimeoutError:
                await mrsyd.send_message(admin_user_id, f"No response from user {user_id} within 60 seconds.")

            await asyncio.sleep(1)  # Small delay before next user

        await asyncio.sleep(8)  # Change to 86400 for daily interval
