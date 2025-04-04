from telethon import events
import asyncio

# Define your handler
@mrsyd.on(events.NewMessage(from_users=[7065204410], pattern=r"^Check"))
async def trigger(event):
    await event.respond("Starting the daily /start loop.")

    while True:
        for user_id in target_users:
            await mrsyd.send_message(user_id, '/start')
            await asyncio.sleep(60)  # Delay between each message
        await asyncio.sleep(86400)  # Wait for a day before repeating
