from telethon import events
import asyncio
from bot import mrsyd
import random


letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
start_year = 2000
end_year = 2002
resolutions = ["240p", "480p", "720p", "1080p", "2160p"]
WAIT = [35, 120, 240, 300, 360, 420, 540, 600, 700, 800, 1000, 1200, 3000]
@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"Search"))
async def handle_search_trigger(event):
    await event.reply("Starting resolution.")

    for letter in letters:
        for year in range(start_year, end_year + 1):
            for res in resolutions:
                msg = f"{letter} {year} {res}"
                await event.client.send_message(1983814301, msg)
                print(f"Sent: {msg}")
                await asyncio.sleep(random.choice(WAIT))

    await event.client.send_message(1733124290, "Done sending all resolutions.")
