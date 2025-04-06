from telethon import events
import asyncio
from bot import mrsyd


target_users = [6592320604]
# Define your handler
@mrsyd.on(events.NewMessage(from_users=[7065204410], pattern=r"^Check"))
async def trigger(event):
    await event.respond("Starting the daily /start loop.")

    while True:
        for user_id in target_users:
            await mrsyd.send_message(user_id, '/start')
            await asyncio.sleep(60)  # Delay between each message
        #await asyncio.sleep(86400)
        await asyncio.sleep(8)# Wait for a day before repeating
