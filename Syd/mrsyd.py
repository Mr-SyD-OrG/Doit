from telethon import events
import asyncio
from bot import mrsyd


letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
start_year = 2000
end_year = 2004
resolutions = ["240p", "480p", "720p", "1080p", "2160p"]

@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"Search"))
async def handle_search_trigger(event):
    chat_id = event.chat_id
    await event.reply("Starting resolution.")

    for i, year in enumerate(range(start_year, end_year + 1)):
        letter = letters[i % len(letters)]
        for res in resolutions:
            msg = f"{letter} {year} {res}"
            await event.client.send_message(1983814301, msg)
            print(f"Sent: {msg}")
            await asyncio.sleep(600)  # 1 minute delay

    await event.client.send_message(chat_id, "Done sending all resolutions.")
