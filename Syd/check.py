import asyncio
from datetime import datetime, timedelta
from telethon import events
from collections import defaultdict
from bot import mrsyd

target_user_ids = [6592320604, 5334261812]  # Replace with your target user IDs
admin_user_id = 1733124290  # Replace with admin's user ID

# Create a response tracker for ea
@mrsyd.on(events.NewMessage(from_users=[admin_user_id], pattern=r"^Chek"))
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


# Assume you already have a list of user IDs to monitor


# Dictionary to track daily messages from target users
user_message_log = defaultdict(lambda: None)

# Listen to all messages from target users
@mrsyd.on(events.NewMessage(from_users=target_user_ids))
async def handle_target_user_message(event):
    user_id = event.sender_id
    user_message_log[user_id] = datetime.utcnow().date()

# Admin sends "Check" to manually trigger the report
@mrsyd.on(events.NewMessage(from_users=[admin_user_id], pattern=r"^Check"))
async def triger(event):
    today = datetime.utcnow().date()
    missed_users = [uid for uid in target_user_ids if user_message_log[uid] != today]

    if missed_users:
        await event.respond(f"No messages received today from user(s): {', '.join(map(str, missed_users))}")
    else:
        await event.respond("All target users have sent a message today.")

# Optional: Automated daily check at midnight UTC
async def daily_check():
    while True:
        now = datetime.utcnow()
        next_run = datetime.combine(now + timedelta(days=1), datetime.min.time())
        wait_seconds = (next_run - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        missed_users = [uid for uid in target_user_ids if user_message_log[uid] != datetime.utcnow().date()]
        if missed_users:
            await mrsyd.send_message(admin_user_id, f"Daily Check: No messages from user(s): {', '.join(map(str, missed_users))}")
        else:
            await mrsyd.send_message(admin_user_id, "Daily Check: All target users have sent a message today.")

# Start the background task
mrsyd.loop.create_task(daily_check())
