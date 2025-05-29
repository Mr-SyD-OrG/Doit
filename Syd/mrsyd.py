from telethon import events
import asyncio
import re
from bot import mrsyd
import random


letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#start_year = 2000
start_year = 2020
end_year = 2023
messge = ["A 2000 480p", "A 2000 720p", "A 2000 1080p", "B 2001 480p", "B 2001 720p", "B 2001 1080p", "C 2002 480p", "C 2002 720p", "C 2002 1080p"]
resolutions = ["240p", "480p", "720p", "1080p", "2160p"]
WAIT = [35, 120, 240, 300, 360, 420, 540, 600, 700, 800, 1000, 1200, 3000]

@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"Search"))
async def handle_search_trigger(event):
    await event.reply("Starting resolution.")
 #   start_from = "V 2001 480p"
    start_reached = False
    start_from = "A 2020 240p"
    for letter in letters:
        for year in range(start_year, end_year + 1):
            for res in resolutions:
                msg = f"{letter} {year} {res}"
                # Wait until we reach the starting point
                if not start_reached:
                    if msg == start_from:
                        start_reached = True
                    else:
                        continue
                # Skip if already sent
                if msg in messge:
                    continue
                sydd = random.choice(WAIT)
                await event.client.send_message(1983814301, msg)
                print(f"Sent: {msg} Wait {sydd}")
                await asyncio.sleep(sydd)

    await event.client.send_message(1733124290, "Done sending all resolutions.")






# Replace this with your target channel ID (use a negative number for channels)
TARGET_CHAT_ID = -1002623780966

DISCUSSION_GROUP_ID = -1002470503901  # ID of the group linked to the channel
ADMIN_ID = 1733124290  # Replace with the actual admin ID

@mrsyd.on(events.NewMessage(chats=DISCUSSION_GROUP_ID))
async def handle_comment(event):
    print("🔔 New message in discussion group")
    # Only handle replies to channel posts
    if not event.is_reply:
        print("❌ Not a reply, ignoring")
        return

    try:
        original_msg = await event.get_reply_message()
    except Exception as e:
        print("Failed to fetch replied message:", e)
        return

    if not original_msg or not original_msg.is_channel:
        return  # Ignore replies to non-channel messages

    text = original_msg.raw_text or ""
    text = text.strip()

    match = re.search(r'\b(code|question)\b\s+(.+)', text, re.IGNORECASE)

    if match:
        keyword = match.group(1)
        expr = match.group(2).strip()

        # Check for multiplication
        mul_match = re.match(r'(\d+)\s*[x×]\s*(\d+)', expr)
        if mul_match:
            a = int(mul_match.group(1))
            b = int(mul_match.group(2))
            response = f"{a} × {b} = {a * b}"
        else:
            response = expr

        await event.reply(response)

    else:
        user = await event.get_sender()
        msg_to_admin = (
            f"❌ *No keyword* found in original channel message.\n\n"
            f"👤 *From user:* [{user.first_name}](tg://user?id={user.id})\n"
            f"💬 *Comment:* {event.raw_text}"
        )
        await event.client.send_message(ADMIN_ID, msg_to_admin, parse_mode='markdown')
